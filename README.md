# FamilyBudget — AI-Powered Household Budget Assistant

A local-first family budgeting app with an AI assistant powered by Google Gemini.

## Quick Start

1. Open `app.html` in any modern browser (Chrome, Firefox, Safari, Edge)
2. Sign up or use the demo login (`elena@martinez.com` / any password)
3. Enter your **Gemini API key** when prompted (get one free at [aistudio.google.com](https://aistudio.google.com))
4. Explore the pre-loaded Martinez family demo data

## Features

| Feature | Description |
|---|---|
| **Dashboard** | Budget pacing, cash flow chart, savings goals |
| **Transactions** | Full ledger with auto-categorisation, bulk edit, review queue |
| **CSV Import** | Upload any US bank statement — drag & drop, column auto-detection |
| **Budget Wizard** | 50/30/20 framework with per-category spending caps |
| **AI Assistant** | Ask questions in plain English — powered by Gemini 1.5 Flash |

## Running Locally

No server or install needed. Just open `app.html` directly in your browser.

```bash
# Or run a simple local server to avoid browser file:// restrictions
python3 -m http.server 8080
# Then open: http://localhost:8080/app.html
```

## API Key Security

- Your Gemini API key is stored **only in your browser's localStorage**
- It is never written to any file or committed to this repository
- Rotate your key at [console.cloud.google.com](https://console.cloud.google.com) after any public demo

## Project Structure

```
├── app.html          Main application (all-in-one SPA)
├── designs/          Landing page design explorations (Options 1–4)
├── PRD.md            Product Requirements Document
├── ARCHITECTURE.md   Architecture design & implementation plan
└── REQUIREMENTS.md   Original requirements document
```

## Design System

- **Fonts:** Fredoka (headings) + Nunito (body)
- **Palette:** Coral `#C84830` · Amber `#D4A030` · Sage `#4AAE7A` · Sky `#5888C8`
- **Style:** Warm & approachable — Option 3 from the design exploration

## Security Notes

- CDN scripts (Chart.js, PapaParse, DOMPurify) are loaded with **Subresource Integrity (SRI)** hashes
- All user-sourced strings (CSV payees, names) are run through `escapeHtml()` before HTML insertion
- AI responses are sanitised with **DOMPurify** before rendering
- No credentials are ever stored or transmitted — file-based import only
