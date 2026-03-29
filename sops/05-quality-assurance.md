# SOP 05 — Quality Assurance

**Category:** Quality Assurance
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Deliverable ready for client delivery
**Frequency:** Per deliverable

---

## Objective

Ensure that nothing leaves the studio that does not meet the brand standard. Quality control should not depend on the operator's mood or memory — it is a checklist executed before every delivery.

---

## Prerequisites

- [ ] Work is complete from the delivery team/contractor's perspective
- [ ] All source files are in the correct project folder
- [ ] 24 hours have passed since final creative work (wherever possible) — fresh eyes catch more

---

## Universal QA Checklist (all deliverables)

Run this before every client delivery regardless of type:

- [ ] **Completeness:** All items agreed in scope are present. Nothing is missing.
- [ ] **Accuracy:** Factual claims, names, dates, numbers, and product details are correct.
- [ ] **Brand consistency:** Deliverable matches client's brand guidelines (colours, fonts, voice, tone).
- [ ] **Spelling and grammar:** Run through grammars check tool AND read aloud (the ear catches what the eye misses).
- [ ] **Links and functionality:** All links work. All interactive elements function correctly.
- [ ] **File format:** Files delivered in the correct format (PDF, editable source, PNG @ correct resolution, etc.).
- [ ] **File naming:** Files named per agreed convention: `[client-slug]_[deliverable-type]_v[X].[ext]`
- [ ] **No placeholders:** No `[INSERT TEXT HERE]`, test content, or Lorem Ipsum remaining.
- [ ] **Metadata:** Document metadata (author field, hidden tracked changes) is cleaned before delivery.

---

## Type-Specific Checklists

### Written Content (copy, blog posts, email sequences)

- [ ] Voice and tone match the client's brand guide
- [ ] Word count is within agreed range
- [ ] CTAs present and correctly formatted
- [ ] Headers follow a logical hierarchy (H1 → H2 → H3)
- [ ] No unattributed quotes or unverified statistics
- [ ] SEO meta title and description are present (if applicable)
- [ ] Internal links (if applicable) point to correct URLs

### Visual Design (logos, social assets, presentations, brochures)

- [ ] Colour values match brand hex/CMYK/Pantone exactly
- [ ] Fonts are the correct licensed versions (not substitutes)
- [ ] Exported at correct resolution: 72dpi screen / 300dpi print
- [ ] Bleed and margins correct for print (if applicable)
- [ ] All licensed assets (stock photos, icons) have correct licence for the use case
- [ ] Editable source file (.ai, .psd, .figma) delivered alongside exported files

### Web / Software Deliverables

- [ ] Tested in Chrome, Firefox, and Safari (minimum)
- [ ] Mobile responsive at 375px, 768px, 1200px breakpoints
- [ ] No console errors
- [ ] All environment variables are in `.env.example` — no hardcoded secrets in code
- [ ] README or handoff documentation is complete
- [ ] Staging environment tested before production deploy

### Email Campaigns

- [ ] Subject line and preview text are both populated
- [ ] All personalisation tokens ({{first_name}}) have fallback values
- [ ] Tested via Litmus or equivalent (renders correctly in Gmail, Outlook, Apple Mail)
- [ ] Unsubscribe link present and functional
- [ ] Sender name and from address are correct
- [ ] Campaign is scheduled at the correct time in the client's timezone
- [ ] Tracking UTM parameters set correctly

### Video / Audio Deliverables

- [ ] Exported at agreed specification (codec, resolution, bitrate, duration)
- [ ] Captions/subtitles present if required
- [ ] Audio mix is balanced — dialogue does not clip; music does not overpower speech
- [ ] All licensed music/SFX have correct licence for the use case
- [ ] No jump cuts or sync errors at delivery point
- [ ] Thumbnail prepared and correctly sized

---

## Proofing and Annotation Process

1. Create a proofing link (Loom, Figma, Google Docs comment mode, or PDF with annotations enabled)
2. Share with client with specific review instructions:
   *"Please share feedback using [commenting tool]. If the change is minor, note it directly. If you are unsure about a direction, flag it as a question, not a change request."*
3. Set a review deadline: *"Please share your feedback by [DATE] so we can maintain our delivery schedule."*

---

## Approval Gate

No deliverable moves to final delivery without:
- [ ] Internal QA checklist completed (this document)
- [ ] Any contractor/team review complete
- [ ] Operator sign-off

If a deliverable fails QA, it goes back to revision — not to the client.

---

## Tools Required

- Grammarly or LanguageTool (copy QA)
- Litmus or Mailtrap (email rendering tests)
- Browser DevTools (web QA)
- Figma / Adobe (visual QA)
- Loom or Figma comment mode (client annotation)

---

## Failure Modes and Escalation

**Failure: QA reveals a significant issue late in the process**
Do not rush delivery to hide the issue. Notify the client of a short delay and the reason. Clients respect transparency. Undisclosed problems delivered on time destroy trust permanently.

**Failure: Client finds an error you missed in QA**
Own it immediately. Fix it. Do not defend the miss. Improve the QA checklist with the specific check that would have caught it.

**Failure: QA takes too long and is becoming a bottleneck**
Break large QA into stage-gates within the project (QA at each milestone, not just the end). Running QA at delivery only on a large project is the problem.

---

## Output / Handoff

QA complete when:
- [ ] Checklist above fully executed
- [ ] Any issues found are resolved
- [ ] Operator has signed off
- [ ] Deliverable ready for Step 8 of SOP 04 (Project Management)
