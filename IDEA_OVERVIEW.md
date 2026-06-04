# Idea Overview — Family Budget Assistant

**Product:** Family Budget Assistant  
**Date:** 2026-06-04  
**Status:** MVP in development  
**One-liner:** The first household finance tool that understands your whole family's money — not just one person's — and answers your questions in plain English, without ever requiring you to hand over your bank login.

---

## ☑️ Target Customer

### Primary Persona — "The Household CFO" (Morgan, 38)

A parent who manages all household bills, accounts, and financial planning. Holds 1 checking, 1 savings, 2+ credit cards, plus a partner's accounts across multiple banks. Privacy-conscious — avoids linking bank APIs. Spends ~2 hours/month manually consolidating finances in spreadsheets. Needs a tool that handles the whole household, not just their own accounts.

### Secondary Segments

| Segment | Profile | Acquisition Path |
|---------|---------|-----------------|
| **Partner / Co-Parent** | Earns income, wants visibility not admin work | Household invite from primary user |
| **Mint Refugees** | Former free Mint users (Mint shut down Jan 2024) seeking a replacement without data selling | "Mint alternative" SEO, comparison content |
| **Budget-Skeptic New User** | Triggered by financial stress; intimidated by spreadsheets | Reddit r/personalfinance, content SEO |
| **Privacy-First Professionals** | Tech, healthcare, legal — high trust bar for financial data | HN, Product Hunt, privacy forums |

### Ideal Customer Profile (ICP)

- **Household size:** 2–4 adults
- **Accounts:** 3–8 across 2+ institutions
- **Income:** $75K–$250K household
- **Geography:** US-first (MVP)
- **Behavior:** Already downloads bank statements monthly; uses or has abandoned spreadsheets

### Market Size (Illustrative)

| Layer | Estimate | Basis |
|-------|----------|-------|
| **TAM** | ~45M US households with 2+ income earners | Census data |
| **SAM** | ~12M actively budgeting households | Mint peak ~20M; ~60% budget-conscious |
| **SOM (Year 3)** | 50K–150K paying households | 0.4–1.2% of SAM at $8–12/mo |

---

## ☑️ Customer Pain Points and Challenges

| Pain Point | Current State | Emotional Cost |
|------------|---------------|----------------|
| **Fragmented data** | Statements scattered across email, bank portals, and separate card apps | Anxiety — "I don't know where we stand" |
| **Manual overhead** | Copy-pasting into spreadsheets for 2+ hours every month | Frustration; abandoned after 2–3 months |
| **Individual-first tools** | Mint, YNAB, Copilot assume one person's finances — not a household | Partners feel excluded; single-user churn |
| **Unrealistic budgets** | Families guess category limits with no data basis | Shame when budgets fail by week 2 |
| **No conversational access** | Can't ask "are we on track for vacation?" and get a real answer | Cognitive load to interpret charts |
| **Privacy anxiety** | Live bank API connections (Plaid) feel risky | 30–40% drop-off at the bank-link step (industry est.) |
| **Late accountability** | Overspending only visible at month-end | Reactive vs. proactive; partner conflict |
| **Double-counting** | Credit card payments counted as expenses in both accounts | Inflated spend figures; broken budgets |

### Jobs-to-be-Done

1. **Consolidate** — "Show me all our money in one place."
2. **Understand** — "Where did it go, and who spent it?"
3. **Plan** — "Help us set a budget we can actually stick to."
4. **Monitor** — "Tell us before we blow dining, not after."
5. **Align** — "Get my partner on the same page without a finance meeting."

---

## ☑️ How We Plan to Solve the Problem

### User Flow

```
Download statements → Upload files → Review & categorize → Budget wizard → Dashboard + AI Q&A
        ↓                  ↓                ↓                    ↓              ↓
   5 min/account      No credentials    80% auto-tagged    50/30/20 from    "Why is dining
                      Files deleted      Review queue        real history      over budget?"
                      after parse        for the rest
```

### Solution by Pain Point

| Problem | Our Solution |
|---------|--------------|
| Fragmented data | Unified ledger across all accounts; transfer detection prevents double-counting |
| Manual overhead | CSV/OFX/QFX import + saved column mappings + dedup → monthly ritual in ~20 min |
| Individual-first tools | Household workspace with Owner/Editor/Viewer roles and per-member transaction tags |
| Unrealistic budgets | Budget wizard using 3–6 month median spend + 50/30/20 (Needs/Wants/Savings) framing |
| No conversational Q&A | AI assistant with function calling over structured DB queries — answers use real numbers |
| Privacy anxiety | File-only import; no credentials stored or transmitted; files deleted after parse |
| Late alerts | Mid-month pacing widgets + email alerts at 90%/100% of budget thresholds |

### Three-Pillar Competitive Moat

