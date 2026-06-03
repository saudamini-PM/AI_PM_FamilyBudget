# Family Budget Planner & Tracker — High-Level Requirements

**Document version:** 1.0 (draft)  
**Audience:** Product, design, and engineering  
**Primary persona:** Household manager (e.g., parent coordinating family finances)

---

## 1. Executive summary

A **web-based personal budget planner and tracker** for multi-member households. Users import **downloaded statements** from banks and credit cards (CSV, OFX/QFX, etc.), and the system **normalizes transactions**, separates **income vs. expenses**, and supports a **family budget** with goals, limits, and simple guidance—not only charts.

**Core value:** One place to see “where our money went,” agree on a realistic budget, and track progress month to month without manual spreadsheet work for every account.

---

## 2. Problem statement

| Pain | Today | Desired state |
|------|--------|----------------|
| Fragmented data | Statements in email, bank sites, multiple cards | Single timeline of household money |
| Time cost | Manual copy/paste into spreadsheets | Import files → review → done |
| Family context | Personal finance tools assume one person | Shared household view with optional per-person splits |
| Budget realism | Guessing category limits | Data-informed suggestions + editable family plan |
| Accountability | Hard to see overspending until too late | Alerts, pacing (“on track / over”), simple reports |

---

## 3. Goals and success metrics

### 3.1 Product goals

1. **Consolidate** income and spending from multiple institutions via file upload.
2. **Classify** transactions consistently (groceries, kids activities, utilities, etc.).
3. **Recommend** a starter family budget from historical spending, then let the user adjust.
4. **Track** actuals vs. budget by category and time period (weekly/monthly).
5. **Support household planning** (shared goals, allowances, recurring bills).

### 3.2 Success metrics (examples)

- Time to first useful dashboard after signup: **< 30 minutes** (with 2+ imports).
- **≥ 80%** of imported transactions auto-categorized with high confidence; remainder quick to fix.
- User returns **≥ 2× per month** to upload new files or review budget pacing.
- User reports budget feels **“realistic”** (in-app survey or NPS after 90 days).

---

## 4. Target users and personas

### 4.1 Primary persona — **Household CFO (Mom/Dad/Partner)**

- Manages bills, knows who spends on what.
- Wants clarity, not day-trading complexity.
- Privacy-conscious; may not want to link live bank APIs initially.
- Needs: import, categorize, family budget, alerts, printable/simple reports.

### 4.2 Secondary personas

| Persona | Needs |
|---------|--------|
| **Partner / co-parent** | Read-only or limited edit; shared visibility on budget vs. actuals |
| **Teen / adult child** | Optional sub-profile: allowance, personal spending bucket (phase 2+) |
| **Accountant / tax prep** | Export categorized annual summary (phase 2+) |

### 4.3 Household model

- **One household** = one budget workspace.
- **Members** (2–8 typical): name, role (adult/teen/child), optional default card/account tags.
- Transactions may be tagged **household** vs. **member** vs. **shared goal** (e.g., vacation fund).

---

## 5. Scope

### 5.1 In scope (MVP)

- Web app (responsive; desktop-first for import/review).
- **Manual file upload** (no live bank aggregation required for MVP).
- Transaction ledger, categories, rules, monthly budget.
- Income detection and recurring bill identification (heuristic).
- Budget recommendation engine based on trailing 3–6 months.
- Dashboards: cash flow, category spend, budget vs. actual.
- Basic alerts (email or in-app): over budget, large transaction, import errors.

### 5.2 Out of scope (MVP) — future phases

- Live Plaid/finicity bank connections (optional later).
- Investment portfolio tracking, tax filing, bill pay.
- Cryptocurrency, business P&L, multi-currency (unless stated).
- Mobile native apps (responsive web OK for MVP).

---

## 6. Functional requirements

### 6.1 Account and institution management

| ID | Requirement | Priority |
|----|-------------|----------|
| ACC-01 | User can create a household and invite members (email invite, role: owner/editor/viewer). | P1 |
| ACC-02 | User can register **accounts**: checking, savings, credit card, cash (manual). | P1 |
| ACC-03 | Each account has: institution name, account nickname, type, currency (USD default), last import date. | P1 |
| ACC-04 | Support **multiple files per account** over time; detect duplicates on re-import. | P1 |

### 6.2 File import and parsing

| ID | Requirement | Priority |
|----|-------------|----------|
| IMP-01 | Upload **CSV, OFX, QFX** (and institution-specific CSV templates where documented). | P1 |
| IMP-02 | Map columns on first import (date, description, amount, debit/credit); save mapping per institution template. | P1 |
| IMP-03 | Parse credit card vs. bank semantics (payments to card = transfer, not expense). | P1 |
| IMP-04 | **Duplicate detection**: same date, amount, description hash; user can merge or skip. | P1 |
| IMP-05 | Import preview: row count, date range, errors, warnings before commit. | P1 |
| IMP-06 | Import history log (who uploaded, when, file name, rows added/skipped). | P2 |
| IMP-07 | Scheduled reminder: “Upload March statements” (optional). | P3 |

