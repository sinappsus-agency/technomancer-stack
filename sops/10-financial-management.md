# SOP 10 — Financial Management

**Category:** Finance + Operations
**Version:** 1.0
**Owner:** Studio Lead
**Trigger:** Invoice event OR monthly review date
**Frequency:** Per-project (invoicing) + monthly (review)

---

## Objective

Ensure all revenue is invoiced on time, all unpaid invoices are followed up systematically, and the studio has a clear financial picture reviewed once a month — without ad-hoc scrambling or chasing clients reactively.

---

## Prerequisites

- [ ] ERPNext set up with your services as items and your payment terms configured
- [ ] Stripe or bank EFT set up as accepted payment methods
- [ ] Invoice template approved and branded (ERPNext allows custom print formats)

---

## Part A — Invoice Creation and Dispatch

**Trigger:** Project milestone hit, retainer due date, or project complete

### Steps

**Step 1 — Create the invoice in ERPNext**
- Navigate: Accounting → Accounts Receivable → Sales Invoice
- Link the invoice to the client (Customer record)
- Add all deliverables as line items (use your service items list, not freetext)
- Set payment terms (Net 7 is recommended for project work, Net 30 for enterprise clients)
- Add your bank details or Stripe payment link to the invoice notes field

**Step 2 — PDF and dispatch**
- Generate and download PDF from ERPNext
- Send from your business email (not ERPNext's internal mailer unless SMTP is configured)
- Subject format: `Invoice [INV-YYYY-###] — [Client Name] — [Project or Month]`
- CC your accounts folder / email alias

**Step 3 — Log in CRM**
- Create an ERPNext Activity on the Customer record: "Invoice dispatched: [invoice number]"
- Set a follow-up reminder for Day 3 after due date

---

## Part B — Payment Follow-Up Sequence

Never chase informally. Always use this sequence. Copy templates exactly — they are calibrated for tone.

### Stage 1 — Due Date +3 (Friendly Reminder)

**Channel:** Email

**Subject:** Friendly reminder — Invoice [INV-YYYY-###]

```
Hi [Name],

Just a quick note to check in — Invoice [INV-YYYY-###] for [amount] was due on [date].

Please let me know if there are any questions or if you need the invoice resent.

Payment details: [bank / Stripe link]

Thanks,
[Your Name]
```

### Stage 2 — Due Date +7 (Direct Follow-Up)

**Channel:** Email + Slack DM (if you have a Slack channel with the client)

**Subject:** Invoice [INV-YYYY-###] — Following Up

```
Hi [Name],

Following up on Invoice [INV-YYYY-###] for [amount], now [X] days overdue.

If there's a hold-up on your end, please let me know and we can sort it out. Otherwise, I'd appreciate payment by [date = today + 3 days].

[Bank / Stripe link]

Let me know if you need anything from my side.

[Your Name]
```

### Stage 3 — Due Date +14 (Final Notice)

**Channel:** Email only. Formal tone. No Slack.

**Subject:** Final Notice — Invoice [INV-YYYY-###] — [Amount] Overdue

```
Hi [Name],

This is a formal notice that Invoice [INV-YYYY-###] for [amount] remains unpaid, now [X] days overdue.

Please arrange payment by [date = today + 5 days] to avoid work on any active projects being paused.

If you believe this invoice is in error, please contact me directly so we can resolve it immediately.

[Bank / Stripe link]

[Your Name]
```

⚠️ If no response after Stage 3: pause active work. Log the situation in ERPNext. Do not write off the debt without a formal process.

---

## Part C — Monthly Financial Review

**Trigger:** First working day of each month
**Duration:** 90 minutes

### Steps

**Step 1 — Accounts receivable aging report**
ERPNext: Accounting → Accounts Receivable Aged Summary

Review every outstanding invoice. Any over 30 days should be in the follow-up sequence above.

**Step 2 — Revenue against forecast**
Compare actual invoiced revenue for the previous month against the monthly target.
Record the delta in your planning tracker (see `months/holder.md` or your monthly file).

**Step 3 — Project-level profitability**
For each project invoiced last month:
- Estimated hours vs actual hours
- Estimated cost (subscriptions, contractors, ad spend) vs actual
- Was the project profitable? By what margin?

If a project made less than 60% margin, document why. If the same issue occurs twice, update your pricing or scope definition.

**Step 4 — Outstanding expenses**
Review any unpaid subscriptions, contractor invoices, or tool costs.
Ensure all are captured in ERPNext.

**Step 5 — 3-month cashflow projection**
Use current pipeline (ERPNext: CRM → Opportunities) to project likely revenue for the next 3 months.
Flag any months with projected gaps below your monthly floor (i.e., minimum revenue needed to cover overhead).

**Step 6 — Record in monthly file**
Record the following in `months/[month].md`:

```
## Financial Review — [Month] [Year]

Total invoiced: 
Total received:
Outstanding (overdue):
Current month target:
Variance:
Upcoming pipeline (3-month):
Notes:
```

---

## Tools Required

- ERPNext (invoicing, AR aging, CRM)
- Business email (dispatch + follow-up)
- Stripe (optional payment link)
- `months/[month].md` (monthly record)

---

## Failure Modes

**Failure: Invoice not sent until end of project**
This is a cash flow problem. Split payment on any project over 2 weeks: 50% upfront, 50% on delivery (or milestone-based). Update your proposal template to reflect this.

**Failure: Multiple clients in Stage 3 at the same time**
This indicates a client selection or contract problem, not a cash flow problem. Review your client qualification criteria in SOP 11.

**Failure: Monthly review not happening**
Block 90 minutes on the first Monday of each month in your calendar. Treat it as a client meeting. Non-negotiable.

---

## Output / Handoff

Monthly review complete when:
- [ ] AR Aged Summary reviewed and all overdue invoices in follow-up sequence
- [ ] Revenue vs forecast delta recorded
- [ ] Project profitability notes added for last month's completed projects
- [ ] 3-month projection updated
- [ ] Monthly financial summary added to `months/[month].md`
