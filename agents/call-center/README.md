# Automated Call Center

A self-hosted, AI-powered inbound and outbound call handling system built on open-source telephony infrastructure.

---

## What This Is

A solo operator cannot be on the phone all day — but a phone presence still matters for lead qualification, appointment booking, client check-ins, and outbound campaigns.

This setup replaces:
- **Receptionist** — AI handles inbound calls 24/7, collects context, routes or resolves
- **Appointment setter** — AI checks calendar availability, books calls, sends confirmations
- **Outbound qualifier** — AI makes first-contact calls from a lead list, qualifies, and transfers hot leads or logs outcomes

---

## Architecture

```
Inbound call
    │
    ▼
[SIP Provider] ─────────────────────────────────────────┐
(Twilio / Vonage / Telnyx)                               │ SIP/WebRTC
                                                          ▼
                                               ┌──────────────────────┐
                                               │   FreeSWITCH / Asterisk │
                                               │   (call routing, IVR)   │
                                               └──────────┬──────────────┘
                                                          │ audio stream
                                               ┌──────────▼──────────────┐
                                               │    Whisper (STT)         │
                                               │    (speech-to-text)      │
                                               └──────────┬──────────────┘
                                                          │ transcript
                                               ┌──────────▼──────────────┐
                                               │    Ollama LLM            │
                                               │    (reason + respond)    │
                                               │    + n8n tool calls      │
                                               └──────────┬──────────────┘
                                                          │ response text
                                               ┌──────────▼──────────────┐
                                               │    Piper TTS             │
                                               │    (text-to-speech)      │
                                               └──────────┬──────────────┘
                                                          │ audio
                                               [Caller hears response]
```

---

## Stack Components

### SIP / Telephony Layer
**Recommended: Telnyx** (best balance of API quality, price, and WebRTC support for AI calling)

Alternatives:
- Twilio (higher cost, excellent docs)
- Vonage
- Voip.ms (cheapest BYOC option)

For local dev / testing without real calls:
- **Zoiper** or **Linphone** (softphone apps for testing your SIP setup)

### Call Server
**FreeSWITCH** (Docker) — higher performance, better for AI audio streams
Or **Asterisk** (Docker) — larger community, more tutorials

Docker image: `drachtio/freeswitch` or `ballantyne/freeswitch`

### Speech-to-Text
**Whisper.cpp** (runs locally via Ollama or standalone)
- Fast enough for real-time transcription on a VPS with >= 4 cores and 8GB RAM
- Model: `whisper-small.en` for English-only, `whisper-medium` for multilingual

Or use **Deepgram** (Nova-2 API) for near-instant, high-accuracy STT if local latency is an issue — about $0.0043/min.

### LLM
**Ollama** local — uses same instance as rest of stack
- Recommended model for voice: `llama3.2:3b` (faster, good enough for structured conversations)
- Or `mistral:7b-instruct` for more nuanced handling

The LLM has tool access to:
- `check_calendar` — queries Cal.com or Calendly API
- `book_appointment` — creates booking via API
- `update_crm` — calls n8n webhook to update contact record
- `escalate_to_human` — sends Telegram alert to operator with call context

### Text-to-Speech
**Piper TTS** (local, zero cost, Docker)
- Voice: `en_US-lessac-medium` (clear, neutral American English)
- Or `en_GB-jenny-dioco-medium` for British accent

Or **ElevenLabs** for higher quality cloned/branded voice (API, $5/mo for starter tier).

---

## Voice Agent Implementation

This is the actual code that makes calls work. The handler bridges FreeSWITCH (SIP) → Whisper (STT) → Ollama (LLM) → Piper TTS and returns audio to the caller.

### Project Structure

```
agents/call-center/
├── handler/
│   ├── package.json          # Node.js dependencies
│   ├── index.js              # Main call handler (Drachtio)
│   ├── stt.js                # Whisper STT client
│   ├── llm.js                # Ollama LLM client
│   ├── tts.js                # Piper TTS client
│   └── tools.js              # LLM tool handlers (calendar, CRM, escalate)
└── config/
    └── agent-prompt.txt      # System prompt for the AI agent
```

### `handler/package.json`