**Assumption:** Users download files from bank/CC sites; app does not scrape institutions.

### 6.3 Transaction model and ledger

| ID | Requirement | Priority |
|----|-------------|----------|
| TXN-01 | Unified transaction list: date, payee/description, amount, account, category, member, notes, tags. | P1 |
| TXN-02 | Transaction types: **expense**, **income**, **transfer** (between own accounts), **refund/adjustment**. | P1 |
| TXN-03 | Split transactions (e.g., Costco: groceries + household). | P2 |
| TXN-04 | Bulk edit: category, member, tag for selected rows. | P1 |
| TXN-05 | Search and filter by date, account, category, amount range, text. | P1 |
| TXN-06 | Mark transactions **pending review** vs. **confirmed**. | P2 |

### 6.4 Categorization

| ID | Requirement | Priority |
|----|-------------|----------|
| CAT-01 | Default **family-oriented category tree** (housing, utilities, groceries, dining, kids—school/activities/clothing, transport, healthcare, subscriptions, gifts, personal care, savings, debt payment, etc.). | P1 |
| CAT-02 | User can add/edit/hide categories and subcategories. | P1 |
| CAT-03 | **Auto-categorization rules**: if description contains X → category Y (per account optional). | P1 |
| CAT-04 | Learn from user corrections (suggest same category next time). | P2 |
| CAT-05 | Flag **uncategorized** and **low-confidence** in review queue after import. | P1 |

### 6.5 Income tracking

| ID | Requirement | Priority |
|----|-------------|----------|
| INC-01 | Detect likely **income** (payroll descriptors, regular deposits, positive amounts on checking). | P1 |
| INC-02 | User can mark income sources: salary A, salary B, side gig, benefits, transfers in (exclude internal transfers). | P1 |
| INC-03 | Monthly **income summary** vs. expenses (net cash flow). | P1 |
| INC-04 | Optional: expected income schedule (biweekly/monthly) for forecast. | P2 |

### 6.6 Expense analysis and recurring items

| ID | Requirement | Priority |
|----|-------------|----------|
| EXP-01 | Monthly and rolling 3/6/12-month spend by category. | P1 |
| EXP-02 | Detect **recurring** subscriptions and bills (amount + interval heuristic). | P2 |
| EXP-03 | Identify **large one-offs** (medical, travel) so they don’t distort “normal month” budget suggestions. | P2 |
| EXP-04 | Optional merchant normalization (“AMZN MKTP” → Amazon). | P2 |

### 6.7 Budget planning and “good budget” guidance

| ID | Requirement | Priority |
|----|-------------|----------|
| BUD-01 | **Budget wizard**: after enough history, propose monthly limits per category from median/trimmed average spend. | P1 |
| BUD-02 | Show **benchmark framing** (informational only): e.g., 50/30/20-style buckets (needs/wants/savings) applied to *their* categories—editable disclaimers, not financial advice. | P2 |
| BUD-03 | User sets **monthly budget** per category; optional annual goals (vacation, emergency fund contribution). | P1 |
| BUD-04 | **Envelope / target** optional: sinking funds (car repair, holidays, back-to-school). | P2 |
| BUD-05 | **Pacing widget**: “Groceries: 62% of budget with 48% of month left” (green/yellow/red). | P1 |
| BUD-06 | Scenario: “If we cut dining by $200, where does it go?” (slider or reallocate). | P3 |
| BUD-07 | **Family goals** page: agreed priorities (pay debt, save $X, cap kids activities). | P2 |

**Definition of “good budget” for this product:**  
Realistic (grounded in actuals), complete (all major categories), balanced (income ≥ planned expenses + savings), and agreed (visible to household, revisable monthly).

### 6.8 Household-specific features

| ID | Requirement | Priority |
|----|-------------|----------|
| HH-01 | Tag spend by **member** or “shared” without requiring separate bank logins. | P1 |
| HH-02 | **Kids / activities** category group with sub-tags (sports, music, school fees). | P1 |
| HH-03 | Optional **allowance tracking** (not full kid banking—ledger only). | P3 |
| HH-04 | Shared notes on month (“March: camp deposit + car insurance”). | P2 |

### 6.9 Reporting and dashboards

| ID | Requirement | Priority |
|----|-------------|----------|
| RPT-01 | **Home dashboard**: net worth snapshot (accounts balances if captured), month-to-date spend, budget status. | P1 |
| RPT-02 | Category breakdown (pie/bar), trend lines MoM. | P1 |
| RPT-03 | **Cash flow** chart: income vs. expenses by month. | P1 |
| RPT-04 | Export CSV/PDF for month or year (categories + totals). | P2 |
| RPT-05 | “Where did we overspend last month?” summary with top 5 merchants. | P1 |

### 6.10 Notifications

