# AI Output Verification Checklist

**Chapter Reference:** Chapter 6 — AI as Creative Clone
**Usage:** Run through this checklist before publishing, sending, or deploying any AI-assisted output.

---

## The Three-Check Verification Protocol

### Check 1: Source Check (Specifics)

Review the output and mark every item below that appears:

- [ ] Statistics or numerical claims (`X% of...`, `$X billion...`, etc.)
- [ ] Citations or references to named studies, reports, or research
- [ ] URLs or web addresses
- [ ] Proper names of companies (not publicly known ones)
- [ ] Product names, version numbers, or pricing
- [ ] Legal provisions, clause numbers, jurisdiction-specific rules
- [ ] Dates (especially recent events)
- [ ] Quotes attributed to named individuals

**For each marked item:**
- [ ] I have verified this against an authoritative primary source
- [ ] I have noted where I verified it

> Rule: If you cannot verify it, remove it or flag it as unverified.

---

### Check 2: Logic Check (Internal Consistency)

Read the output as a skeptical editor. Check:

- [ ] The conclusion follows logically from the evidence presented
- [ ] No claims in the output contradict each other
- [ ] No claims contradict established facts in my domain knowledge
- [ ] Weasel words (`it is widely believed`, `many experts say`, `research suggests`) are either removed or replaced with specific sources
- [ ] The output actually answers the question asked, not an easier adjacent question
- [ ] Hedging language accurately reflects actual uncertainty (not false confidence, not excessive qualification)

---

### Check 3: Execution Check (Code, Instructions, Automations)

*Skip if output is purely text with no commands, code, or step-by-step instructions.*

- [ ] I have run the code in a safe test environment
- [ ] The code does what I expected it to do
- [ ] I have reviewed the code for the following specific issues:
  - [ ] No user input directly interpolated into database queries (SQL injection)
  - [ ] No credentials hardcoded in the code (should be in environment variables)
  - [ ] Authentication exists on any endpoint that should require it
  - [ ] No overly permissive CORS settings
  - [ ] Package/dependency version numbers verified against current official documentation
- [ ] I can explain what every section of the code does

---

## Quick Reference: What AI Fabricates Most Often

High risk (verify always):
- Statistics and percentages
- Named research studies
- URLs and links
- Legal and regulatory specifics
- Price points and financial figures
- Recent events (within last 18 months)
- Niche industry details

Lower risk (spot-check):
- Well-established conceptual explanations
- Common procedural descriptions
- General structural advice
- Creative drafts and copy (check for plagiarism, not factual accuracy)

---

## Session Boundary Template

Paste this at the start of any AI writing session on a project to prevent context drift:

```
Project context: [Project name]
My role: [Your professional role]
Writing style: [e.g., First-person, direct, technical but accessible, no jargon without explanation]
Target reader: [Specific audience description]
Core argument / thesis: [What this project is trying to establish or demonstrate]
Key terms we use consistently: [Any specific terminology or brand language]
What we have established so far: [Brief summary of decisions made in previous sessions]
Constraints: [Word count, format requirements, things to avoid]

With this context established, please [your actual request for this session].
```