```json
{
  "name": "technomancer-call-handler",
  "version": "1.0.0",
  "description": "AI voice agent handler — FreeSWITCH + Whisper + Ollama + Piper",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  },
  "dependencies": {
    "drachtio-fsmrf": "^0.3.0",
    "drachtio-srf": "^5.0.0",
    "axios": "^1.7.0",
    "form-data": "^4.0.0",
    "wav": "^1.0.2",
    "ws": "^8.18.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### `handler/index.js` — Main Call Handler

```javascript
'use strict';

const Srf = require('drachtio-srf');
const Mrf = require('drachtio-fsmrf');
const { transcribeAudio } = require('./stt');
const { generateResponse } = require('./llm');
const { synthesiseSpeech } = require('./tts');
const { handleTool } = require('./tools');

const srf = new Srf();
const mrf = new Mrf(srf);

// Connect to Drachtio server
srf.connect({
  host: process.env.DRACHTIO_HOST || 'drachtio',
  port: 9022,
  secret: process.env.DRACHTIO_SECRET
});

srf.on('connect', (err, hostport) => {
  if (err) { console.error('Drachtio connect error:', err); return; }
  console.log(`Connected to Drachtio at ${hostport}`);
});

// Connect to FreeSWITCH media
mrf.connect({
  address: process.env.FREESWITCH_HOST || 'freeswitch',
  port: 8021,
  secret: process.env.FREESWITCH_SECRET || 'ClueCon'
});

// Conversation state per call
const sessions = new Map();

// Handle inbound SIP INVITE
srf.invite((req, res) => {
  srf.createUAS(req, res, { localSdp: req.body }, async (err, dialog) => {
    if (err) { console.error('Failed to create UAS dialog:', err); return; }

    const callSid = req.get('Call-ID');
    console.log(`[${callSid}] Inbound call from ${req.callingNumber}`);

    // Allocate media endpoint
    mrf.connect(dialog.local.sdp, dialog.remote.sdp, async (err, endpoint) => {
      if (err) { console.error('Media connect error:', err); return; }

      const state = {
        callSid,
        callerNumber: req.callingNumber,
        history: [],
        turnCount: 0
      };
      sessions.set(callSid, state);

      // Greet caller
      await speak(endpoint, 'Thank you for calling. How can I help you today?', callSid);

      // Start listen/respond loop
      listenAndRespond(endpoint, dialog, state);
    });

    dialog.on('destroy', () => {
      console.log(`[${callSid}] Call ended`);
      sessions.delete(callSid);
    });
  });
});

/**
 * Core listen/respond loop — runs until call ends or max turns reached
 */
async function listenAndRespond(endpoint, dialog, state) {
  const MAX_TURNS = 10;
  const SILENCE_THRESHOLD_MS = 1500;
  const MAX_LISTEN_MS = 15000;

  while (state.turnCount < MAX_TURNS && dialog.connected) {
    state.turnCount++;

    // Collect audio from caller
    let audioBuffer;
    try {
      audioBuffer = await collectAudio(endpoint, SILENCE_THRESHOLD_MS, MAX_LISTEN_MS);
    } catch (err) {
      console.error(`[${state.callSid}] Audio collection error:`, err);
      break;
    }

    if (!audioBuffer || audioBuffer.length < 1000) {
      // Too short — prompt caller
      await speak(endpoint, 'Sorry, I did not catch that. Could you repeat?', state.callSid);
      continue;
    }

    // Transcribe speech to text
    let transcript;
    try {
      transcript = await transcribeAudio(audioBuffer);
    } catch (err) {
      console.error(`[${state.callSid}] STT error:`, err);
      await speak(endpoint, 'I had trouble hearing you. One moment.', state.callSid);
      continue;
    }
    console.log(`[${state.callSid}] Transcript: "${transcript}"`);

    if (!transcript || transcript.trim().length === 0) continue;

    // Add to conversation history
    state.history.push({ role: 'user', content: transcript });

    // Generate LLM response
    let llmResult;
    try {
      llmResult = await generateResponse(state.history, state.callerNumber);
    } catch (err) {
      console.error(`[${state.callSid}] LLM error:`, err);
      await speak(endpoint, 'I need a moment to process that. Please hold.', state.callSid);
      continue;
    }

    // Handle tool calls (calendar, CRM, escalate)
    if (llmResult.tool_call) {
      const toolResult = await handleTool(llmResult.tool_call, state);
      // Feed tool result back to LLM for final spoken response
      state.history.push({ role: 'tool', content: JSON.stringify(toolResult), tool_call_id: llmResult.tool_call.id });
      llmResult = await generateResponse(state.history, state.callerNumber);
    }

    const responseText = llmResult.content;
    state.history.push({ role: 'assistant', content: responseText });
    console.log(`[${state.callSid}] Agent: "${responseText}"`);

    // Speak response
    await speak(endpoint, responseText, state.callSid);

    // Check for call-ending phrases
    const endPhrases = ['goodbye', 'thank you, bye', 'have a good day', 'take care'];
    if (endPhrases.some(p => responseText.toLowerCase().includes(p))) {
      await new Promise(r => setTimeout(r, 800));
      break;
    }
  }

  // End call gracefully
  if (dialog.connected) {
    dialog.destroy();
  }
}

