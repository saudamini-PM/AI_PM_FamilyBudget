"""
Generates Idea_Overview_Deck.pptx from IDEA_OVERVIEW.md content.
Run: python3 scripts/build_idea_overview_pptx.py
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'Idea_Overview_Deck.pptx')

# ── Colours ────────────────────────────────────────────────────────────────────
BG      = RGBColor(0x0a, 0x0e, 0x1a)
SURFACE = RGBColor(0x11, 0x18, 0x27)
CARD    = RGBColor(0x1a, 0x22, 0x35)
BORDER  = RGBColor(0x2a, 0x34, 0x50)
ACCENT  = RGBColor(0x4f, 0x8e, 0xf7)
GREEN   = RGBColor(0x22, 0xc5, 0x5e)
AMBER   = RGBColor(0xf5, 0x9e, 0x0b)
PURPLE  = RGBColor(0x7c, 0x3a, 0xed)
RED     = RGBColor(0xef, 0x44, 0x44)
WHITE   = RGBColor(0xff, 0xff, 0xff)
MUTED   = RGBColor(0x94, 0xa3, 0xb8)
TEXT    = RGBColor(0xe2, 0xe8, 0xf0)

# ── Helpers ────────────────────────────────────────────────────────────────────
def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    return slide

def W(frac=1.0): return Inches(13.33 * frac)
def H(frac=1.0): return Inches(7.5  * frac)
L = Inches
P = Pt

def box(slide, left, top, width, height,
        fill=None, line_color=BORDER, line_pt=0.75):
    shp = slide.shapes.add_shape(1, left, top, width, height)
    shp.fill.solid() if fill else shp.fill.background()
    if fill: shp.fill.fore_color.rgb = fill
    if line_color:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_pt)
    else:
        shp.line.fill.background()
    return shp

def txt(slide, text, left, top, width, height,
        size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
        wrap=True, italic=False):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = P(size)
    run.font.color.rgb = color
    run.font.bold  = bold
    run.font.italic = italic
    run.font.name  = 'Calibri'
    return txb

def label_header(slide, label_text, title_text, top=Inches(0.38)):
    txt(slide, label_text.upper(), L(0.5), top, W(0.9), L(0.28),
        size=9, color=ACCENT, bold=True)
    txt(slide, title_text, L(0.5), top + L(0.28), W(0.9), L(0.6),
        size=26, color=WHITE, bold=True)

def card_box(slide, left, top, width, height, fill=CARD, line=BORDER):
    return box(slide, left, top, width, height, fill=fill, line_color=line, line_pt=0.75)

def set_cell_fill(cell, color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    solidFill = etree.SubElement(tcPr, qn('a:solidFill'))
    srgbClr   = etree.SubElement(solidFill, qn('a:srgbClr'))
    srgbClr.set('val', '%02x%02x%02x' % (color[0], color[1], color[2]))

def table_cell_text(cell, text, size=11, color=TEXT, bold=False, align=PP_ALIGN.LEFT):
    cell.text = ''
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = P(size)
    run.font.color.rgb = color
    run.font.bold  = bold
    run.font.name  = 'Calibri'

def add_notes(slide, text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = text

# ── Presentation setup ─────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)

box(sl, L(0), L(0), W(0.38), H(), fill=RGBColor(0x0d, 0x1f, 0x4a), line_color=None)
txt(sl, '💡', L(0.55), L(0.44), L(0.7), L(0.7), size=28, align=PP_ALIGN.CENTER)

txt(sl, 'Idea Overview', L(0.5), L(1.1), W(0.55), L(0.7), size=46, color=WHITE, bold=True)
txt(sl, 'Family Budget Assistant', L(0.5), L(1.78), W(0.55), L(0.55), size=32, color=ACCENT, bold=True)

txt(sl,
    'A structured overview covering target customers, pain points,\n'
    'our solution, key features, competitive landscape,\n'
    'and the AI/data strategy behind the product.',
    L(0.5), L(2.55), W(0.52), L(1.1), size=13, color=MUTED)

checklist = [
    ('☑', 'Target Customer'),
    ('☑', 'Customer Pain Points & Challenges'),
    ('☑', 'How We Plan to Solve the Problem'),
    ('☑', 'Key Features'),
    ('☑', 'Competitors in the Market'),
    ('☑', 'Existing Data & Models for AI'),
]
for i, (check, item) in enumerate(checklist):
    y = L(3.85) + i * L(0.42)
    txt(sl, check, L(0.55), y, L(0.35), L(0.38), size=14, color=GREEN, bold=True)
    txt(sl, item,  L(0.9),  y, W(0.45), L(0.38), size=12, color=TEXT)

box(sl, W(0.62), L(0), W(0.38), H(), fill=RGBColor(0x06, 0x0a, 0x12), line_color=None)
txt(sl, '🏠', W(0.62), L(2.4), W(0.38), L(0.8), size=60, align=PP_ALIGN.CENTER)
txt(sl, 'Family Budget Assistant', W(0.62), L(3.2), W(0.38), L(0.5), size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(sl, 'Your household finances, honestly.', W(0.62), L(3.68), W(0.38), L(0.4), size=12, color=MUTED, align=PP_ALIGN.CENTER)
txt(sl, '2026-06-04', W(0.62), L(6.9), W(0.38), L(0.3), size=10, color=BORDER, align=PP_ALIGN.CENTER)

add_notes(sl, "Introduce the six sections of this idea overview. Each section is one slide. The goal is to give any stakeholder a complete mental model of the product in under 10 minutes.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — TARGET CUSTOMER
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ Target Customer', 'The Household CFO & their family')

# Primary persona card
card_box(sl, L(0.5), L(1.72), W(0.93), L(1.62), line=ACCENT)
box(sl, L(0.5), L(1.72), L(0.06), L(1.62), fill=ACCENT, line_color=None)
txt(sl, '👩', L(0.65), L(1.82), L(0.85), L(0.85), size=34)
txt(sl, 'Primary: "Morgan, 38" — The Household CFO', L(1.65), L(1.79), W(0.78), L(0.38), size=13, color=WHITE, bold=True)
txt(sl, 'Parent · $75K–$250K household income · US-first · 3–8 accounts across 2+ banks', L(1.65), L(2.14), W(0.78), L(0.28), size=10, color=ACCENT)
txt(sl,
    'Manages checking, savings, 2+ credit cards, and her partner\'s accounts. '
    'Spends ~2 hours/month manually consolidating finances in spreadsheets. '
    'Privacy-conscious — avoids linking bank credentials to third-party apps. '
    'Needs: import, categorize, family budget, mid-month alerts, and plain-English answers.',
    L(1.65), L(2.4), W(0.78), L(0.78), size=11, color=MUTED, wrap=True)

# ICP tags
tags = ['3–8 accounts', '2+ institutions', 'Privacy-conscious', 'Spreadsheet refugee', 'Already downloads CSVs']
for i, t in enumerate(tags):
    bx = L(0.5) + i * L(2.28)
    box(sl, bx, L(3.46), L(2.15), L(0.3), fill=RGBColor(0x0d, 0x2a, 0x5a), line_color=ACCENT, line_pt=0.4)
    txt(sl, t, bx + L(0.08), L(3.47), L(2.0), L(0.26), size=9, color=ACCENT)

# Secondary segments
segs = [
    ('Partner / Co-Parent', '"Alex, 36" — earns income, wants\nvisibility not admin work. Enters\nvia household invite.', ACCENT),
    ('Mint Refugees', '20M+ displaced users (Jan 2024)\nseeking free, privacy-respecting\nreplacement.', AMBER),
    ('Budget-Skeptic', '"Jamie, 42" — triggered by financial\nstress. Intimidated by spreadsheets.\nNeeds fast time-to-value.', PURPLE),
    ('Privacy-First Pros', 'Tech, healthcare, legal workers.\nHigh trust bar; willing to pay\nfor privacy guarantees.', GREEN),
]
for i, (name, desc, color) in enumerate(segs):
    x = L(0.5) + i * L(3.1)
    card_box(sl, x, L(3.9), L(2.88), L(1.42))
    box(sl, x, L(3.9), L(2.88), L(0.05), fill=color, line_color=None)
    txt(sl, name, x + L(0.12), L(4.0),  L(2.65), L(0.32), size=12, color=WHITE, bold=True)
    txt(sl, desc, x + L(0.12), L(4.3),  L(2.65), L(0.85), size=10, color=MUTED, wrap=True)

# TAM/SAM/SOM row
tam = [('45M', 'TAM', 'US dual-income households', PURPLE),
       ('12M', 'SAM', 'Actively budgeting households', ACCENT),
       ('150K', 'SOM Y3', 'Paying households (0.4–1.2% of SAM)', GREEN)]
for i, (val, label, sub, color) in enumerate(tam):
    x = L(0.5) + i * L(4.2)
    card_box(sl, x, L(5.5), L(3.95), L(1.12))
    txt(sl, label, x, L(5.56), L(3.95), L(0.28), size=9, color=color, bold=True, align=PP_ALIGN.CENTER)
    txt(sl, val,   x, L(5.82), L(3.95), L(0.5),  size=26, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(sl, sub,   x, L(6.3),  L(3.95), L(0.26), size=9,  color=MUTED, align=PP_ALIGN.CENTER)

add_notes(sl, "Primary persona is Morgan — the Household CFO. She already downloads CSVs. We change nothing about her workflow except making it 6x faster and giving her AI-powered answers. Secondary segments extend reach. TAM/SAM/SOM grounds the market size.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — CUSTOMER PAIN POINTS
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ Customer Pain Points & Challenges', '8 reasons families give up on budgeting')

pains = [
    ('🧩 Fragmented Data',      'Statements scattered across email,\nbank portals, and separate card apps.',    '⏱  2+ hrs/month manual consolidation'),
    ('📋 Manual Overhead',      'Copy-paste into spreadsheets every\nmonth. Abandoned after 2–3 months.',       '🔄  High churn for DIY solutions'),
    ('👤 Individual-First Tools','Mint, YNAB, Copilot assume one\nperson. Partners feel excluded.',             '📉  Low household adoption'),
    ('📉 Unrealistic Budgets',  'Families guess limits with no data.\nBudgets fail by week 2.',                 '😔  Shame → tool abandonment'),
    ('❓ No Conversational Q&A','Can\'t ask "are we on track?"\nMust interpret dense charts.',                 '🧠  Dashboard becomes "set and forget"'),
    ('🔐 Privacy Anxiety',      'Plaid / bank API links feel risky\nafter data breaches.',                     '🚫  30–40% drop-off at bank-link step'),
    ('🔔 Late Accountability',  'Overspending only visible at\nmonth-end — too late to course-correct.',       '🚨  Reactive vs. proactive money mgmt'),
    ('🔁 Double-Counting',      'Credit card payments counted as\nexpenses in both accounts.',                 '🏚  Erodes trust in the tool'),
]
cols, rows = 4, 2
cw, ch = L(3.02), L(1.58)
for idx, (title, desc, cost) in enumerate(pains):
    col, row = idx % cols, idx // cols
    x = L(0.5) + col * (cw + L(0.1))
    y = L(1.72) + row * (ch + L(0.12))
    card_box(sl, x, y, cw, ch)
    box(sl, x, y, L(0.06), ch, fill=RED, line_color=None)
    txt(sl, title, x + L(0.15), y + L(0.1),  cw - L(0.2), L(0.3),  size=10, color=WHITE, bold=True)
    txt(sl, desc,  x + L(0.15), y + L(0.4),  cw - L(0.2), L(0.65), size=10, color=MUTED, wrap=True)
    txt(sl, cost,  x + L(0.15), y + L(1.26), cw - L(0.2), L(0.28), size=9,  color=AMBER)

# JTBD strip
jtbd = ['Consolidate', 'Understand', 'Plan', 'Monitor', 'Align']
jw = L(2.3)
for i, j in enumerate(jtbd):
    jx = L(0.5) + i * (jw + L(0.1))
    box(sl, jx, L(5.1), jw, L(0.32), fill=RGBColor(0x0d, 0x2a, 0x5a), line_color=ACCENT, line_pt=0.5)
    txt(sl, f'{i+1}. {j}', jx + L(0.08), L(5.12), jw - L(0.1), L(0.28), size=10, color=ACCENT, bold=True)

txt(sl, 'Jobs-to-be-Done:', L(0.5), L(4.85), L(3.0), L(0.28), size=9, color=MUTED, bold=True)

add_notes(sl, "Walk the 4×2 grid of pain points. The goal is to make the investor feel the frustration Morgan feels on the 15th of the month. The JTBD strip at the bottom names the five outcomes she is hiring this product to deliver.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — HOW WE SOLVE IT
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ How We Plan to Solve the Problem', 'From chaos to clarity in <30 minutes')

# 5-step flow
steps = [
    ('📥', 'Download', '5 min/account'),
    ('⬆️', 'Upload', 'No credentials'),
    ('🏷️', 'Auto-Categorize', '80%+ auto-tagged'),
    ('🧮', 'Budget Wizard', '50/30/20 from data'),
    ('💬', 'Ask AI', '"Why is dining over?"'),
]
sw = L(1.9)
for i, (icon, title, sub) in enumerate(steps):
    x = L(0.5) + i * (sw + L(0.46))
    card_box(sl, x, L(1.72), sw, L(1.05))
    txt(sl, icon,  x, L(1.8),  sw, L(0.4),  size=20, align=PP_ALIGN.CENTER)
    txt(sl, title, x, L(2.18), sw, L(0.3),  size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(sl, sub,   x, L(2.46), sw, L(0.28), size=9,  color=GREEN,  align=PP_ALIGN.CENTER)
    if i < 4:
        txt(sl, '→', x + sw, L(1.98), L(0.46), L(0.4), size=18, color=ACCENT, align=PP_ALIGN.CENTER)

# Solution table
tbl_data = [
    ('Fragmented data',     'Unified ledger + transfer detection',               'Single timeline; no double-counting'),
    ('Manual overhead',     'CSV/OFX import + saved mappings + dedup',           'Monthly ritual → 20 min vs. 2 hrs'),
    ('Individual-first',    'Household workspace with roles + member tags',       'Built for couples from day one'),
    ('Unrealistic budgets', 'Budget wizard from 3–6 month median spend',         'Grounded in their own data'),
    ('No conversational Q&A','AI assistant via function calling over real DB',   'Real numbers; no hallucination'),
    ('Privacy anxiety',     'File-only import; encrypted at rest; GDPR delete', 'No credentials ever stored'),
]
t = sl.shapes.add_table(len(tbl_data) + 1, 3, L(0.5), L(3.0), W(0.94), L(4.1)).table
for ci, h in enumerate(['Pain', 'Our Solution', 'Why It Works']):
    c = t.cell(0, ci)
    set_cell_fill(c, SURFACE)
    table_cell_text(c, h, size=10, color=MUTED, bold=True)
for ri, (pain, sol, why) in enumerate(tbl_data):
    set_cell_fill(t.cell(ri + 1, 0), CARD)
    set_cell_fill(t.cell(ri + 1, 1), CARD)
    set_cell_fill(t.cell(ri + 1, 2), CARD)
    table_cell_text(t.cell(ri + 1, 0), pain, color=MUTED)
    table_cell_text(t.cell(ri + 1, 1), sol,  color=WHITE)
    table_cell_text(t.cell(ri + 1, 2), why,  color=GREEN)
for ci, w in enumerate([L(1.9), L(5.0), L(5.3)]):
    t.columns[ci].width = w

add_notes(sl, "Walk the 5-step flow — it is the user journey in 20 seconds. Key call-outs in the table: (1) 2 hours → 20 minutes, (2) File-only import = no credentials ever stored, (3) AI uses function calls over real DB = no hallucination.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — KEY FEATURES
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ Key Features', 'Everything families need — nothing they don\'t')

feats = [
    ('🏠', 'Household Workspace',  'Email + Google SSO; invite members with\nOwner / Editor / Viewer roles'),
    ('📤', 'Smart File Import',    'CSV, OFX, QFX; column mapper; saved\ninstitution templates; preview + dedup'),
    ('📊', 'Unified Ledger',       'All accounts in one timeline; bulk edit;\nmember tags; transfer pairing'),
    ('🏷️', 'AI Categorization',   'Family-oriented categories; rules engine;\nlow-confidence review queue'),
    ('🧮', 'Budget Wizard',        '50/30/20 framing + per-category caps\nfrom 3–6 months of real history'),
    ('💬', 'AI Budget Assistant',  'NL Q&A over transactions, budgets, goals\nvia GPT-4o / Gemini function calling'),
    ('🔔', 'Mid-Month Alerts',     'Category pacing widgets; email alerts at\n90% and 100% of budget thresholds'),
    ('💎', 'Freemium Model',       '6 months history free; premium for full\nhistory + CSV/PDF export; no ads'),
]
fw, fh = L(2.98), L(1.28)
for idx, (icon, title, desc) in enumerate(feats):
    col, row = idx % 4, idx // 4
    x = L(0.5) + col * (fw + L(0.14))
    y = L(1.72) + row * (fh + L(0.12))
    card_box(sl, x, y, fw, fh)
    txt(sl, icon,  x + L(0.15), y + L(0.1),  fw - L(0.3), L(0.38), size=20)
    txt(sl, title, x + L(0.15), y + L(0.48), fw - L(0.3), L(0.3),  size=11, color=WHITE, bold=True)
    txt(sl, desc,  x + L(0.15), y + L(0.78), fw - L(0.3), L(0.45), size=9,  color=MUTED, wrap=True)

# Success metrics strip
metrics = [('<30m', 'First dashboard'), ('≥60%', 'Week-1 activation'),
           ('≥80%', 'Auto-categorization'), ('≥40%', '90-day retention'),
           ('≥5%', 'Free → Premium'), ('≥3', 'AI queries/user/mo')]
mw = L(1.96)
for i, (v, k) in enumerate(metrics):
    mx = L(0.5) + i * (mw + L(0.06))
    card_box(sl, mx, L(6.18), mw, L(0.9))
    txt(sl, v, mx, L(6.22), mw, L(0.42), size=18, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
    txt(sl, k, mx, L(6.62), mw, L(0.28), size=9,  color=MUTED,  align=PP_ALIGN.CENTER)

add_notes(sl, "8 feature areas cover the complete household budgeting loop. The AI assistant is the differentiator — every other feature exists in competitors. Bottom strip shows the success metrics we hold ourselves to — these gate Series A.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — COMPETITIVE LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ Competitors in the Market', 'We own the white space no one else occupies')

comp_data = [
    ('⭐ Family Budget Assistant', 'Freemium', '✓ Native (roles)', '✓ Grounded NL Q&A', '✓ Primary path', '✓ MVP default', 'Privacy-first families', True),
    ('Monarch Money',              '$99/yr',   '✓ Couples view',  '✗ Insights only',   '✗',              '✗',             'Mint replacement',      False),
    ('YNAB',                       '$109/yr',  '~ Shared budget', '✗',                 '✗',              '✗',             'ZBB purists',           False),
    ('Copilot',                    '~$95/yr',  '✗ No sharing',    '~ Cat AI only',     '✗',              '✗',             'Apple / design-first',  False),
    ('Empower',                    'Free',     '✗',               '✗',                 '✗',              '✗',             'Net worth tracker',     False),
    ('Rocket Money',               'Freemium', '✗',               '✗',                 '✗',              '✗',             'Subscription cancels',  False),
    ('Goodbudget',                 'Free/$8',  '~ Limited',       '✗',                 '~ Manual entry', '✓',             'Envelope budgeters',    False),
    ('Spreadsheets',               'Free',     '~ DIY only',      '✗',                 '✓',              '✓',             'Power users',           False),
]
ncols = 7
t = sl.shapes.add_table(len(comp_data) + 1, ncols, L(0.4), L(1.62), W(0.94), H(0.66)).table
hdrs = ['Product', 'Price', 'Household Sharing', 'AI Q&A', 'File Import', 'Privacy', 'Best For']
col_widths = [L(2.6), L(0.9), L(1.7), L(1.6), L(1.5), L(1.4), L(1.8)]
for ci, h in enumerate(hdrs):
    c = t.cell(0, ci)
    set_cell_fill(c, SURFACE)
    table_cell_text(c, h, size=9, color=MUTED, bold=True)
for ri, (prod, price, hh, ai, fi, priv, best, is_us) in enumerate(comp_data):
    row_fill = RGBColor(0x0d, 0x1a, 0x38) if is_us else CARD
    for ci, val in enumerate([prod, price, hh, ai, fi, priv, best]):
        c = t.cell(ri + 1, ci)
        set_cell_fill(c, row_fill)
        if ci == 0:
            fcol = ACCENT if is_us else TEXT
        elif val.startswith('✓'):
            fcol = GREEN
        elif val == '✗':
            fcol = RED
        elif val.startswith('~'):
            fcol = AMBER
        else:
            fcol = TEXT
        table_cell_text(c, val, size=9, color=fcol, bold=(ci == 0 and is_us))
for ci, w in enumerate(col_widths):
    t.columns[ci].width = w

# Positioning map (compact)
map_l, map_t, map_w, map_h = L(0.4), L(5.5), W(0.94), L(1.62)
card_box(sl, map_l, map_t, map_w, map_h)
box(sl, map_l, map_t + map_h / 2 - L(0.02), map_w, L(0.03), fill=BORDER, line_color=None)
box(sl, map_l + map_w / 2 - L(0.015), map_t, L(0.03), map_h, fill=BORDER, line_color=None)
txt(sl, '↑ HIGH AUTOMATION + AI',    map_l, map_t + L(0.06), map_w, L(0.25), size=8, color=MUTED, align=PP_ALIGN.CENTER)
txt(sl, '↓ LOW AUTOMATION / MANUAL', map_l, map_t + map_h - L(0.28), map_w, L(0.25), size=8, color=MUTED, align=PP_ALIGN.CENTER)
txt(sl, '← INDIVIDUAL',    map_l + L(0.1), map_t + map_h / 2 - L(0.36), L(2.0), L(0.25), size=8, color=MUTED)
txt(sl, 'HOUSEHOLD-NATIVE →', map_l + map_w - L(2.2), map_t + map_h / 2 - L(0.36), L(2.1), L(0.25), size=8, color=MUTED, align=PP_ALIGN.RIGHT)

players = [
    (0.72, 0.22, '⭐ Family Budget Assistant', ACCENT, True),
    (0.20, 0.28, 'Copilot',    MUTED, False),
    (0.18, 0.72, 'YNAB',       MUTED, False),
    (0.62, 0.68, 'Monarch',    MUTED, False),
    (0.50, 0.80, 'Goodbudget', MUTED, False),
]
for (xp, yp, name, color, is_us) in players:
    px = map_l + int(map_w * xp) - L(0.7)
    py = map_t + int(map_h * yp) - L(0.14)
    box(sl, px, py, L(2.5) if is_us else L(1.5), L(0.3),
        fill=ACCENT if is_us else CARD,
        line_color=ACCENT if is_us else BORDER,
        line_pt=1.0 if is_us else 0.5)
    txt(sl, name, px + L(0.08), py + L(0.04), L(2.35), L(0.22),
        size=8 if not is_us else 9, color=WHITE if is_us else MUTED, bold=is_us)

txt(sl, '★ White space: only player combining household-native + high automation + privacy-safe file import.',
    L(0.4), L(7.16), W(0.93), L(0.3), size=9, color=ACCENT, italic=True)

add_notes(sl, "Read the column patterns: Household Sharing — only Monarch and us. AI Q&A — only us with grounded answers. File Import + Privacy together — only us and Goodbudget, but Goodbudget is manual entry. Our ⭐ row is the only one with all four differentiating checkmarks.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — AI & DATA STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)
label_header(sl, '☑ Existing Data & Models — No Training from Scratch', 'Leverage what exists; fine-tune only where ROI is clear')

layers = [
    (ACCENT, 'Layer 1 — Transaction Categorization',
     'Pre-trained DistilBERT on 68K US bank strings\n(HuggingFace: us-bank-transaction-categories-v2 · 99.9% val accuracy)',
     '📌 MVP: Rules engine first → fine-tuned classifier → review queue for <0.85 confidence. No GPU required.'),
    (PURPLE, 'Layer 2 — AI Budget Q&A (GPT-4o / Gemini)',
     'Foundation LLM + structured function calls:\nget_budget_status · get_transactions · get_spending_summary · get_goal_progress',
     '📌 No fine-tuning needed for MVP. Function-calling is our IP. ~$0.01–0.05/query vs. $0.50+ with raw CSV dumps.'),
    (GREEN,  'Layer 3 — Budget Recommendation Engine',
     'Median/trimmed-mean per category from user\'s own 3–6 month history + 50/30/20 (Needs/Wants/Savings) framing.',
     '📌 No external model needed. Statistically grounded, explainable, and zero incremental cost.'),
    (AMBER,  'Layer 4 — Bank File Parsing',
     'Open-source ofxparse / ofx-js for OFX/QFX. Rule-based column-mapper for CSV with saved institution templates.',
     '📌 Top 10 US bank templates ship in MVP. Community-contributed templates expand coverage in Phase 2.'),
]
for i, (color, title, desc, note) in enumerate(layers):
    y = L(1.72) + i * L(1.25)
    card_box(sl, L(0.5), y, W(0.93), L(1.1))
    box(sl, L(0.5), y, L(0.07), L(1.1), fill=color, line_color=None)
    txt(sl, title, L(0.75), y + L(0.08), W(0.5),  L(0.3),  size=11, color=color, bold=True)
    txt(sl, desc,  L(0.75), y + L(0.38), W(0.5),  L(0.42), size=10, color=TEXT,  wrap=True)
    txt(sl, note,  L(0.75), y + L(0.8),  W(0.5),  L(0.26), size=9,  color=GREEN)

# Phase roadmap
phases = [
    (ACCENT, 'MVP — No Training from Scratch',
     '• Rules engine + pre-trained DistilBERT\n• GPT-4o / Gemini + function calling\n• Statistical budget wizard (median spend)\n• Open-source OFX / CSV parsers'),
    (GREEN,  'Phase 2 — Targeted Fine-Tuning',
     '• Fine-tune classifier on user corrections (opt-in)\n• Merchant normalization (Foursquare + household data)\n• Recurring detection: heuristic → lightweight ML\n• 4.5M+ synthetic transaction dataset (HuggingFace)'),
    (PURPLE, 'Phase 3+ — Optional Expansion',
     '• Household embedding cache for repeat merchants\n• Local / offline small LLM (privacy-first premium tier)\n• Optional Plaid bank link (opt-in, expands TAM)\n• Tax summary AI (accountant export)'),
]
for i, (color, title, items) in enumerate(phases):
    x = L(0.5) + i * L(4.17)
    card_box(sl, x, L(6.82), L(3.98), L(0.5))
    box(sl, x, L(6.82), L(3.98), L(0.22), fill=RGBColor(
        int(color[0] * 0.12 + 0x1a * 0.88),
        int(color[1] * 0.12 + 0x22 * 0.88),
        int(color[2] * 0.12 + 0x35 * 0.88),
    ), line_color=None)
    txt(sl, title, x + L(0.12), L(6.86), L(3.74), L(0.22), size=8, color=color, bold=True)

# Open the phase cards taller if space allows — use tooltip style instead
# Privacy compliance note
txt(sl,
    'Privacy rule: never train on raw user data without opt-in. '
    'Synthetic HuggingFace datasets avoid PII entirely for initial models. '
    'User corrections → anonymized aggregate patterns only.',
    L(0.5), L(7.1), W(0.93), L(0.3), size=9, color=MUTED, italic=True)

add_notes(sl, "Core message: do not start from scratch. Four layers each have a clear 'use existing' recommendation. The function-calling tool layer (Layer 2) is our IP — not the base model. MVP ships with zero model training. Phase 2 fine-tuning is targeted and funded by real user correction data.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — CLOSING / SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
sl = new_slide(prs)

box(sl, L(0), L(0), W(), H(), fill=RGBColor(0x0d, 0x1a, 0x3f), line_color=None)
box(sl, L(0), L(0), W(), H(), fill=BG, line_color=None)

txt(sl, '🏠', W(0.5) - L(0.5), L(1.1), L(1.0), L(1.0), size=40, align=PP_ALIGN.CENTER)
txt(sl, 'Family Budget Assistant', W(0.5) - L(4.5), L(2.2), L(9), L(0.65), size=34, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(sl, 'Family-native  ·  Privacy-safe  ·  AI-powered  ·  No bank credentials ever',
    W(0.5) - L(4.5), L(2.85), L(9), L(0.38), size=13, color=MUTED, align=PP_ALIGN.CENTER)

summary = [
    ('👥', 'Target Customer',    'Household CFO + partner;\n3–8 accounts; privacy-conscious;\nalready downloads CSVs', ACCENT),
    ('😣', 'Pain Points',        '8 pain points; 30–40% bank-link drop-off;\n2 hrs/month manual overhead;\nno conversational access', RED),
    ('🛠', 'Solution',           'File import → unified ledger →\nbudget wizard → AI Q&A;\n<30 min to first dashboard', GREEN),
    ('⚡', 'Key Features',       '8 MVP feature areas; GPT-4o Q&A;\nfreemium model; household roles;\nmid-month pacing alerts', ACCENT),
    ('🏆', 'Competitive Moat',   'Only player with all three pillars:\nfamily-native + file-import-first\n+ grounded AI Q&A', AMBER),
    ('🤖', 'AI & Data Strategy', 'No training from scratch;\npre-trained DistilBERT + GPT-4o\nfunction calling = our IP', PURPLE),
]
sw2 = L(3.75)
for i, (icon, title, desc, color) in enumerate(summary):
    col, row = i % 3, i // 3
    x = L(0.55) + col * (sw2 + L(0.17))
    y = L(3.35) + row * L(1.42)
    card_box(sl, x, y, sw2, L(1.28))
    box(sl, x, y, sw2, L(0.05), fill=color, line_color=None)
    txt(sl, icon,  x + L(0.12), y + L(0.12), L(0.5),       L(0.38), size=16)
    txt(sl, title, x + L(0.62), y + L(0.12), sw2 - L(0.75), L(0.32), size=11, color=color, bold=True)
    txt(sl, desc,  x + L(0.12), y + L(0.5),  sw2 - L(0.2),  L(0.72), size=9,  color=MUTED, wrap=True)

txt(sl, 'saudamini@gmail.com  ·  Family Budget Assistant  ·  2026',
    L(0), L(7.1), W(), L(0.32), size=10, color=BORDER, align=PP_ALIGN.CENTER)

add_notes(sl, "Closing summary. Six sections covered. Each card maps to one slide in the deck. Use this as the recap or leave-behind.")

# ── Save ───────────────────────────────────────────────────────────────────────
prs.save(OUT)
print(f'Saved → {os.path.abspath(OUT)}')
