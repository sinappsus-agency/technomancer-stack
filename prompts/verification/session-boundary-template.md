# Session Boundary Template

**Purpose:** Use this at the start of every new AI conversation (or every ~20 exchanges) to reset context and prevent drift.

---

## Instructions

Copy the block below. Fill in the `[ ]` placeholders. Paste it as your first message in a new conversation, or insert it mid-session when you notice the AI losing track of your original brief.

---

```
## CONTEXT RESET — Session Boundary

**Who I am:**
I am [your name / role — e.g., "Jacques, a solo creative technologist and founder of Sinappsus"].

**My brand voice:**
[One or two sentences describing your communication style — e.g., "Direct, technically grounded, no fluff. I write for practitioners, not for hype. I use real tools and real numbers."]

**The project I am working on:**
[Specific project name and phase — e.g., "The Technomancer manuscript — Part III, Chapter 14: n8n and the Automation Layer. I am expanding the existing draft."]

**What we are doing in this session:**
[One clear task statement — e.g., "I need you to write the 'Making Workflows Robust' section — approximately 600 words. Tone: technical but practical. Include real n8n error handling patterns."]

**Constraints:**
- [Any hard rules — e.g., "Do not invent products that do not exist."]
- [Any scope limits — e.g., "Only cover n8n self-hosted, not cloud n8n."]
- [Any style rules — e.g., "No motivational fluff. Start with the problem, not the solution."]

**Context files you may reference:**
- [File 1 name or contents]
- [File 2 name or contents]

**Output format I expect:**
[Description — e.g., "Markdown prose, H2 subheadings, one code block showing the error handler JSON structure. Approximately 600 words."]
```

---

## When to Use This Template

| Situation | Action |
|-----------|--------|
| Starting a new conversation | Use the full template |
| After ~20 exchanges in a long session | Use a condensed 3-line version: who/project/task |
| When the AI starts giving answers that miss the brief | Insert the template and continue |
| When switching projects in the same session | Use the full template again |
| After a complex tangent or deep debug session | Condensed reset |

---

## Condensed Mid-Session Version

For quick resets during a session, use just this:

```
## Context Reset

I am [name], working on [project]. We are currently doing [specific task].
My constraints are: [one sentence]. 
Please continue with [next action].
```

---

## Why This Works

Every AI conversation has a context window. As a session progresses, older instructions get pushed further from the model's effective attention. When you provide the context again, you are not repeating yourself — you are restoring working memory. 

Think of it as saving your game. The session boundary template is a save point.

---

*See also:* `prompts/verification/ai-output-checklist.md` — for verifying the output after you get it.