| Pillar | Why It Matters |
|--------|----------------|
| **Family-native** | 2–8 members, shared goals, per-member spend attribution, household roles — no competitor offers this natively |
| **Privacy-safe import** | File upload only in MVP — no Plaid, no credential storage; the segment that drops off at bank-link steps comes to us |
| **AI assistant** | Natural language Q&A via structured tool calls over real household data — not generic chatbot advice |

### AI Design (Anti-Hallucination)

The assistant uses function calling, not raw data dumps:

- `get_spending_summary(period, category, member)`
- `get_budget_status(period, category)`
- `get_transactions(filters)`
- `get_goal_progress(goal_id)`
- `get_cash_flow(months)`

This keeps token costs low (~$0.01–0.05/query), prevents invented transactions, and enables audit logging.

---

## ☑️ Key Features

### MVP (In Scope)

| Area | Features |
|------|----------|
| **Auth & Household** | Email/password + Google SSO; create household; invite members (Owner / Editor / Viewer roles) |
| **Accounts** | Checking, savings, credit card, cash; institution nickname; multi-account household view |
| **File Import** | CSV, OFX, QFX upload; column mapper; saved institution templates; preview + duplicate detection |
| **Transaction Ledger** | Unified timeline; bulk edit; search/filter; member tags; credit card transfer pairing |
| **Categorization** | Family-oriented category tree; rules engine; review queue for low-confidence transactions |
| **Income Tracking** | Payroll detection; income vs. expense separation; net cash flow |
| **Budget Planning** | Wizard (50/30/20 + per-category caps derived from real history); pacing widgets |
| **AI Assistant** | Natural language Q&A over transactions, budgets, and goals; powered by GPT-4o + function calling |
| **Dashboard** | Net cash flow card, MTD spend, budget pacing bars, category breakdown, monthly cash flow chart |
| **Alerts** | Import status; category at 90% and 100% threshold (in-app + email) |
| **Freemium Gate** | 6 months history free; premium for full history + CSV/PDF export |

### Phase 2+ Roadmap

- Recurring bill / subscription detection
- Split transactions
- Sinking funds / envelope budgeting
- ML categorization that learns from household corrections (opt-in)
- Optional Plaid bank link (opt-in only — does not replace file import)
- Teen allowances, multi-currency support, tax summary reports

---

## ☑️ Competitors in the Market

### Competitive Matrix

| Competitor | Price | Bank Sync Required | Household Sharing | AI Q&A | File Import | Privacy (No Credentials) |
|------------|-------|--------------------|-------------------|--------|-------------|--------------------------|
| **Family Budget Assistant** | Freemium | Phase 3 opt-in | ✅ Native (roles) | ✅ Grounded NL Q&A | ✅ Primary path | ✅ MVP default |
| **Monarch Money** | $99.99/yr | ✅ Required | ✅ Couples view | ❌ Insights only | ❌ | ❌ |
| **YNAB** | $109/yr | ✅ Required | ⚠️ Shared budget, not household-native | ❌ | ❌ | ❌ |
| **Copilot** | ~$95/yr | ✅ Required | ❌ No sharing | ⚠️ Categorization AI only | ❌ | ❌ |
| **Empower (Personal Capital)** | Free | ✅ Required | ❌ | ❌ | ❌ | ❌ |
| **Rocket Money** | Freemium | ✅ Required | ❌ | ❌ | ❌ | ❌ |
| **Goodbudget** | Free / $8/mo | ❌ Manual only | ⚠️ Limited | ❌ | ⚠️ Manual entry | ✅ |
| **Spreadsheets** | Free | N/A | ⚠️ DIY sharing | ❌ | ✅ | ✅ |
| **Mint (defunct Jan 2024)** | Was free | ✅ | ⚠️ Individual | ❌ | ❌ | ❌ |

### Positioning Map

```
                    HIGH AUTOMATION (Import + AI)
                              │
                    Copilot   │   ★ Family Budget Assistant
                              │
         ─────────────────────┼─────────────────────────────
         INDIVIDUAL-FIRST     │       HOUSEHOLD-NATIVE
                              │
                    YNAB      │   Monarch
                              │
                    LOW AUTOMATION / MANUAL
```

**Our white space:** Upper-right quadrant — the only player that is household-native AND offers high automation AND does not require credentials.

### Key Competitor Gaps We Exploit

| Competitor | Their Gap | Our Wedge |
|------------|-----------|-----------|
| **Monarch** | Requires Plaid; no conversational AI; individual transaction philosophy | Privacy-first file import + AI Q&A + deeper family model |
| **YNAB** | Zero-based methodology is prescriptive; steep learning curve; no AI; requires bank link | Flexible 50/30/20; faster time-to-value; ask questions, don't read charts |
| **Copilot** | iOS/Mac only; no household sharing; no budget Q&A | Cross-platform; family-native; conversational layer |
| **Goodbudget** | Manual entry; no import automation; no AI | Automated import + categorization + AI at the same privacy posture |

