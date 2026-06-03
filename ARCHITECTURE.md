# Architecture Design & Implementation Plan
## Family Budget Assistant

**Document version:** 1.0  
**Date:** 2026-06-03  
**Constraint:** Local deployment only — no cloud infrastructure. Fully functional with live AI API connections.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Tech Stack & Rationale](#2-tech-stack--rationale)
3. [Architecture Diagram](#3-architecture-diagram)
4. [Data Models](#4-data-models)
5. [API Design](#5-api-design)
6. [AI Integration Architecture](#6-ai-integration-architecture)
7. [Security Design](#7-security-design)
8. [Performance Design](#8-performance-design)
9. [Scalability Considerations](#9-scalability-considerations)
10. [Implementation Plan](#10-implementation-plan)
11. [Local Development Setup](#11-local-development-setup)

---

## 1. System Overview

The Family Budget Assistant is a **locally-hosted full-stack web application** with three core processing concerns:

| Concern | What it does |
|---------|-------------|
| **File ingestion** | Accepts CSV/OFX bank exports, normalises them into a unified transaction ledger |
| **Budget intelligence** | Categorises, aggregates, and tracks actuals vs. budget limits |
| **AI Q&A** | Accepts natural-language questions and answers them using structured queries over real household data via OpenAI function calling |

Because the app runs locally, there is no CDN, no object storage, no managed cloud database. Every layer — frontend, backend, database — runs as a local process. The AI calls out to the OpenAI API over the internet; everything else stays on-device.

---

## 2. Tech Stack & Rationale

### 2.1 Frontend

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | **React 18 + TypeScript** | Component ecosystem, strict typing catches data-model mismatches early |
| Build tool | **Vite** | Fast HMR for local dev; no CRA bloat |
| Styling | **Tailwind CSS** | Utility-first matches the Option 3 design system; no runtime CSS-in-JS overhead |
| Server state | **TanStack Query (React Query)** | Intelligent caching of dashboard aggregates; automatic background refetch |
| Client state | **Zustand** | Lightweight global state for auth session, UI state |
| Charts | **Recharts** | Declarative, accessible, React-native; good fit for budget bars and cash flow |
| Forms | **React Hook Form + Zod** | Schema-validated forms; Zod schemas can be shared with the backend |

### 2.2 Backend

| Layer | Choice | Why |
|-------|--------|-----|
| Runtime | **Node.js 20 + TypeScript** | Unified JS/TS ecosystem; share Zod schemas and types between frontend and backend |
| Framework | **Express.js** | Minimal, well-understood, easy to layer middleware onto |
| ORM | **Prisma** | Type-safe queries, auto-generated migrations, works perfectly with local PostgreSQL |
| File parsing | **csv-parse** (CSV) + **ofx-js** (OFX/QFX) | Battle-tested parsers; csv-parse handles encoding edge cases |
| Auth | **JWT** (access) + **bcrypt** (passwords) + **Passport.js** (Google OAuth) | Standard stack; works fully locally with Google OAuth on localhost redirect |
| Validation | **Zod** | Shared schemas with frontend; validates all request bodies at the boundary |
| Rate limiting | **express-rate-limit** | Protects the AI endpoint from cost abuse locally |

### 2.3 Data

| Layer | Choice | Why |
|-------|--------|-----|
| Database | **PostgreSQL 16** (via Docker) | Relational model fits the household/account/transaction hierarchy; complex aggregation queries run in SQL, not JS |
| Caching | **In-process Node.js Map** (TTL cache) | No Redis needed locally; dashboard aggregates cached for 60s |
| File storage | **Local temp directory** | Files written to `/tmp/fba-uploads`, parsed, then deleted. Never persisted |
| Migrations | **Prisma Migrate** | Version-controlled schema changes |

### 2.4 AI

| Layer | Choice | Why |
|-------|--------|-----|
| Provider | **OpenAI GPT-4o** | Strong function-calling, long context, reliable structured output |
| Integration pattern | **Function calling (tool use)** | AI queries structured data rather than receiving raw transaction dumps — prevents hallucination, keeps token cost low |
| SDK | **openai** npm package | Official, typed |

---

## 3. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│  BROWSER (localhost:5173)                                           │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │  React App   │  │ TanStack     │  │  Zustand                  │ │
│  │  (Vite)      │  │ Query Cache  │  │  (auth + UI state)        │ │
│  └──────┬───────┘  └──────┬───────┘  └───────────────────────────┘ │
│         │                 │                                         │
└─────────┼─────────────────┼─────────────────────────────────────────┘
          │ HTTP/REST        │
          ▼ (localhost:3001) │
┌─────────────────────────────────────────────────────────────────────┐
│  EXPRESS API SERVER (Node.js)                                       │
│                                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │  Auth       │  │  Middleware  │  │  In-process TTL Cache     │  │
│  │  (JWT +     │  │  • helmet    │  │  (dashboard aggregates)   │  │
│  │   Google)   │  │  • rate-limit│  └───────────────────────────┘  │
│  └─────────────┘  │  • household │                                  │
│                   │    scoping   │                                  │
│  Route Groups:    └──────────────┘                                  │
│  /api/auth          /api/transactions                               │
│  /api/accounts      /api/budgets                                    │
│  /api/imports       /api/dashboard                                  │
│  /api/categories    /api/ai  ──────────────────────────────────┐   │
│                                                                 │   │
│  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  File Ingestion Pipeline                                │   │   │
│  │  upload → validate → parse (csv/ofx) → dedup           │   │   │
│  │  → categorise (rules) → commit → delete file           │   │   │
│  └───────────────────────────┬─────────────────────────────┘   │   │
│                              │                                  │   │
└──────────────────────────────┼──────────────────────────────────┼───┘
                               │                                  │
                               ▼                                  ▼
┌──────────────────────────┐      ┌──────────────────────────────────┐
│  PostgreSQL 16 (Docker)  │      │  OpenAI API (internet)           │
│  localhost:5432          │      │  GPT-4o + function calling       │
│                          │      │                                  │
│  • households            │  ◄───│  Tools:                          │
│  • members               │      │  • query_transactions()          │
│  • accounts              │      │  • get_budget_status()           │
│  • transactions          │      │  • get_goal_progress()           │
│  • categories            │      │  • get_cash_flow()               │
│  • budget_periods        │      │  • get_income_summary()          │
│  • goals                 │      └──────────────────────────────────┘
│  • import_batches        │
│  • category_rules        │
└──────────────────────────┘

              ┌──────────────────┐
              │  /tmp/fba-uploads│  ← files land here, parsed, deleted
              └──────────────────┘
```

---

## 4. Data Models

### 4.1 Full Prisma Schema

```prisma
// schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ── HOUSEHOLD & MEMBERS ──────────────────────────────────────────

model Household {
  id         String   @id @default(uuid())
  name       String
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  members      Member[]
  accounts     Account[]
  transactions Transaction[]
  categories   Category[]
  rules        CategoryRule[]
  budgets      BudgetPeriod[]
  goals        Goal[]
  invites      InviteToken[]
  auditLogs    AuditLog[]
}

model Member {
  id           String     @id @default(uuid())
  householdId  String
  email        String     @unique
  passwordHash String?
  googleId     String?    @unique
  name         String
  role         MemberRole @default(VIEWER)
  createdAt    DateTime   @default(now())
  updatedAt    DateTime   @updatedAt

  household    Household    @relation(fields: [householdId], references: [id], onDelete: Cascade)
  sessions     Session[]
  imports      ImportBatch[]
  transactions Transaction[] @relation("TransactionMember")
  invitesSent  InviteToken[]
  auditLogs    AuditLog[]

  @@index([householdId])
  @@index([email])
}

enum MemberRole {
  OWNER
  EDITOR
  VIEWER
}

// ── AUTH ─────────────────────────────────────────────────────────

model Session {
  id         String   @id @default(uuid())
  memberId   String
  tokenHash  String   @unique
  expiresAt  DateTime
  createdAt  DateTime @default(now())

  member Member @relation(fields: [memberId], references: [id], onDelete: Cascade)

  @@index([memberId])
  @@index([tokenHash])
}

model InviteToken {
  id          String    @id @default(uuid())
  householdId String
  invitedById String
  email       String
  role        MemberRole
  token       String    @unique @default(uuid())
  expiresAt   DateTime
  acceptedAt  DateTime?
  createdAt   DateTime  @default(now())

  household Household @relation(fields: [householdId], references: [id], onDelete: Cascade)
  invitedBy Member    @relation(fields: [invitedById], references: [id])

  @@index([token])
  @@index([email])
}

// ── ACCOUNTS & IMPORTS ───────────────────────────────────────────

model Account {
  id              String      @id @default(uuid())
  householdId     String
  institutionName String
  nickname        String
  accountType     AccountType
  currency        String      @default("USD")
  lastImportDate  DateTime?
  createdAt       DateTime    @default(now())
  updatedAt       DateTime    @updatedAt

  household    Household     @relation(fields: [householdId], references: [id], onDelete: Cascade)
  imports      ImportBatch[]
  transactions Transaction[]

  @@index([householdId])
}

enum AccountType {
  CHECKING
  SAVINGS
  CREDIT_CARD
  CASH
}

model ImportBatch {
  id             String       @id @default(uuid())
  accountId      String
  uploadedById   String
  fileName       String
  fileSize       Int
  status         ImportStatus @default(PENDING)
  rowsImported   Int          @default(0)
  rowsSkipped    Int          @default(0)
  rowsFailed     Int          @default(0)
  dateRangeStart DateTime?
  dateRangeEnd   DateTime?
  columnMapping  Json?        // saved mapping for re-use per institution
  errorLog       Json?        // array of {row, reason} for failures
  createdAt      DateTime     @default(now())

  account      Account       @relation(fields: [accountId], references: [id], onDelete: Cascade)
  uploadedBy   Member        @relation(fields: [uploadedById], references: [id])
  transactions Transaction[]

  @@index([accountId])
}

enum ImportStatus {
  PENDING
  PARSING
  AWAITING_REVIEW
  COMPLETE
  FAILED
}

// ── TRANSACTIONS ─────────────────────────────────────────────────

model Transaction {
  id               String          @id @default(uuid())
  householdId      String
  accountId        String
  importBatchId    String?
  externalId       String?         // dedup hash: date+amount+description+accountId
  date             DateTime
  payee            String          // original description from bank
  payeeNormalized  String?         // cleaned merchant name
  amount           Decimal         @db.Decimal(12, 2) // positive = money in, negative = money out
  transactionType  TransactionType @default(EXPENSE)
  categoryId       String?
  memberId         String?         // which household member
  notes            String?
  status           ReviewStatus    @default(PENDING_REVIEW)
  isDuplicateOf    String?         // self-reference for soft-duplicate flagging
  transferPairId   String?         // links debit+credit sides of an internal transfer
  createdAt        DateTime        @default(now())
  updatedAt        DateTime        @updatedAt

  household   Household    @relation(fields: [householdId], references: [id], onDelete: Cascade)
  account     Account      @relation(fields: [accountId], references: [id])
  importBatch ImportBatch? @relation(fields: [importBatchId], references: [id])
  category    Category?    @relation(fields: [categoryId], references: [id])
  member      Member?      @relation("TransactionMember", fields: [memberId], references: [id])

  @@unique([externalId, accountId])   // dedup constraint
  @@index([householdId, date])        // primary query pattern
  @@index([householdId, categoryId])
  @@index([accountId])
  @@index([transferPairId])
}

enum TransactionType {
  EXPENSE
  INCOME
  TRANSFER
  REFUND
}

enum ReviewStatus {
  PENDING_REVIEW
  CONFIRMED
}

// ── CATEGORIES ───────────────────────────────────────────────────

model Category {
  id          String  @id @default(uuid())
  householdId String? // null = system default category
  name        String
  parentId    String? // null = top-level category
  bucket      Bucket  @default(NEEDS)
  color       String  @default("#6A5A42")
  icon        String  @default("📦")
  isHidden    Boolean @default(false)
  sortOrder   Int     @default(0)
  createdAt   DateTime @default(now())

  household    Household?    @relation(fields: [householdId], references: [id], onDelete: Cascade)
  parent       Category?     @relation("CategoryTree", fields: [parentId], references: [id])
  children     Category[]    @relation("CategoryTree")
  transactions Transaction[]
  rules        CategoryRule[]
  budgetLines  BudgetLine[]
  goals        Goal[]

  @@index([householdId])
  @@index([parentId])
}

enum Bucket {
  NEEDS
  WANTS
  SAVINGS
}

model CategoryRule {
  id          String      @id @default(uuid())
  householdId String
  pattern     String      // text to match against payee
  patternType PatternType @default(CONTAINS)
  categoryId  String
  memberId    String?     // optionally also assign a member
  accountId   String?     // scope rule to a specific account
  priority    Int         @default(0) // higher = applied first
  createdAt   DateTime    @default(now())

  household Household @relation(fields: [householdId], references: [id], onDelete: Cascade)
  category  Category  @relation(fields: [categoryId], references: [id])

  @@index([householdId])
}

enum PatternType {
  CONTAINS
  STARTS_WITH
  ENDS_WITH
  REGEX
}

// ── BUDGETS ──────────────────────────────────────────────────────

model BudgetPeriod {
  id              String   @id @default(uuid())
  householdId     String
  year            Int
  month           Int      // 1–12
  incomeExpected  Decimal? @db.Decimal(12, 2)
  isFinalized     Boolean  @default(false)
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  household   Household    @relation(fields: [householdId], references: [id], onDelete: Cascade)
  budgetLines BudgetLine[]

  @@unique([householdId, year, month])
  @@index([householdId])
}

model BudgetLine {
  id             String  @id @default(uuid())
  budgetPeriodId String
  categoryId     String
  amountLimit    Decimal @db.Decimal(12, 2)
  createdAt      DateTime @default(now())

  budgetPeriod BudgetPeriod @relation(fields: [budgetPeriodId], references: [id], onDelete: Cascade)
  category     Category     @relation(fields: [categoryId], references: [id])

  @@unique([budgetPeriodId, categoryId])
}

// ── GOALS ────────────────────────────────────────────────────────

model Goal {
  id            String    @id @default(uuid())
  householdId   String
  name          String
  targetAmount  Decimal   @db.Decimal(12, 2)
  targetDate    DateTime?
  categoryId    String?   // linked savings category
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  household Household @relation(fields: [householdId], references: [id], onDelete: Cascade)
  category  Category? @relation(fields: [categoryId], references: [id])

  @@index([householdId])
}

// ── AUDIT LOG ────────────────────────────────────────────────────

model AuditLog {
  id          String   @id @default(uuid())
  householdId String
  memberId    String?
  action      String   // e.g. "import.complete", "transaction.bulk_categorise"
  entityType  String?
  entityId    String?
  details     Json?
  createdAt   DateTime @default(now())

  household Household @relation(fields: [householdId], references: [id], onDelete: Cascade)
  member    Member?   @relation(fields: [memberId], references: [id])

  @@index([householdId, createdAt])
}
```

### 4.2 Key Relationship Notes

| Relationship | Design decision |
|---|---|
| `Transaction.amount` | Signed decimal: negative = money out (expense), positive = money in (income). Single field avoids debit/credit confusion across bank formats. |
| `Transaction.externalId` | SHA-256 hash of `date + amount + payee + accountId`. Unique constraint enforces dedup at DB level — not just application logic. |
| `Transaction.transferPairId` | Self-join links the checking debit to the credit card credit for the same payment. Both sides are confirmed as TRANSFER type. |
| `Category.householdId = null` | System default categories (Groceries, Dining, etc.) have no household owner. Households can override or add their own. |
| `BudgetLine` per category per month | Granular: each category gets its own limit. The 50/30/20 bucket totals are computed in the query layer, not stored. |

---

## 5. API Design

### 5.1 Route Map

```
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/auth/google                   ← OAuth redirect
GET    /api/auth/google/callback
POST   /api/auth/logout
POST   /api/auth/refresh

GET    /api/household                     ← current household
PATCH  /api/household
GET    /api/household/members
POST   /api/household/invite
DELETE /api/household/members/:memberId
GET    /api/household/invite/:token       ← accept invite

GET    /api/accounts
POST   /api/accounts
PATCH  /api/accounts/:id
DELETE /api/accounts/:id

POST   /api/imports/upload               ← multipart/form-data
POST   /api/imports/:id/preview          ← parse without committing
POST   /api/imports/:id/commit           ← write to DB, delete file
GET    /api/imports                      ← history log
GET    /api/imports/:id

GET    /api/transactions                 ← ?page, filter, sort, search
GET    /api/transactions/:id
PATCH  /api/transactions/:id
POST   /api/transactions/bulk            ← bulk category/member update
DELETE /api/transactions/:id

GET    /api/categories                   ← system + household categories
POST   /api/categories
PATCH  /api/categories/:id
DELETE /api/categories/:id
GET    /api/categories/rules
POST   /api/categories/rules
DELETE /api/categories/rules/:id

GET    /api/budgets/:year/:month
POST   /api/budgets/:year/:month
PUT    /api/budgets/:year/:month/lines   ← replace all lines
GET    /api/budgets/wizard               ← suggested budget from history

GET    /api/goals
POST   /api/goals
PATCH  /api/goals/:id
DELETE /api/goals/:id

GET    /api/dashboard                    ← current month summary (cached 60s)
GET    /api/dashboard/cashflow           ← 6-month income vs expense
GET    /api/dashboard/pacing             ← budget vs actual, all categories

POST   /api/ai/chat                      ← { message, conversationHistory[] }
```

### 5.2 Middleware Stack (every request)

```
Request
  → helmet()               // security headers
  → cors({ localhost })    // restrict to localhost
  → express.json()         // parse body
  → rateLimiter()          // global: 100/min; AI endpoint: 10/min
  → authenticate()         // verify JWT, attach req.member
  → scopeToHousehold()     // attach req.householdId, enforce membership
  → route handler
  → errorHandler()         // unified error responses
```

### 5.3 Standard Response Shape

```typescript
// Success
{ data: T, meta?: { page, total, hasMore } }

// Error
{ error: { code: string, message: string, details?: unknown } }

// Error codes used throughout
"UNAUTHORIZED"        // 401 — missing or invalid JWT
"FORBIDDEN"           // 403 — insufficient role
"NOT_FOUND"           // 404
"VALIDATION_ERROR"    // 422 — Zod schema failure, includes field-level details
"RATE_LIMITED"        // 429
"IMPORT_PARSE_ERROR"  // 422 — file could not be parsed
"DUPLICATE_IMPORT"    // 409 — all rows already exist
```

---

## 6. AI Integration Architecture

### 6.1 Why Function Calling (Not Raw Data in Prompt)

Sending raw transaction CSVs to GPT-4o would:
- Cost ~$0.05–0.50 per query for a household with 6 months of history
- Risk hallucinating transaction details
- Leak all data in a single large request

Instead, the AI receives a **minimal system prompt** and uses **structured tool calls** to fetch only the data it needs to answer the question.

### 6.2 Tool Definitions

```typescript
const AI_TOOLS = [
  {
    name: "get_spending_summary",
    description: "Returns total spending aggregated by category for a time period",
    parameters: {
      period:      { type: "string", enum: ["current_month","last_month","last_3_months","last_6_months","ytd"] },
      categoryId:  { type: "string", optional: true },
      memberId:    { type: "string", optional: true },
      bucket:      { type: "string", enum: ["NEEDS","WANTS","SAVINGS"], optional: true }
    }
  },
  {
    name: "get_budget_status",
    description: "Returns budget limit vs actual spend for each category in a period",
    parameters: {
      period: { type: "string", enum: ["current_month","last_month"] },
      categoryId: { type: "string", optional: true }
    }
  },
  {
    name: "get_transactions",
    description: "Returns a filtered list of transactions — use for specific merchant or date questions",
    parameters: {
      startDate:   { type: "string" },
      endDate:     { type: "string" },
      categoryId:  { type: "string", optional: true },
      memberId:    { type: "string", optional: true },
      minAmount:   { type: "number", optional: true },
      maxAmount:   { type: "number", optional: true },
      limit:       { type: "number", default: 20, max: 50 }
    }
  },
  {
    name: "get_goal_progress",
    description: "Returns progress toward savings goals",
    parameters: {
      goalId: { type: "string", optional: true }   // omit to get all goals
    }
  },
  {
    name: "get_cash_flow",
    description: "Returns monthly income vs expense totals over N months",
    parameters: {
      months: { type: "number", default: 6, max: 12 }
    }
  },
  {
    name: "get_income_summary",
    description: "Returns income sources and totals for a period",
    parameters: {
      period: { type: "string", enum: ["current_month","last_month","last_3_months","ytd"] }
    }
  }
]
```

### 6.3 Request Flow

```
User message
    │
    ▼
POST /api/ai/chat
    │
    ├── Validate: member has access to household
    ├── Build system prompt (household context — member names, current date)
    ├── Append conversation history (last 10 turns, trimmed)
    │
    ▼
OpenAI GPT-4o (stream: false for simplicity in MVP)
    │
    ├── Model returns tool_call?
    │     YES → execute tool against DB → append tool result → re-call model
    │     NO  → return final text response
    │
    ▼
Response streamed back to client
    │
    ├── Logged to AuditLog (member, question, tools used — not the answer)
    └── Rate-limited: 10 AI requests / member / minute
```

### 6.4 System Prompt Template

```
You are a budget assistant for the {householdName} household.
Today's date is {date}. The current budget period is {month} {year}.

Household members: {memberNames}.

You have access to tools that query this household's real financial data.
Always use a tool to answer questions — never guess or invent numbers.

Rules:
- Answer in plain English, as if explaining to a non-finance person.
- Never give investment advice, tax advice, or financial recommendations.
- When data is unavailable, say so clearly.
- Keep answers concise (2–4 sentences unless more detail is requested).
- This is not financial advice. You are summarising the household's own data.
```

### 6.5 Cost Control (Local Use)

| Control | Implementation |
|---|---|
| Rate limit | 10 AI queries/member/minute via `express-rate-limit` |
| Tool result size | `get_transactions` capped at 50 rows; aggregations return totals not raw rows |
| Max turns | Conversation history trimmed to last 10 turns before each request |
| No streaming in MVP | Reduces connection complexity; stream can be added in Phase 2 |

---

## 7. Security Design

### 7.1 Authentication Flow

```
Signup:
  POST /auth/signup
    → Zod validate input
    → Check email not already registered
    → bcrypt.hash(password, 12)
    → Create Member + Household in transaction
    → Issue JWT access token (15 min) + refresh token (7 days)
    → Refresh token stored as SHA-256 hash in Session table

Login:
  POST /auth/login
    → bcrypt.compare(password, hash)
    → Issue new token pair
    → Old sessions not invalidated (max 3 active sessions per member)

Token refresh:
  POST /auth/refresh
    → Hash incoming refresh token
    → Look up Session by hash
    → Verify not expired
    → Issue new access token
    → Rotate refresh token (sliding window)

Google OAuth:
  GET /auth/google → Passport redirect → Google
  GET /auth/google/callback → match googleId to Member or create Member
    → Same token issuance flow
```

### 7.2 Authorisation Model

Every protected route runs `scopeToHousehold()` middleware, which:
1. Extracts `householdId` from the authenticated member's record
2. Attaches `req.householdId` to every downstream query
3. **All Prisma queries include `householdId` as a where clause** — enforced at the service layer, not route handler

Role enforcement:

| Action | OWNER | EDITOR | VIEWER |
|--------|-------|--------|--------|
| Read all data | ✓ | ✓ | ✓ |
| Import files | ✓ | ✓ | ✗ |
| Edit transactions / categories | ✓ | ✓ | ✗ |
| Manage budgets | ✓ | ✓ | ✗ |
| AI assistant | ✓ | ✓ | ✓ |
| Invite members | ✓ | ✗ | ✗ |
| Delete household | ✓ | ✗ | ✗ |

### 7.3 File Upload Security

```
Upload pipeline:
  1. Multer: max 10 MB, accept only .csv / .ofx / .qfx (mime + extension check)
  2. File written to /tmp/fba-uploads/{uuid}-{timestamp}
  3. Parser reads from disk — never loaded fully into memory
  4. On commit: file deleted immediately after DB write
  5. On error: file deleted in catch block
  6. Scheduled cleanup: on server start, delete any orphaned files > 1h old
```

### 7.4 Data Validation

- All request bodies validated against **Zod schemas** at the route boundary
- Zod `.strict()` mode rejects unknown fields
- SQL injection: impossible via Prisma parameterised queries
- CSV injection: payee strings stored as text, rendered in React — never eval'd

### 7.5 XSS Prevention

There are three distinct surfaces where untrusted content is rendered in this app.
Each requires a different control:

#### Surface 1 — AI chat responses

The AI assistant returns plain-text answers that may be formatted with light
markdown (bold, bullet lists). Rendering these as raw HTML would allow a
prompt-injection attack to embed `<script>` tags in the AI response.

**Control:** Use `react-markdown` with a restricted allowlist of elements.
`react-markdown` renders markdown to React elements — it never calls
`dangerouslySetInnerHTML` internally when a custom renderer is provided.
Disallow `html`, `script`, `iframe`, and `a[href^="javascript:"]` nodes:

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ALLOWED_ELEMENTS = ['p','strong','em','ul','ol','li','code','blockquote'];

function AiMessage({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      allowedElements={ALLOWED_ELEMENTS}
      unwrapDisallowed   // strips disallowed tags but keeps their text content
    >
      {content}
    </ReactMarkdown>
  );
}
```

If `dangerouslySetInnerHTML` is ever used for AI content (e.g., for richer
formatting), the content **must** be sanitised with DOMPurify first:

```tsx
import DOMPurify from 'dompurify';

// Only if dangerouslySetInnerHTML is unavoidable
const clean = DOMPurify.sanitize(aiResponse, {
  ALLOWED_TAGS: ['p', 'strong', 'em', 'ul', 'ol', 'li', 'code'],
  ALLOWED_ATTR: []   // no attributes — prevents href/src injection
});
<div dangerouslySetInnerHTML={{ __html: clean }} />
```

#### Surface 2 — CSV payee strings from bank files

Bank CSV files can contain arbitrary text in the description column. A malicious
file could include strings like `=HYPERLINK(...)` (CSV injection for spreadsheet
tools) or HTML tags.

**Control:**
- Payee strings are stored as plain text in PostgreSQL (no HTML encoding at rest)
- React renders them as text nodes via JSX `{transaction.payee}` — automatic escaping
- `dangerouslySetInnerHTML` is **never** used to render payee or any bank-sourced string
- CSV injection note: exported CSVs prefix values starting with `=`, `+`, `-`, `@`
  with a single quote to neutralise spreadsheet formula injection

#### Surface 3 — User-defined content (category names, notes, household name)

Free-text fields entered by the user (notes, category names, household name).

**Control:** React JSX escapes these automatically. No special treatment needed
as long as they are rendered as text children, not as HTML. Zod schemas enforce
`string().max(255)` limits to prevent oversized payloads.

### 7.6 Local Security Considerations

| Risk | Mitigation |
|------|-----------|
| `.env` file with OpenAI key | `.env` in `.gitignore`; README warns never to commit |
| JWT secret in `.env` | Randomly generated 256-bit secret on `npm run setup` |
| Database on localhost | Postgres bound to `127.0.0.1` only (Docker config) |
| No HTTPS locally | Acceptable for localhost; headers set but TLS not enforced in dev |

---

## 8. Performance Design

### 8.1 Database Indexes (Critical Queries)

```sql
-- Most common query: all transactions for a household in a date range
CREATE INDEX idx_txn_household_date ON transactions(household_id, date DESC);

-- Category breakdown (dashboard)
CREATE INDEX idx_txn_household_category ON transactions(household_id, category_id);

-- Budget vs actual join
CREATE INDEX idx_txn_household_type_date ON transactions(household_id, transaction_type, date);

-- Dedup lookup during import
CREATE UNIQUE INDEX idx_txn_external_account ON transactions(external_id, account_id)
  WHERE external_id IS NOT NULL;

-- Transfer pair lookup
CREATE INDEX idx_txn_transfer_pair ON transactions(transfer_pair_id)
  WHERE transfer_pair_id IS NOT NULL;
```

### 8.2 Dashboard Aggregation Query

Dashboard data is computed in a **single SQL query** (not N queries in JS):

```sql
SELECT
  c.id            AS category_id,
  c.name          AS category_name,
  c.bucket        AS bucket,
  c.icon,
  c.color,
  bl.amount_limit AS budget_limit,
  SUM(ABS(t.amount)) FILTER (
    WHERE t.date >= date_trunc('month', CURRENT_DATE)
    AND   t.transaction_type = 'EXPENSE'
  )               AS spent_this_month,
  COUNT(t.id) FILTER (
    WHERE t.status = 'PENDING_REVIEW'
  )               AS pending_review_count
FROM categories c
LEFT JOIN budget_lines bl
  ON bl.category_id = c.id
  AND bl.budget_period_id = (
    SELECT id FROM budget_periods
    WHERE household_id = $1
    AND year = EXTRACT(YEAR FROM CURRENT_DATE)
    AND month = EXTRACT(MONTH FROM CURRENT_DATE)
  )
LEFT JOIN transactions t
  ON t.category_id = c.id
  AND t.household_id = $1
WHERE (c.household_id = $1 OR c.household_id IS NULL)
  AND c.is_hidden = FALSE
GROUP BY c.id, c.name, c.bucket, c.icon, c.color, bl.amount_limit
ORDER BY c.bucket, c.sort_order;
```

### 8.3 Caching Strategy

```typescript
// In-process TTL cache — no Redis needed locally
const cache = new Map<string, { data: unknown; expiresAt: number }>();

function getCached<T>(key: string, ttlMs: number, fetcher: () => Promise<T>): Promise<T> {
  const hit = cache.get(key);
  if (hit && hit.expiresAt > Date.now()) return Promise.resolve(hit.data as T);
  return fetcher().then(data => {
    cache.set(key, { data, expiresAt: Date.now() + ttlMs });
    return data;
  });
}

// Cache keys and TTLs
// dashboard:{householdId}          → 60 seconds
// cashflow:{householdId}           → 5 minutes
// categories:{householdId}         → 5 minutes
// budget_wizard:{householdId}      → 10 minutes

// Invalidation: any import commit or bulk transaction edit clears household cache
```

### 8.4 Import Performance

CSV parsing is the most CPU-intensive operation (up to 5,000 rows):

```
Target: 5,000 rows parsed in < 10 seconds on a typical laptop

Approach:
  1. csv-parse in streaming mode (not buffered) — memory stays flat
  2. Dedup hashing done in JS (SHA-256 per row) — ~0.1ms per row = 0.5s for 5k
  3. DB write: single Prisma createMany() in one transaction — avoids N round trips
  4. Category rules applied in JS after bulk insert (rules are few, usually < 50)
  5. Import preview (without DB write): returns in < 3 seconds

If needed: Node.js worker_thread for parsing to avoid blocking event loop.
```

### 8.5 React Query Cache Configuration

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,          // dashboard data fresh for 60s
      gcTime:    5 * 60_000,      // keep in memory 5 min
      retry: 1,
      refetchOnWindowFocus: false // don't refetch on tab switch for finance data
    }
  }
});

// Specific overrides
// transactions list: staleTime 30s (changes frequently after import)
// categories:        staleTime 5min (rarely changes)
// budget_wizard:     staleTime 10min (expensive aggregation)
```

---

## 9. Scalability Considerations

This section documents constraints and upgrade paths **for after local MVP**, so the architecture doesn't paint itself into corners.

### 9.1 What the Local Architecture Already Gets Right

- **Stateless API**: JWT auth means no server-side session affinity. Adding a second API instance later requires zero code changes.
- **Database schema**: UUID PKs (not serial integers) and `householdId` scoping are cloud-ready. No schema changes to shard by household later.
- **AI function calling**: Tool-based architecture means the AI layer is independent of DB scale. Tools can query replicas or a data warehouse later.
- **File parsing**: Stateless pipeline (upload → parse → delete) is trivially moveable to a worker queue later.

### 9.2 Upgrade Path Per Constraint

| Constraint | Local solution | Scale-up path |
|---|---|---|
| Database | Local PostgreSQL | Managed Postgres (Supabase, RDS) — same Prisma schema |
| Cache | In-process Map | Redis (swap one function) |
| File storage | `/tmp` disk | S3 + presigned upload URLs |
| Session store | PostgreSQL Sessions table | Redis |
| Import processing | Synchronous, in-request | BullMQ job queue + worker process |
| AI latency | Synchronous response | SSE streaming (add `stream: true` to OpenAI call) |
| Multi-tenant isolation | `householdId` WHERE clauses | Row-level security in Postgres (policy per householdId) |

### 9.3 Data Volume Projections

| Scenario | Transactions/year | Storage estimate |
|---|---|---|
| 1 household, 4 accounts | ~3,000 | < 5 MB |
| 100 households | ~300,000 | < 500 MB |
| 10,000 households | ~30M | < 50 GB — still single Postgres instance |

The data model supports millions of transactions per household without structural changes. Index design in §8.1 is the primary scaling lever.

---

## 10. Implementation Plan

### 10.1 Phased Delivery

```
Phase 1 — Foundation (Week 1)
├── Monorepo scaffold (apps/web, apps/api, packages/shared)
├── Prisma schema + initial migration
├── Auth: signup, login, JWT, Google OAuth
├── Household creation + member invite flow
├── Account CRUD
└── Basic nav shell (React, Tailwind, React Query setup)

Phase 2 — Import Engine (Week 2)
├── File upload endpoint (Multer, validation)
├── CSV parser: streaming, column mapper, dedup hash
├── OFX/QFX parser
├── Duplicate detection + merge/skip UI
├── Import preview screen
├── Import commit pipeline (categorisation rules applied)
└── Transaction ledger page (paginated list, filter, search)

Phase 3 — Categorisation + Budget (Week 3)
├── Seed default family category tree (system categories)
├── Category management UI (add/edit/hide)
├── Auto-categorisation rule engine (pattern matching + priority)
├── Review queue UI (uncategorised + low-confidence after import)
├── Bulk edit (category, member for selected rows)
├── Budget wizard (median spend from last 3 months → proposed limits)
└── Budget setup UI (edit limits per category, 50/30/20 bucket totals)

Phase 4 — Dashboard + AI (Week 4)
├── Dashboard aggregation query + caching
├── Pacing widgets (category % used vs % of month elapsed)
├── Cash flow chart (6-month income vs expense — Recharts)
├── Category breakdown chart
├── OpenAI integration (function calling, tool implementations)
├── AI chat panel UI (right drawer, conversation history)
└── "Where did we overspend?" summary component

Phase 5 — Polish + Freemium (Week 5)
├── Freemium gating: 6-month history limit (query filter + upsell prompt)
├── Export lock (CSV export button → premium prompt for free tier)
├── In-app notifications (over-budget alerts, import complete)
├── Settings page (household name, member roles, account management)
├── Mobile-responsive pass (dashboard, AI chat, quick review)
└── End-to-end smoke tests for all critical flows
```

### 10.2 Critical Path

The features that block everything else:

```
Auth → Household → Account → Import → Transaction Ledger
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                         Categories   Budget      AI Chat
                         + Rules      Wizard      (needs data)
                              │           │
                              └─────┬─────┘
                                    ▼
                                Dashboard
```

**Minimum viable demo sequence:**
1. Sign up → create household
2. Add a Chase Checking account
3. Upload a Chase CSV
4. See mapped + auto-categorised transactions in the ledger
5. Run budget wizard → set limits
6. Ask AI: "How much did we spend on groceries last month?"

This end-to-end path should be unblocked by end of Week 2.

### 10.3 Folder Structure

```
family-budget-app/
├── apps/
│   ├── web/                          # React + Vite frontend
│   │   ├── src/
│   │   │   ├── pages/                # Route-level page components
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── Transactions.tsx
│   │   │   │   ├── Import.tsx
│   │   │   │   ├── Budget.tsx
│   │   │   │   └── AiChat.tsx
│   │   │   ├── components/           # Shared UI components
│   │   │   │   ├── PacingWidget.tsx
│   │   │   │   ├── CategoryBar.tsx
│   │   │   │   ├── ChatPanel.tsx
│   │   │   │   └── ImportWizard/
│   │   │   ├── hooks/                # Custom React Query hooks
│   │   │   ├── lib/                  # API client, auth helpers
│   │   │   └── store/                # Zustand stores
│   │   └── package.json
│   │
│   └── api/                          # Express + Prisma backend
│       ├── src/
│       │   ├── routes/               # Route handlers (thin)
│       │   │   ├── auth.ts
│       │   │   ├── accounts.ts
│       │   │   ├── imports.ts
│       │   │   ├── transactions.ts
│       │   │   ├── budgets.ts
│       │   │   ├── dashboard.ts
│       │   │   └── ai.ts
│       │   ├── services/             # Business logic (thick)
│       │   │   ├── importService.ts
│       │   │   ├── categorisationService.ts
│       │   │   ├── budgetService.ts
│       │   │   ├── dashboardService.ts
│       │   │   └── aiService.ts
│       │   ├── parsers/
│       │   │   ├── csvParser.ts
│       │   │   └── ofxParser.ts
│       │   ├── middleware/
│       │   │   ├── authenticate.ts
│       │   │   ├── scopeToHousehold.ts
│       │   │   └── rateLimiter.ts
│       │   ├── lib/
│       │   │   ├── prisma.ts
│       │   │   ├── cache.ts
│       │   │   └── openai.ts
│       │   └── app.ts
│       └── package.json
│
├── packages/
│   └── shared/                       # Shared Zod schemas + TypeScript types
│       ├── schemas/
│       │   ├── transaction.ts
│       │   ├── budget.ts
│       │   └── import.ts
│       └── package.json
│
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts                       # Seeds default categories
│
├── docker-compose.yml                # PostgreSQL only
├── .env.example
└── package.json                      # Workspace root
```

---

## 11. Local Development Setup

### 11.1 Prerequisites

```bash
node >= 20.x
docker + docker compose
openssl (for JWT secret generation)
```

### 11.2 First-Time Setup

```bash
# 1. Clone and install
git clone <repo>
npm install          # installs all workspaces

# 2. Start PostgreSQL
docker compose up -d

# 3. Configure environment
cp .env.example .env
# Edit .env:
#   DATABASE_URL=postgresql://fba:fba@localhost:5432/familybudget
#   JWT_SECRET=$(openssl rand -hex 32)
#   OPENAI_API_KEY=sk-...
#   GOOGLE_CLIENT_ID=...     (optional for local — email/password works without it)
#   GOOGLE_CLIENT_SECRET=...

# 4. Run migrations + seed default categories
npx prisma migrate dev
npx prisma db seed

# 5. Start both apps
npm run dev          # starts api on :3001 and web on :5173 concurrently
```

### 11.3 docker-compose.yml

```yaml
version: '3.9'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: fba
      POSTGRES_PASSWORD: fba
      POSTGRES_DB: familybudget
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 11.4 Environment Variables

```bash
# apps/api/.env.example
DATABASE_URL="postgresql://fba:fba@localhost:5432/familybudget"
JWT_SECRET=""                  # openssl rand -hex 32
JWT_ACCESS_EXPIRES="15m"
JWT_REFRESH_EXPIRES="7d"
OPENAI_API_KEY=""              # required for AI assistant
OPENAI_MODEL="gpt-4o"
GOOGLE_CLIENT_ID=""            # optional — Google OAuth
GOOGLE_CLIENT_SECRET=""
GOOGLE_CALLBACK_URL="http://localhost:3001/api/auth/google/callback"
UPLOAD_TEMP_DIR="/tmp/fba-uploads"
MAX_FILE_SIZE_MB=10
PORT=3001
```

---

*Architecture owner: Engineering Lead (TBD)*  
*Next review: Before Phase 1 kickoff*
