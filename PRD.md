# Product Requirements Document
## Family Budget Assistant

**Document version:** 1.0  
**Date:** 2026-06-03  
**Status:** Draft — pending stakeholder sign-off  
**Audience:** Product, Design, Engineering, Stakeholders  
**Derived from:** requirements.md v1.0 + stakeholder clarification session (2026-06-03)

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Product Vision & Competitive Positioning](#2-product-vision--competitive-positioning)
3. [Business Success Metrics](#3-business-success-metrics)
4. [Personas & Key User Journeys](#4-personas--key-user-journeys)
5. [Technical Success Metrics](#6-technical-success-metrics)
6. [MVP Scope](#6-mvp-scope)
7. [Technical Considerations](#7-technical-considerations)
8. [UI Style & Design System Guidelines](#8-ui-style--design-system-guidelines)
9. [Corner Cases & Edge Conditions](#9-corner-cases--edge-conditions)
10. [Open Questions & Parking Lot](#10-open-questions--parking-lot)

---

## 1. Problem Statement

Modern households manage money across 3–8 financial accounts (checking, savings, 2–4 credit cards, a partner's accounts) spread across multiple institutions. No single tool addresses the full picture of *family* finances.

| Pain | Current State | Desired State |
|------|---------------|---------------|
| **Fragmented data** | Statements buried in email, bank portals, and separate card apps | One timeline of all household money |
| **Manual overhead** | Hours per month copy-pasting into spreadsheets | Upload file → review → done in under 30 min |
| **Individual-first tools** | Mint, YNAB, Copilot assume one person's finances | Shared household view with per-member tagging and shared goals |
| **Unrealistic budgets** | Families guess category limits with no data basis | AI-suggested budget grounded in 3–6 months of actual spending |
| **No conversational access** | Can't ask "are we on track for our vacation fund?" and get a real answer | Natural language Q&A over your own financial data |
| **Privacy anxiety** | Live bank API connections (Plaid) make privacy-conscious users uncomfortable | File-based import — no credentials ever stored or transmitted |
| **Late accountability** | Overspending visible only at month-end | Mid-month pacing alerts and budget status in plain English |

### The Gap in the Market

Mint shut down in January 2024, leaving millions of family-budget users without a home. YNAB addresses serious budgeters but is subscription-only, individual-first, and methodology-prescriptive. No mainstream product combines: (1) family-native shared finances, (2) privacy-safe file-based import, and (3) AI-powered conversational access to your own data. **The Family Budget Assistant is that combination.**

---

## 2. Product Vision & Competitive Positioning

### Vision Statement

> "The Family Budget Assistant is the first household finance tool that understands your whole family's money — not just one person's — and answers your questions in plain English, without ever requiring you to hand over your bank login."

### Competitive Moat (Three Pillars)

| Pillar | Why it matters | Closest competitor gap |
|--------|----------------|------------------------|
| **Family-native** | Models 2–8 members, shared goals, per-member spend attribution, household roles | All major tools are individual-first |
| **Privacy-safe** | File upload only in MVP; no Plaid/credential storage | Mint, Monarch, Copilot require live bank auth |
| **AI assistant** | Ask natural language questions; get answers grounded in your real data | No mainstream budgeting app has this |

### Budget Methodology

The app defaults to a **50/30/20 framework** (Needs / Wants / Savings) as an organizing principle, with user-editable **per-category spending caps** inside each bucket. This gives families a familiar mental model while preserving granular control.

---

## 3. Business Success Metrics

### 3.1 Acquisition & Activation

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Time to first useful dashboard (signup → 2 imports complete) | < 30 minutes | Measured per session |
| Week-1 activation rate (user completes onboarding + sets first budget) | ≥ 60% | 30 days post-launch |
| Signup-to-invite rate (household owner invites ≥ 1 member) | ≥ 35% | 60 days post-launch |

### 3.2 Engagement & Retention

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Monthly active users returning ≥ 2×/month to upload or review | ≥ 55% | 90 days post-launch |
| AI assistant queries per active user per month | ≥ 3 | 60 days post-launch |
| 90-day retention rate | ≥ 40% | 120 days post-launch |

### 3.3 Quality & Trust

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Budget realism NPS ("Does your budget feel realistic?") | ≥ 40 | 90-day in-app survey |
| Auto-categorization accuracy (no user correction needed) | ≥ 80% of transactions | 60 days post-launch |
| User-reported privacy confidence score | ≥ 4.2 / 5.0 | 90-day in-app survey |

### 3.4 Freemium Conversion

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Free-to-premium conversion rate | ≥ 5% | 6 months post-launch |
| Premium churn rate (monthly) | ≤ 3% | Ongoing |
| **Premium triggers:** History > 6 months, CSV/PDF export | — | — |

---

## 4. Personas & Key User Journeys

### Persona 1 — The Household CFO ("Morgan, 38")

**Profile:** Parent, manages all household bills and accounts. Has 1 checking, 1 savings, 2 credit cards, and a partner's credit card. Privacy-conscious — doesn't want to link bank APIs. Spends ~2 hours/month on finances manually today.

**Needs:** Import, categorize, set family budget, track actuals, get alerts, answer questions like "where did we overspend last month?"

**Key User Journey: Monthly Budget Review**

```
1. Downloads CSV statements from 3 institutions (~5 min)
2. Logs into app → uploads files per account
3. App shows import preview: 143 rows, 2 duplicates found, 8 uncategorized
4. Resolves duplicates (merge), quick-categorizes 8 transactions
5. Navigates to dashboard → sees month-to-date vs. budget pacing
6. Asks AI: "Why is dining over budget this month?"
7. AI responds: "You've spent $847 on dining vs. a $600 budget. 
   The difference is 4 restaurant visits between June 1–15. 
   At this pace, you'll end the month at ~$1,100."
8. Morgan adjusts next month's dining cap to $750
9. Shares summary view with partner (viewer role)
Total time: ~20 minutes
```

---

### Persona 2 — The Partner / Co-Parent ("Alex, 36")

**Profile:** Earns income, aware of household budget goals but not the one managing them. Wants visibility, not administrative work. Invited as editor.

**Needs:** See the shared dashboard, understand where family stands vs. budget, categorize own purchases, view goals progress.

**Key User Journey: Mid-Month Check-In**

```
1. Receives weekly email digest: "Groceries: 71% used (18 days left)"
2. Opens app on phone (mobile-responsive web)
3. Reviews dashboard: two categories in yellow (dining, entertainment)
4. Sees 3 uncategorized transactions tagged to them → categorizes in 2 taps
5. Asks AI: "Are we on track for the vacation fund this month?"
6. AI: "You've saved $320 toward your $500/month vacation goal — 
   64% with 40% of the month left. You're on track."
7. Alex shares screenshot with Morgan via text
```

---

### Persona 3 — The Budget-Skeptic New User ("Jamie, 42")

**Profile:** Has never tracked a budget before. Triggered by a "we need to figure out our money" moment (large unexpected expense). Not financially literate. Intimidated by spreadsheets.

**Needs:** Quick wins, no jargon, guided setup, simple answers, non-judgmental framing.

**Key User Journey: First-Time Onboarding**

```
1. Signs up with Google account (no password to create)
2. Onboarding wizard: "Tell us about your household" (2 adults, 1 kid)
3. Adds 2 accounts (Chase checking, Citi card) — no bank login required
4. Uploads last month's CSV from each
5. App auto-categorizes 87 of 102 transactions
6. Guided "review queue": 15 items needing a category — wizard 
   shows one at a time with suggested category
7. Budget wizard runs: "Based on your history, here's a suggested 
   50/30/20 budget for your household"
8. Jamie adjusts groceries ($600 → $700 "feels more real")
9. First dashboard visible: "You're currently on track in 4 of 5 categories"
10. Asks AI: "What does 'needs' mean?" 
    AI explains 50/30/20 in plain English with their own numbers
```

---

### Persona 4 — The Viewer (Teen or Non-Managing Partner)

**Phase 2 persona** — read-only access to limited household view. Not in MVP scope but informs data model decisions (member tagging, role permissions).

---

## 5. Technical Success Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Import throughput | 5,000 rows parsed in < 10 seconds | Async parsing with progress indicator |
| Dashboard load time | < 3 seconds (P95) on home broadband | Cached aggregates, lazy-load charts |
| AI query response time | < 4 seconds (P95) | OpenAI GPT-4o with streaming response |
| Duplicate detection accuracy | < 1% false positives | Same date + amount + description hash |
| Transfer mis-classification rate | < 2% | Credit card payment → checking shouldn't appear as expense |
| Auto-categorization accuracy | ≥ 80% high-confidence on first import | After 50 user corrections, rules cover ≥ 70% |
| Uptime (hosted MVP) | ≥ 99.5% monthly | Excludes scheduled maintenance |
| WCAG 2.1 AA compliance | Core flows (upload, review, budget, AI chat) | Tested with screen reader + automated lint |
| Auth token session expiry | 30-day sliding window, max 90 days hard expiry | Security posture for financial app |

---

## 6. MVP Scope

### 6.1 In Scope — MVP

| Area | Features |
|------|----------|
| **Auth** | Email + password registration; Google SSO; email verification; password reset |
| **Household setup** | Create household; invite members via email; roles: Owner, Editor, Viewer |
| **Account management** | Add/edit/delete accounts (checking, savings, credit card, cash); institution name, type, currency (USD) |
| **File import** | Upload CSV, OFX, QFX; column mapper (first import); save mapping per institution; import preview (row count, date range, errors); duplicate detection + merge/skip |
| **Transaction ledger** | Unified list: date, payee, amount, account, category, member, notes; bulk edit category/member; search + filter |
| **Categorization** | Family-oriented default category tree; add/edit/hide categories; auto-categorization rules; low-confidence review queue after import |
| **Income tracking** | Income detection (positive deposits, payroll descriptors); mark income sources; monthly income vs. expense summary (net cash flow) |
| **Budget planning** | Budget wizard (proposes 50/30/20 + per-category caps from historical median); user edits and saves monthly budget; pacing widget per category |
| **AI assistant** | Natural language Q&A over household transaction data; powered by OpenAI GPT-4o; context includes: transactions, budgets, goals |
| **Dashboard** | Home: net cash flow, month-to-date spend, budget pacing; category breakdown (bar/pie); cash flow chart (income vs. expenses by month); "Where did we overspend?" top-5 summary |
| **Alerts** | Import completed / failed (in-app); category over 90%/100% budget threshold (in-app + email) |
| **Freemium gating** | Full data visible for current + 5 prior months (free); beyond 6 months = premium prompt; CSV/PDF export = premium |

### 6.2 Out of Scope — MVP (Phased)

| Phase | Features |
|-------|---------|
| **Phase 2** | Recurring bill/subscription detection; split transactions; sinking funds / envelopes; PDF export (premium); improved ML categorization (learns from corrections); import history log; shared household notes |
| **Phase 3** | Live bank API (Plaid/Finicity) — opt-in; mobile-native app polish; allowance tracking for teens; multi-currency |
| **Phase 4** | Tax category summaries; net worth across investments; accountant export; multi-household (premium) |

### 6.3 MVP Acceptance Criteria

- [ ] User imports two different institution file types and sees a single chronological ledger
- [ ] Credit card payment from checking is classified as a transfer, not an expense
- [ ] User completes budget wizard and sees 50/30/20 bucket breakdown + per-category budget vs. actual
- [ ] AI assistant correctly answers at least 4 of 5 sample natural language financial questions against test data
- [ ] Household owner can invite a member with viewer role (read-only dashboard access)
- [ ] 6-month history limit triggers premium upsell prompt for free-tier users
- [ ] Export prompt appears (premium gate) when user attempts CSV download on free tier
- [ ] ≥ 70% of transactions auto-categorized after 50 user corrections (rule-based)
- [ ] WCAG 2.1 AA: import, review, budget, and AI chat flows pass automated + manual audit

---

## 7. Technical Considerations

### 7.1 Recommended Stack

| Layer | Recommendation | Rationale |
|-------|---------------|-----------|
| **Frontend** | React 18 + TypeScript + Tailwind CSS | Component ecosystem, type safety, utility-first CSS matches the "warm top / dense drill-down" UX pattern |
| **Charts** | Recharts or Nivo | Declarative, accessible, React-native |
| **Backend API** | Node.js (Express or Fastify) or Python (FastAPI) | Node: unified JS ecosystem; Python: stronger ML/parsing libs for CSV/OFX work |
| **Database** | PostgreSQL (primary) + Redis (caching/sessions) | Relational model fits transaction/budget structure; Redis for dashboard aggregates |
| **File parsing** | Python service (ofxparse, pandas) OR Node (ofx, csv-parser) | Python preferred if AI/ML processing is co-located |
| **AI Q&A** | OpenAI GPT-4o via function calling | Structured tool calls let the AI query transaction data programmatically rather than hallucinating |
| **Auth** | NextAuth.js (if Next.js) or Auth.js / Passport.js | Email + Google OAuth support out of the box |
| **Hosting** | Vercel (frontend) + Railway/Render or AWS (backend/DB) | Low ops overhead for MVP |
| **Storage** | S3-compatible (uploaded files, exports) | Encrypted at rest; files deleted after successful parse |

### 7.2 AI Assistant Architecture

The AI assistant should **NOT** receive raw transaction data in a context window. Instead:

```
User query → NLP intent classification
           → Tool call: query_transactions(filters, aggregations)
           → Tool call: get_budget_status(category, period)
           → Tool call: get_goal_progress(goal_id)
           → Compose natural language response from structured results
```

This approach:
- Keeps prompts token-efficient (structured data, not full CSV dumps)
- Prevents hallucination of transaction details
- Enables auditability (log what data was queried)
- Respects per-household data isolation

### 7.3 Security Requirements

- HTTPS everywhere; HSTS headers
- Encrypted data at rest (AES-256 or cloud-provider encryption)
- Passwords: bcrypt with cost factor ≥ 12
- Session tokens: HttpOnly, Secure, SameSite cookies
- No raw bank credentials stored or transmitted (file-only model)
- Uploaded files: stored temporarily during parse, then deleted from server
- Household data isolation: all queries scoped by `household_id` at ORM level
- Role enforcement: Owner/Editor/Viewer checked server-side on every mutation
- GDPR-style: export all data and delete account flows required at launch
- Rate limiting on AI Q&A endpoint (cost protection + abuse prevention)

### 7.4 Duplicate Detection

Duplicate detection key: `hash(date + amount + description_normalized + account_id)`

Edge cases to handle:
- Same transaction imported twice from different file exports (date range overlap)
- Pending → posted transaction (amount same, date shifts 1–2 days)
- Credit card payment appearing in both checking (debit) and card (credit) imports

### 7.5 CSV/OFX Parser Strategy

- Maintain a **template library** for top 10 US banks/cards (Chase, Bank of America, Citi, Wells Fargo, Discover, Capital One, American Express, USAA, Ally, Fidelity)
- Column mapper UI for unknown formats, with save-template capability
- OFX/QFX parsing is more standardized — prefer auto-detection over manual mapping

---

## 8. UI Style & Design System Guidelines

### 8.1 Design Philosophy: "Warm Surface, Dense Core"

The interface should feel **approachable and human at first glance** — calming, not intimidating — while allowing users who want to dig in to access full data density one level deeper.

| Layer | Principle | Example |
|-------|-----------|---------|
| **Home dashboard** | Summary cards, plain-English status, gentle colors | "Groceries: You're on track 🟢" not a wall of numbers |
| **Category drill-down** | Full transaction table, sortable, filterable | Click a category card → see every transaction |
| **AI assistant** | Conversational, non-jargon, uses family's actual numbers | Never says "YoY variance"; says "compared to last month" |
| **Import / review** | Guided, step-by-step, progress indicator | Never dumps 200 rows on the user without context |

### 8.2 Color Palette Direction

- **Primary:** Warm neutral base (off-white / warm gray backgrounds)
- **Accent:** One warm primary color (teal, sage green, or soft blue — not bank-blue)
- **Status colors:**
  - On track: soft green
  - Approaching limit (80–99%): amber/warm yellow
  - Over budget: warm red (not alarm-red — still calm)
- **Avoid:** Cold grays, hard white, finance-bro dashboard palettes

### 8.3 Typography

- Friendly sans-serif (Inter, DM Sans, or Plus Jakarta Sans)
- Large summary numbers (monetary amounts): medium weight, prominent
- Table data: regular weight, compact

### 8.4 Key UI Components

| Component | Notes |
|-----------|-------|
| **Pacing widget** | Horizontal bar: "Groceries: 62% used, 48% of month left" with color state |
| **AI chat panel** | Right-side drawer or bottom sheet (not full-page takeover) |
| **Import wizard** | Step progress bar: Upload → Map → Preview → Review → Done |
| **Budget wizard** | Slider-based category caps; 50/30/20 bucket totals update live |
| **Category card** | Summary on dashboard; click expands to inline transaction table |
| **Member tags** | Color-coded avatar chips on transactions |

### 8.5 Responsive Behavior

- Desktop-first for import and budget planning (file management is desktop behavior)
- Mobile-responsive for dashboard, AI chat, and quick transaction review
- Mobile-native app: Phase 3

---

## 9. Corner Cases & Edge Conditions

### 9.1 Import & Parsing

| Case | Handling |
|------|---------|
| CSV with no header row | Column mapper prompts user to label columns manually |
| Negative amounts for credits (Chase format) vs. positive (other banks) | Per-institution template flags debit/credit polarity |
| Credit card payment in checking export = debit; same payment in card export = credit | Transfer detection: same amount, opposite accounts, within 3 days → auto-link as transfer |
| Duplicate import of overlapping date range | Hash-based dedup: user sees "47 new, 12 duplicates skipped" in preview |
| OFX file with timezone-offset dates | Normalize all dates to UTC; display in user's local timezone |
| File with 0 transactions (empty statement period) | Show warning: "This file has no transactions for [date range]. Import anyway?" |
| Malformed CSV (encoding issues, extra commas) | Surface row-level errors in import preview; let user download error report |

### 9.2 Categorization

| Case | Handling |
|------|---------|
| Amazon transaction (could be groceries, clothing, electronics, or a gift) | Default → "Shopping (uncategorized)"; prompt user to confirm; rule creation available |
| Venmo / Zelle / PayPal payments (no merchant detail) | Mark as "Transfer / Person Payment" with review flag; user can add note |
| Refund appears as positive amount in expense account | Detect as "Refund/Adjustment" type; deducts from category spend for that month |
| Split paycheck into checking + savings from same employer | Income detection should count only checking deposit; savings = internal transfer |
| Joint paycheck in one partner's name but counts as household income | User manually marks as "Household Income" source |

### 9.3 Budget & AI Assistant

| Case | Handling |
|------|---------|
| User has < 1 month of data when running budget wizard | Show warning: "We recommend 3 months of data for accurate suggestions. Here's a starter budget you can edit." |
| AI query references future projections | AI clearly labels as "estimate based on current pace" — never presents forecast as fact |
| AI query asks for advice ("Should I cut my grocery budget?") | AI provides data context, does not make recommendations; includes disclaimer: "This is not financial advice" |
| User asks AI about a member's private spending | Viewer role cannot query another member's individual spending; Owner/Editor can query all |
| Budget sum > income | Budget wizard surfaces warning: "Your planned expenses ($4,200) + savings ($500) exceed your stated income ($4,000). You may want to adjust." |
| 50/30/20 bucketing edge cases (e.g., is a gym membership "Needs" or "Wants"?) | User can re-assign category → bucket; defaults provided but always editable |

### 9.4 Household & Multi-User

| Case | Handling |
|------|---------|
| Partner invited but never accepts | Invitation expires after 7 days; resend available; household works normally without them |
| Owner wants to remove a member | Owner can revoke access; member's tagged transactions remain in household ledger |
| Two owners (co-parents with equal access) | MVP: one Owner role. Phase 2: co-owner role or transfer ownership |
| Member uses a personal account they don't want to share fully | MVP: all accounts are household-scoped. Personal-only account view = Phase 2 feature |
| Household has no income (e.g., retired, supported by parent) | Income = $0 is valid; budget wizard operates on expense caps only; 50/30/20 shows as "not applicable" |

### 9.5 Freemium & Data

| Case | Handling |
|------|---------|
| Free user tries to view a 7-month-old transaction | Transaction row is blurred/locked with "Upgrade to view full history" inline prompt |
| Free user exports via browser "save as" workaround | File contents are within the visible 6-month window; no server-side bypass possible |
| User deletes account | All household data deleted within 30 days (GDPR-style); confirmation email sent; 7-day grace period with restore option |
| Premium subscription lapses | Data retained; UI reverts to free tier (older than 6 months grayed out); no data deleted |

---

## 10. Open Questions & Parking Lot

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | What is the monthly/annual price point for premium? | Product / Business | Open |
| 2 | Should the AI assistant be available on the free tier with a query limit (e.g., 5/month)? | Product | Open |
| 3 | Should import templates from the community be shareable (e.g., "Chase Sapphire CSV format")? | Product / Eng | Phase 2 consideration |
| 4 | Joint accounts held by both partners — model as one shared account or two linked views? | Product / Design | Open |
| 5 | Kids' privacy: at what age does a child's spending become visible to them vs. parents only? | Product / Legal | Phase 3 |
| 6 | "Financial advice" liability language — needs legal review before launch | Legal | Pre-launch blocker |
| 7 | Accessibility: is WCAG 2.1 AA sufficient or is AA+ / Section 508 required (if targeting US gov employees)? | Legal / Product | Open |

---

## Appendix A — Phased Roadmap Summary

| Phase | Key Deliverables | When |
|-------|-----------------|------|
| **MVP** | Auth, household, file import, ledger, categories, income detection, budget wizard (50/30/20), AI Q&A, dashboard, pacing, freemium gates | Launch |
| **Phase 2** | Recurring detection, split transactions, sinking funds, PDF export, ML categorization, import history, shared notes | 3–6 months post-launch |
| **Phase 3** | Optional Plaid API, mobile polish, teen allowances, multi-currency | 6–12 months |
| **Phase 4** | Tax summaries, net worth, investment import, multi-household premium | 12–18 months |

---

## Appendix B — Definition of "Good Budget" (Product Standard)

A budget in this product is considered **good** if it meets four criteria:

1. **Realistic** — grounded in ≥ 3 months of actual spending, not aspirational guesses
2. **Complete** — all major household expense categories are represented
3. **Balanced** — income ≥ planned expenses + savings goal (wizard enforces this check)
4. **Agreed** — visible to all household members; revisable each month without friction

The app guides families toward this standard. It never changes budget numbers without explicit user confirmation.

---

*Document owner: [Product Manager name TBD]*  
*Next review: 2026-07-01 (or before technical design begins)*