---

## ☑️ Existing Data and Models (Fine-Tuning vs. Starting from Scratch)

**Short answer: Do not start from scratch.** Use a hybrid stack — pre-trained open models + open datasets for categorization; foundation LLMs (GPT-4o / Gemini) with function calling for Q&A. Fine-tune only where ROI is clear.

### Layer 1 — Transaction Categorization

| Resource | What It Provides | How We Use It |
|----------|-----------------|---------------|
| **[DoDataThings/us-bank-transaction-categories-v2](https://huggingface.co/datasets/DoDataThings/us-bank-transaction-categories-v2)** (Hugging Face) | 68K synthetic US bank strings across 17 categories; Chase, Apple Card, PayPal formats | Fine-tune DistilBERT classifier — pre-trained model available at 99.9% val accuracy |
| **[mitulshah/transaction-categorization](https://huggingface.co/datasets/mitulshah/transaction-categorization)** (Hugging Face) | 4.5M+ synthetic transactions, 10 categories, 5 countries | Pre-training / category taxonomy benchmarking |
| **[utkarshugale/BusinessTransactions](https://huggingface.co/datasets/utkarshugale/BusinessTransactions)** (Hugging Face) | Foursquare merchant names → realistic transaction strings | Merchant normalization training |
| **[d-daemon/transaction-enrichment-ml](https://github.com/d-daemon/transaction-enrichment-ml)** (GitHub) | End-to-end pipeline: char n-gram TF-IDF + Logistic Regression | Lightweight production baseline — no GPU required |
| **MCC (Merchant Category Codes)** | ISO 18245 standard merchant codes | Feature enrichment where available in parsed files |

**Recommended MVP path:**
1. **Rules engine first** (regex pattern → category) — ships in MVP, learns from user corrections
2. **Fine-tuned DistilBERT** on `us-bank-transaction-categories-v2` for high-confidence auto-tagging
3. **Review queue** for confidence < 0.85 — human-in-the-loop continuously improves the rules

### Layer 2 — AI Budget Assistant (MVP)

| Resource | What It Provides | How We Use It |
|----------|-----------------|---------------|
| **OpenAI GPT-4o** | Function calling, natural language generation | System prompt + custom tool definitions — **no fine-tuning needed for MVP** |
| **Google Gemini 1.5 Flash** | Faster / cheaper alternative | Fallback or cost optimization |
| **Structured tool layer (our IP)** | `get_budget_status`, `get_transactions`, `get_goal_progress` etc. | Prevents hallucination; grounded answers from real DB queries |

**Why not fine-tune the LLM:** Function calling + structured DB queries achieves grounding without custom training. Fine-tuning adds cost, latency, and compliance complexity for marginal gain at MVP stage.

### Layer 3 — Budget Recommendation Engine

| Approach | Data Source | Notes |
|----------|-------------|-------|
| **Median/trimmed mean** per category | User's own 3–6 months history | No external model needed; grounded in their data |
| **50/30/20 bucketing** | Elizabeth Warren framework | Informational framing, not ML |
| **Outlier detection** (Phase 2) | Statistical IQR on user history | Flag one-time medical/travel spikes |

### Layer 4 — Bank File Parsing

| Resource | What It Provides | How We Use It |
|----------|-----------------|---------------|
| **Institution template library** | Column mappings for top 10 US banks (Chase, BofA, Citi, Wells Fargo, etc.) | Rule-based; community templates in Phase 2 |
| **ofxparse / ofx-js** | OFX/QFX standard parsing | Open-source; no training needed |

### Data Strategy Summary

```
MVP  (no training from scratch)
 ├── Categorization:  Rules + optional pre-trained DistilBERT
 ├── AI Q&A:          GPT-4o/Gemini + function calling (no fine-tune)
 ├── Budget wizard:   Statistical median on user's own history
 └── File parsing:    Institution templates + open-source OFX/CSV libs

Phase 2  (targeted fine-tuning)
 ├── Fine-tune classifier on anonymized user corrections (opt-in)
 ├── Merchant normalization model (Foursquare + user data)
 └── Recurring detection: heuristic → lightweight ML

Phase 3+  (optional)
 ├── Household-specific embedding cache for repeat merchants
 └── Fine-tuned small LLM for offline/local-first AI (privacy+)
```

### Privacy & Compliance for Training Data

- **Never** train on raw user data without explicit opt-in
- Synthetic Hugging Face datasets avoid PII entirely for initial models
- User correction feedback → aggregated, anonymized patterns only
- GDPR-style export/delete must be in place before any ML pipeline touches household data

---

*Related documents: [PRD.md](PRD.md) · [VC_PITCH_AND_COMPETITIVE_ANALYSIS.md](VC_PITCH_AND_COMPETITIVE_ANALYSIS.md) · [ARCHITECTURE.md](ARCHITECTURE.md)*