| ID | Requirement | Priority |
|----|-------------|----------|
| NTF-01 | Category over budget threshold (e.g., 90%, 100%). | P2 |
| NTF-02 | Import completed / import failed. | P1 |
| NTF-03 | Unreviewed transactions > N days after import. | P2 |

---

## 7. Non-functional requirements

| Area | Requirement |
|------|-------------|
| **Security** | HTTPS, encrypted data at rest, hashed passwords, session timeout; no storage of full bank login credentials in MVP. |
| **Privacy** | Household data isolated; role-based access; clear data export/delete (GDPR-style). |
| **Performance** | Import 5k rows in < 10s; dashboard loads < 3s on typical home broadband. |
| **Availability** | Target 99.5% for hosted MVP (if cloud). |
| **Accessibility** | WCAG 2.1 AA for core flows (upload, review, budget view). |
| **Browser support** | Latest Chrome, Safari, Firefox, Edge (last 2 versions). |
| **Data retention** | User-configurable; default retain all history. |

---

## 8. High-level data model (conceptual)

```
Household
  ├── Members (role, display name)
  ├── Accounts (institution, type)
  │     └── ImportBatches (file metadata, parse status)
  ├── Transactions (amount, date, type, category, member, account, splits)
  ├── Categories (tree, budget flags)
  ├── Rules (pattern → category/member)
  ├── BudgetPeriods (month, category limits, goals)
  └── Alerts / AuditLog
```

**Key relationships:**

- Transaction belongs to one Account and one Household.
- Transfers link two Transactions (or one transfer record with from/to account).
- BudgetPeriod has many BudgetLines (category + amount).

---

## 9. Key user flows

### 9.1 Onboarding

1. Sign up → create household → add members (optional).
2. Add accounts (nickname + type).
3. Upload first statement → map columns → preview → import.
4. Review uncategorized queue → confirm categories.
5. Run budget wizard → adjust proposed limits → save monthly budget.

### 9.2 Monthly rhythm (target habit)

1. Download new CSV/OFX from each bank/card.
2. Upload per account → resolve duplicates → review new merchants.
3. Check dashboard pacing mid-month.
4. End of month: budget vs. actual report → adjust next month’s budget.

### 9.3 Partner view

1. Invited as viewer/editor.
2. Sees same dashboard; editor can categorize; viewer read-only.

---

## 10. Budget recommendation logic (high level)

**Inputs:** 3–6 months categorized expenses; flagged one-time outliers; stated income.

**Outputs:**

- Proposed category caps = trimmed mean or median per category.
- Minimum savings line = user target or % of income (configurable).
- Warning if sum(expense budgets) + savings > income.
- Suggestions list: “Top 3 discretionary categories above peer baseline” (optional, phase 2).

**User always approves** final numbers; system never auto-changes budget without confirmation.

---

## 11. MVP vs. phased roadmap

| Phase | Focus |
|-------|--------|
| **MVP** | Upload, ledger, categories/rules, income vs. expense, budget wizard, pacing dashboard, one household, 2 roles |
| **Phase 2** | Recurring detection, splits, sinking funds, PDF export, improved ML categorization |
| **Phase 3** | Optional bank link API, mobile polish, allowances, multi-currency |
| **Phase 4** | Tax summaries, net worth tracking across investments |

---

## 12. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Inconsistent bank CSV formats | Template library + column mapper + community templates |
| Double-counting credit card payments | Transfer detection rules between paired accounts |
| User abandons after tedious categorization | Strong defaults, rules, bulk edit, review queue only for low confidence |
| Privacy trust | File-based import first; clear security page; local export anytime |
| “Financial advice” liability | Educational framing; disclaimers; user-owned decisions |

---

## 13. Open questions (for stakeholder review)

1. **Authentication:** Email/password only, or Google/Apple SSO for family invites?
2. **Monetization:** Free for household, freemium (export/history limits), or subscription?
3. **Default budget method:** Strict monthly caps vs. flexible weekly envelopes?
4. **Joint vs. separate accounts:** Model partner’s premarital account as household or personal?
5. **Supported countries:** US-only formats first?
6. **Kids’ privacy:** Age threshold before member-level tagging is hidden from children?

---

## 14. Acceptance criteria (MVP release)

- [ ] User can import two different institution file types and see a single chronological ledger.
- [ ] Credit card payment from checking is classified as transfer, not double expense.
- [ ] User completes budget wizard and sees budget vs. actual for current month.
- [ ] ≥ 70% of transactions categorized automatically after 50 user corrections (rules).
- [ ] Household owner can invite one member with viewer role.
- [ ] User can export transaction list with categories for a date range.

---

## 15. Suggested next steps

1. Validate **category tree** and **monthly ritual** with 3–5 families (interviews).
2. Collect **sample CSV/OFX files** (anonymized) from top 10 banks/cards for parser specs.
3. Wireframe **dashboard**, **import preview**, and **budget wizard**.
4. Technical spike: duplicate detection + transfer pairing accuracy.