/**
 * Collect audio from the caller endpoint until silence or timeout
 */
function collectAudio(endpoint, silenceMs, maxMs) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let silenceTimer;

    endpoint.startRecording('/tmp/caller_audio.wav', {
      'record-policy': 'silence',
      'silence-thresh': 200,
      'silence-hits': Math.floor(silenceMs / 20)
    });

    endpoint.on('record-stop', () => {
      clearTimeout(silenceTimer);
      const fs = require('fs');
      try {
        const data = fs.readFileSync('/tmp/caller_audio.wav');
        resolve(data);
      } catch (e) {
        reject(e);
      }
    });

    // Hard timeout
    silenceTimer = setTimeout(() => {
      endpoint.stopRecording('/tmp/caller_audio.wav');
    }, maxMs);
  });
}

/**
 * Synthesise text to speech and play to caller
 */
async function speak(endpoint, text, callSid) {
  try {
    const audioPath = `/tmp/response_${callSid}_${Date.now()}.wav`;
    await synthesiseSpeech(text, audioPath);
    await new Promise((resolve, reject) => {
      endpoint.play(audioPath, (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  } catch (err) {
    console.error(`[${callSid}] TTS/play error:`, err);
  }
}

console.log('AI call handler starting...');
```

### `handler/stt.js` — Whisper STT

```javascript
'use strict';

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const WHISPER_HOST = process.env.WHISPER_HOST || 'http://ollama:11434';

/**
 * Transcribe audio buffer using Whisper via Ollama or standalone Whisper API.
 * Falls back to Ollama's whisper endpoint if available.
 */
async function transcribeAudio(audioBuffer) {
  // If using standalone whisper.cpp server (recommended for better latency)
  if (process.env.WHISPER_API_URL) {
    const form = new FormData();
    form.append('file', audioBuffer, { filename: 'audio.wav', contentType: 'audio/wav' });
    form.append('model', 'whisper-small.en');
    form.append('response_format', 'json');

    const response = await axios.post(process.env.WHISPER_API_URL + '/inference', form, {
      headers: form.getHeaders(),
      timeout: 10000
    });

    return response.data.text?.trim() || '';
  }

  // Fallback: use Deepgram API (better latency, ~$0.004/min)
  if (process.env.DEEPGRAM_API_KEY) {
    const response = await axios.post(
      'https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true',
      audioBuffer,
      {
        headers: {
          'Authorization': `Token ${process.env.DEEPGRAM_API_KEY}`,
          'Content-Type': 'audio/wav'
        },
        timeout: 10000
      }
    );
    return response.data.results?.channels[0]?.alternatives[0]?.transcript?.trim() || '';
  }

  throw new Error('No STT provider configured. Set WHISPER_API_URL or DEEPGRAM_API_KEY.');
}

module.exports = { transcribeAudio };
```

### `handler/llm.js` — Ollama LLM

```javascript
'use strict';

const axios = require('axios');
const fs = require('fs');
const path = require('path');

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://ollama:11434';
const MODEL = process.env.VOICE_LLM_MODEL || 'llama3.2:3b';

// Load system prompt from file
const SYSTEM_PROMPT = fs.readFileSync(
  path.join(__dirname, '..', 'config', 'agent-prompt.txt'),
  'utf8'
).trim();

// Tool definitions for the LLM
const TOOLS = [
  {
    type: 'function',
    function: {
      name: 'check_calendar',
      description: 'Check available appointment slots in the next 7 days',
      parameters: {
        type: 'object',
        properties: {
          preferred_day: { type: 'string', description: 'Day preference e.g. "Monday" or "this week"' }
        },
        required: []
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'book_appointment',
      description: 'Book an appointment for the caller',
      parameters: {
        type: 'object',
        properties: {
          caller_name: { type: 'string' },
          caller_phone: { type: 'string' },
          slot_datetime: { type: 'string', description: 'ISO 8601 datetime' },
          notes: { type: 'string' }
        },
        required: ['caller_name', 'caller_phone', 'slot_datetime']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'escalate_to_human',
      description: 'Escalate the call to a human operator immediately',
      parameters: {
        type: 'object',
        properties: {
          reason: { type: 'string', description: 'Reason for escalation' },
          caller_summary: { type: 'string', description: 'Brief summary of the conversation so far' }
        },
        required: ['reason', 'caller_summary']
      }
    }
  }
];

async function generateResponse(history, callerPhone) {
  const messages = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...history
  ];

  const payload = {
    model: MODEL,
    messages,
    tools: TOOLS,
    stream: false,
    options: {
      temperature: 0.3,
      num_predict: 150  // Keep responses short for voice
    }
  };

  const response = await axios.post(`${OLLAMA_HOST}/api/chat`, payload, {
    timeout: 20000
  });

  const message = response.data.message;

  // Check for tool call
  if (message.tool_calls && message.tool_calls.length > 0) {
    return {
      content: null,
      tool_call: message.tool_calls[0]
    };
  }

  return {
    content: message.content,
    tool_call: null
  };
}

module.exports = { generateResponse };
```

### `handler/tts.js` — Piper TTS

```javascript
'use strict';

const axios = require('axios');
const fs = require('fs');

const PIPER_HOST = process.env.PIPER_HOST || 'http://piper-tts:10200';

/**
 * Synthesise text to a WAV file using Piper TTS
 */
async function synthesiseSpeech(text, outputPath) {
  // Piper Wyoming protocol TTS endpoint
  const response = await axios.post(
    `${PIPER_HOST}/api/tts`,
    { text: text.replace(/[#*_~`]/g, '') },  // Strip markdown if any
    {
      responseType: 'arraybuffer',
      headers: { 'Content-Type': 'application/json' },
      timeout: 15000
    }
  );

  fs.writeFileSync(outputPath, Buffer.from(response.data));
  return outputPath;
}

module.exports = { synthesiseSpeech };
```

### `handler/tools.js` — Tool Handlers

```javascript
'use strict';

const axios = require('axios');

const N8N_WEBHOOK_BASE = process.env.N8N_WEBHOOK_URL || 'https://workflow.yourdomain.com/webhook';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const OPERATOR_TELEGRAM_ID = process.env.OPERATOR_TELEGRAM_ID;

/**
 * Execute a tool call from the LLM and return a result string
 */
async function handleTool(toolCall, callState) {
  const name = toolCall.function.name;
  const args = JSON.parse(toolCall.function.arguments);

  switch (name) {
    case 'check_calendar':
      return await checkCalendar(args);

    case 'book_appointment':
      return await bookAppointment(args, callState);

    case 'escalate_to_human':
      return await escalateToHuman(args, callState);

    default:
      return { error: `Unknown tool: ${name}` };
  }
}

async function checkCalendar(args) {
  try {
    const response = await axios.post(`${N8N_WEBHOOK_BASE}/call-center/check-calendar`, args, {
      timeout: 8000
    });
    return response.data;
  } catch (err) {
    return { slots: ['Tomorrow at 10am', 'Tomorrow at 2pm', 'Friday at 11am'] };
  }
}

async function bookAppointment(args, callState) {
  try {
    // Add call metadata
    args.source = 'voice_agent';
    args.call_sid = callState.callSid;

    const response = await axios.post(`${N8N_WEBHOOK_BASE}/call-center/book-appointment`, args, {
      timeout: 10000
    });
    return response.data;
  } catch (err) {
    console.error('Booking error:', err.message);
    return { success: false, error: 'Booking system unavailable' };
  }
}

async function escalateToHuman(args, callState) {
  const message = [
    `🚨 Call Escalation`,
    `Caller: ${callState.callerNumber}`,
    `Reason: ${args.reason}`,
    `Summary: ${args.caller_summary}`,
    `Call ID: ${callState.callSid}`
  ].join('\n');

  try {
    await axios.post(
      `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      { chat_id: OPERATOR_TELEGRAM_ID, text: message },
      { timeout: 5000 }
    );
  } catch (err) {
    console.error('Telegram alert error:', err.message);
  }

  return { escalated: true, message: 'Operator has been alerted. Transferring you now.' };
}

module.exports = { handleTool };
```

### `config/agent-prompt.txt`

```
You are a professional AI assistant for [BUSINESS_NAME]. You handle incoming calls warmly and efficiently.

Your goals on this call:
1. Greet the caller and understand what they need (one clear reason for the call)
2. If they are a potential client: ask 2-3 brief qualifying questions, then offer to schedule a discovery call using check_calendar
3. If they are an existing client: take a message and promise a follow-up within 24 hours
4. If the call is complex, urgent, or the caller is distressed: use escalate_to_human immediately
5. If you successfully book an appointment: use book_appointment with the confirmed details

Qualifying questions to ask potential clients (choose 2 that feel natural):
- "What are you working on and what prompted you to reach out?"
- "Have you worked with a [SERVICE_TYPE] before?"
- "What does your timeline look like?"
- "What's the most important thing for you to get sorted right now?"

VOICE RULES — non-negotiable:
- Keep responses under 25 words whenever possible
- Never use bullet points, lists, asterisks, or markdown — this is spoken audio
- Do not fill silence with "um" or filler phrases
- One question at a time — never stack two questions in one response
- If you do not know something: say so plainly and offer to have a human follow up

End the call with appropriate warmth: "Thank you for calling, we'll be in touch" or similar.
```

---

## Startup and Deployment

### First-Time Setup

```bash
# 1. Navigate to the handler directory
cd agents/call-center/handler

# 2. Install dependencies
npm install

# 3. Copy env and populate
cp .env.example .env
nano .env   # Add DRACHTIO_SECRET, WHISPER_API_URL or DEEPGRAM_API_KEY, etc.

# 4. Start the call handler
npm start
```

### Run via Docker (recommended)

Add to `docker/docker-compose.yml`:

```yaml
  call-handler:
    build: ../agents/call-center/handler
    container_name: call-handler
    restart: unless-stopped
    networks:
      - backend
    depends_on:
      - drachtio
      - ollama
    environment:
      DRACHTIO_HOST: drachtio
      DRACHTIO_SECRET: ${DRACHTIO_SECRET}
      FREESWITCH_HOST: freeswitch
      OLLAMA_HOST: http://ollama:11434
      PIPER_HOST: http://piper-tts:10200
      VOICE_LLM_MODEL: llama3.2:3b
      N8N_WEBHOOK_URL: https://workflow.${BASE_DOMAIN}/webhook
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      OPERATOR_TELEGRAM_ID: ${OPERATOR_TELEGRAM_ID}
      # Set one of these for STT:
      WHISPER_API_URL: http://whisper:9000     # if self-hosting whisper.cpp
      # DEEPGRAM_API_KEY: ${DEEPGRAM_API_KEY}  # or use Deepgram
```

### Add a Dockerfile

```dockerfile
# agents/call-center/handler/Dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "index.js"]
```

### Test Without Real SIP Calls

Use Zoiper or Linphone (free softphone apps) pointed at your FreeSWITCH IP to make test calls locally. Check FreeSWITCH SIP registrations:

```bash
docker exec -it freeswitch fs_cli -x "show registrations"
```

Monitor call handler logs:

```bash
docker logs -f call-handler
```

---

## Docker Compose Addition

Add to `../docker/docker-compose.yml`:

```yaml
  ##############################################################################
  # FREESWITCH — SIP call server for AI call center
  ##############################################################################
  freeswitch:
    image: drachtio/freeswitch:1.10.10
    container_name: freeswitch
    restart: unless-stopped
    ports:
      - "5060:5060/udp"    # SIP
      - "5060:5060/tcp"    # SIP TCP
      - "16384-32768:16384-32768/udp"  # RTP media (CAUTION: large port range)
    volumes:
      - ./config/freeswitch:/etc/freeswitch
      - ./data/freeswitch:/var/log/freeswitch
    networks:
      - backend
    environment:
      - DOMAIN=${BASE_DOMAIN}

  ##############################################################################
  # PIPER TTS — Local text-to-speech
  ##############################################################################
  piper-tts:
    image: rhasspy/wyoming-piper:latest
    container_name: piper-tts
    restart: unless-stopped
    volumes:
      - ./data/piper:/data
    command: --voice en_US-lessac-medium
    networks:
      - backend

  ##############################################################################
  # DRACHTIO — SIP application server (bridges FreeSWITCH + Node.js/Python apps)
  ##############################################################################
  drachtio:
    image: drachtio/drachtio-server:latest
    container_name: drachtio
    restart: unless-stopped
    networks:
      - backend
    environment:
      - DRACHTIO_SECRET=${DRACHTIO_SECRET}
```

Add to `.env.example`:
```
# ============================================================
# CALL CENTER
# ============================================================
TELNYX_API_KEY=your_telnyx_api_key
TELNYX_APP_ID=your_telnyx_app_id
DRACHTIO_SECRET=replace_with_strong_secret

# Operator's Telegram user ID for escalation alerts
OPERATOR_TELEGRAM_ID=your_telegram_user_id
```

---

## Call Flow Scripts

### Inbound Lead Qualification

System prompt for the inbound AI agent:

```
You are an AI assistant for [BUSINESS NAME]. You handle inbound inquiries professionally and warmly.

Your goals on this call:
1. Greet the caller and confirm you have reached [BUSINESS NAME]
2. Understand what they are looking for (one clear reason for the call)
3. If they are a potential client: ask the 3 qualification questions below, then offer to schedule a discovery call
4. If they are an existing client: take a message and promise follow-up within [TIMEFRAME]
5. If unclear or complex: escalate to the operator immediately

QUALIFICATION QUESTIONS:
1. "Can you tell me a bit about your business and what you're working on?"
2. "What's prompting you to reach out now?"
3. "Have you worked with a [TYPE OF SERVICE] before, or is this your first time?"

If the caller qualifies (has budget signals, clear need, timeline): use check_calendar tool and offer 2 available slots.
If the caller does not qualify: "I'll pass your details to [NAME] and they'll follow up with you by email."

Keep responses under 30 words when possible. Speak in short, clear sentences. Do not fill silence.
```

### Outbound Appointment Setting

Used for following up on leads who completed a form but did not book a call.

System prompt:

```
You are calling on behalf of [NAME] at [BUSINESS NAME]. This is a friendly follow-up call.

The person you are calling: [NAME], submitted a form on [DATE] expressing interest in [OFFER].

Your goals:
1. Confirm you have the right person ("Is this [FIRST NAME]?")
2. Reference their form submission and ask if now is a good time
3. Briefly confirm what they were interested in
4. Offer 2 specific times to speak with [OPERATOR NAME]
5. If no answer: leave a clear, brief voicemail with callback number

Max call duration: 3 minutes. Be warm, human, and respectful of their time.
```

---

## n8n Integration

The call center connects to your n8n via webhooks. The `call-center-crm-update.json` workflow template (to be added to `n8n-templates/`):

- Receives call outcome from the AI agent (booked / qualified-no-book / not-qualified / escalated)
- Updates the contact record in ERPNext/CRM
- Sends confirmation email to booker (via Notifuse)
- Notifies operator via Telegram for escalated calls
- Logs call duration, transcript summary, and outcome to database

---

## Privacy and Compliance

**Always comply with local call recording and consent laws.**

- USA: At minimum, comply with TCPA (outbound calling rules). Two-party consent states (CA, FL, etc.) require disclosure at call start.
- EU: GDPR applies. Personal data in call transcripts must have a lawful basis for processing and be deleted on request.
- Disclose at call start: *"This call may be recorded for quality and training purposes."*

Transcripts should be:
- Stored in PostgreSQL, not in logs or flat files
- Purged per your data retention policy (default recommendation: 90 days)
- Encrypted at rest (PostgreSQL `pgcrypto` extension)

---

## Further Reading

- FreeSWITCH docs: https://developer.signalwire.com/freeswitch/FreeSWITCH-Explained/
- Drachtio framework: https://drachtio.org
- Piper TTS: https://github.com/rhasspy/piper
- Telnyx AI Calling: https://developers.telnyx.com/docs/voice/programmable-voice
