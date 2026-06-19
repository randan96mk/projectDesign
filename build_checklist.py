import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Production Release Checklist"

# ── Colours ──────────────────────────────────────────────────────────────────
C = {
    "hdr":      "1A1A1A", "hdr_fg":  "FFFFFF",
    "sec1":     "2C2C2C", "sec1_fg": "FFFFFF",   # Pre-Release     – charcoal
    "sec2":     "C94B4B", "sec2_fg": "FFFFFF",   # Workfront       – red
    "sec3":     "B36200", "sec3_fg": "FFFFFF",   # Fusion Common   – dark amber
    "sec4":     "8B5E00", "sec4_fg": "FFFFFF",   # Fusion Watch    – brown-amber
    "sec5":     "5C4000", "sec5_fg": "FFFFFF",   # Fusion Webhook  – dark gold
    "sec6":     "5A2DB5", "sec6_fg": "FFFFFF",   # Adobe I/O       – purple
    "sec7":     "0F4F9E", "sec7_fg": "FFFFFF",   # Planning        – blue
    "sec8":     "0A6644", "sec8_fg": "FFFFFF",   # Validation      – teal
    "sec9":     "7A2E70", "sec9_fg": "FFFFFF",   # Marketo/MCZ     – purple-pink
    "sec10":    "8B4513", "sec10_fg":"FFFFFF",   # Notifications   – brown
    "sec11":    "1B5E8A", "sec11_fg":"FFFFFF",   # Testing         – steel blue
    "sec12":    "1A1A1A", "sec12_fg":"FFFFFF",   # Post-Release    – charcoal
    "sub":      "F0F0F0", "sub_fg":  "2C2C2C",  # Sub-section row
    "row_a":    "FFFFFF", "row_b":   "F8F8F8",  # Data row alternating
    "high":     "FFDEDE", "high_fg": "8B0000",
    "med":      "FFF3CD", "med_fg":  "7A4D00",
    "low":      "DFF0D8", "low_fg":  "1A5C2A",
}

def fill(hex_col):
    return PatternFill("solid", fgColor=hex_col)

def font(bold=False, color="000000", size=10, italic=False):
    return Font(bold=bold, color=color, size=size, italic=italic, name="Calibri")

def border_thin():
    s = Side(border_style="thin", color="D0D0D0")
    return Border(left=s, right=s, top=s, bottom=s)

def align(h="left", v="center", wrap=True):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

# ── Columns ───────────────────────────────────────────────────────────────────
#  A   B          C            D                    E              F              G           H        I       J           K
# [#] [Section] [Sub-Section] [Checklist Item]     [Detail/Notes] [Preview/Stage Ref]  [Prod Ref] [Owner] [Priority] [Status] [Verified By] [Date]
COLS = ["#", "Section", "Sub-Section", "Checklist Item",
        "Detail / Notes", "Preview / Stage Ref", "Prod Ref",
        "Owner", "Priority", "Status", "Verified By", "Date"]
COL_W = [4, 18, 18, 45, 38, 28, 28, 12, 9, 12, 14, 12]

# ── Write header row ──────────────────────────────────────────────────────────
ws.append(COLS)
for ci, (col, w) in enumerate(zip(COLS, COL_W), 1):
    cell = ws.cell(1, ci)
    cell.fill = fill(C["hdr"])
    cell.font = font(bold=True, color=C["hdr_fg"], size=11)
    cell.alignment = align("center")
    cell.border = border_thin()
    ws.column_dimensions[get_column_letter(ci)].width = w

ws.row_dimensions[1].height = 28
ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}1"

# ── Data ──────────────────────────────────────────────────────────────────────
# Row format: (section_key, sub_section, item, detail, stage_ref, prod_ref, owner, priority)
# Special rows: ("SECTION", label, color_key)  →  section header
#               ("SUB", label)                 →  sub-section header

rows = [

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 1 – PRE-RELEASE PREREQUISITES", "sec1"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC1","General","Prod access confirmed – Adobe Workfront","Verify login to PROD WF tenant","Stage WF tenant","Prod WF tenant","Adobe Admin","High"),
("SEC1","General","Prod access confirmed – Workfront Fusion","Verify login to PROD Fusion org","Stage Fusion org","Prod Fusion org","Adobe Admin","High"),
("SEC1","General","Prod access confirmed – Workfront Planning","Verify PROD Planning workspace accessible","Stage Planning","Prod Planning","Adobe Admin","High"),
("SEC1","General","Prod access confirmed – Adobe I/O Runtime","Verify PROD namespace reachable","23294-dxcampaignautomation-stage","14257-918erinrhinoceros","Adobe Admin","High"),
("SEC1","General","Prod access confirmed – SnapLogic","Verify PROD SnapLogic API credentials active","Stage SnapLogic","Prod SnapLogic","Adobe Admin","High"),
("SEC1","General","All PREVIEW/Stage scenarios fully tested and signed off","No open bugs; test sign-off document available","Stage","Prod","Dev Team","High"),
("SEC1","General","IMS / OAuth tokens and API credentials ready for PROD","Store securely; do not reuse Stage tokens","Stage creds","Prod creds","Adobe Admin","High"),
("SEC1","General","Rollback plan documented and approved","Define steps to revert to previous state if go-live fails","–","Prod","Dev Team","High"),
("SEC1","General","Prod deployment window approved and communicated","Agreed downtime window; stakeholders notified","–","Prod","Ops Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 2 – WORKFRONT CONFIGURATION", "sec2"),
# ══════════════════════════════════════════════════════════════════════════════
("SUB","Request Queue & Topics","","","","","",""),
("SEC2","Request Queue","Queue 'EAC Enterprise Marketing & Operations Request Queue - Infosys' exists in PROD","Verify queue is live and accessible by APAC/AMER teams","Stage WF","Prod WF","Adobe Admin","High"),
("SEC2","Request Queue","Queue Topic 'Enterprise Global Campaign Operations Requests' configured","APAC and AMER topics active under the queue","Stage WF","Prod WF","Adobe Admin","High"),

("SUB","Custom Forms","","","","","",""),
("SEC2","Custom Forms","Form: Enterprise Global Campaign Operations Requests-INF active","Issue form; attached to all Campaign Ops requests (#CO #GMOT #MMO)","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","Form: Campaign Orchestration – Profile and Targeting Criteria AMER active","Task-level targeting form for AMER projects","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","Form: Campaign Orchestration – Profile and Targeting Criteria APAC active","Task-level targeting form for APAC projects","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","Form: EAC Enterprise Global Campaign Operations Requests for Tasks-INF active","Task-level request form for all templates","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","Form: Campaign Orchestration – MCZ Resources INF active","MCZ pre-build task form","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","Form: E-Mail Governance Approval DX active","Governance approval task form (Approve / Reject field)","Stage Form","Prod Form","Dev Team","High"),
("SEC2","Custom Forms","All 250+ custom fields verified active via WF Field List report","Run 'DX CO Custom Fields' report in PROD to confirm all fields","Stage Report","Prod Report","Dev Team","High"),

("SUB","Project Templates (4 Templates)","","","","","",""),
("SEC2","Templates","Template: Campaign Orchestration | Email Blast-AMER-INF cloned to PROD","Verify all tasks, forms, owners and task order","Stage Template ID","Prod Template ID","Dev Team","High"),
("SEC2","Templates","Template: Campaign Orchestration | Email Blast-APAC-INF cloned to PROD","","Stage Template ID","Prod Template ID","Dev Team","High"),
("SEC2","Templates","Template: Campaign Orchestration | Newsletter-AMER-INF cloned to PROD","","Stage Template ID","Prod Template ID","Dev Team","High"),
("SEC2","Templates","Template: Campaign Orchestration | Newsletter-APAC-INF cloned to PROD","","Stage Template ID","Prod Template ID","Dev Team","High"),
("SEC2","Templates","All Prod Template Task IDs documented and available for Fusion config","Required for all watch event filters; note IDs per template","Stage Task IDs","Prod Task IDs","Dev Team","High"),
("SEC2","Templates","Monitored task IDs noted: Targeting Criteria, Schedule, Solution & Languages","English, Spanish, Portuguese, Japanese, Chinese Simplified, Traditional, Thai, Korean versions","Stage Task IDs","Prod Task IDs","Dev Team","High"),
("SEC2","Templates","Monitored task IDs noted: Email Governance Approval, Email Program Summary, MCZ Pre-Build Confirmation","Used by watch event filter in scenarios","Stage Task IDs","Prod Task IDs","Dev Team","High"),
("SEC2","Templates","Monitored task IDs noted: Profile and Content parent task IDs","Used by auto-update watch event (profile/content completion)","Stage Task IDs","Prod Task IDs","Dev Team","High"),
("SEC2","Templates","Task ordering and dependencies correct in all 4 PROD templates","Re-verify after cloning; ordering can shift","–","Prod","Dev Team","High"),

("SUB","Teams","","","","","",""),
("SEC2","Teams","APAC Team created in PROD and Team ID noted","Team ID stored for Fusion scenario 01 routing","Stage Team ID","Prod Team ID","Adobe Admin","High"),
("SEC2","Teams","AMER Team created in PROD and Team ID noted","","Stage Team ID","Prod Team ID","Adobe Admin","High"),
("SEC2","Teams","Email Governance Team APAC created and Team ID noted","Used in scenario 06 assignment routing","Stage Team ID","Prod Team ID","Adobe Admin","High"),
("SEC2","Teams","Email Governance Team AMER created and Team ID noted","","Stage Team ID","Prod Team ID","Adobe Admin","High"),
("SEC2","Teams","Ops Team APAC configured in PROD","Used in scenario 07 approval routing","Stage","Prod","Adobe Admin","High"),
("SEC2","Teams","Ops Team AMER configured in PROD","","Stage","Prod","Adobe Admin","High"),

("SUB","Dashboards & Other","","","","","",""),
("SEC2","Dashboards","Email Governance Dashboard APAC live in PROD","Governance team can access and action from dashboard","Stage","Prod","Dev Team","Medium"),
("SEC2","Dashboards","Email Governance Dashboard AMER live in PROD","","Stage","Prod","Dev Team","Medium"),
("SEC2","Other","Portfolio ID confirmed and documented for Fusion configuration","Portfolio ID used in scenario 01 Set Variable module","Stage Portfolio ID","Prod Portfolio ID","Adobe Admin","High"),
("SEC2","Other","Marketer ID (automated user) configured in PROD","Used for future marketer assignments in scenario 01","Stage","Prod","Adobe Admin","High"),
("SEC2","Other","Layouts configured for Marketer and Ops team views","","Stage","Prod","Adobe Admin","Medium"),
("SEC2","Other","Roles configured for APAC and AMER teams","","Stage","Prod","Adobe Admin","Medium"),
("SEC2","Other","Operation Queue project exists in PROD (target for request move on governance approval)","Scenario 07 moves approved request here","Stage Project ID","Prod Project ID","Adobe Admin","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 3 – WORKFRONT FUSION: COMMON SETUP", "sec3"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC3","Connections","Workfront PROD connection created in Fusion","Used by ALL 19 scenarios; must use PROD WF URL","Stage Connection","Prod Connection","Dev Team","High"),
("SEC3","Connections","Workfront Planning PROD connection created in Fusion","Used by scenarios 04, 06, 11, 13, 15","Stage Connection","Prod Connection","Dev Team","High"),
("SEC3","Connections","Adobe I/O Runtime PROD connection configured","IMS auth; used by all I/O module calls","Stage Connection","Prod Connection","Dev Team","High"),
("SEC3","Connections","SnapLogic PROD API credentials stored in Fusion","OAuth token + PROD API URL","Stage Creds","Prod Creds","Dev Team","High"),
("SEC3","Connections","IMS / OAuth token for Adobe I/O auth available in PROD","Separate from Stage token","Stage Token","Prod Token","Adobe Admin","High"),
("SEC3","Datastore","Fusion Datastore configured for PROD (document ID tracking)","Used in scenario 13 to prevent duplicate builds","Stage Datastore","Prod Datastore","Dev Team","High"),
("SEC3","Webhooks","All webhook URLs regenerated in PROD for each webhook scenario","Webhooks generate new URLs in PROD; all callers must be updated","Preview URLs","New Prod URLs","Dev Team","High"),
("SEC3","General","All scenario names renamed from [PREVIEW] to PROD equivalent","Remove [PREVIEW] prefix to avoid confusion","[PREVIEW] prefix","No prefix","Dev Team","Low"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 4 – FUSION: WATCH EVENT SCENARIOS (4 Scenarios)", "sec4"),
# ══════════════════════════════════════════════════════════════════════════════

("SUB","Watch 1: Campaign Orchestration – new Request (APAC,AMER)","","","","","",""),
("SEC4","Watch 1","Scenario cloned from PREVIEW to PROD","","Preview Scenario","Prod Scenario","Dev Team","High"),
("SEC4","Watch 1","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC4","Watch 1","Queue filter: 'DX - Campaign Operation Requests' queue topic configured","Ensure PROD queue name matches exactly","Preview","Prod","Dev Team","High"),
("SEC4","Watch 1","HTTP POST module: webhook URL of scenario 01 updated to PROD URL","Watch event fires → calls scenario 01 webhook","Preview S01 URL","Prod S01 URL","Dev Team","High"),
("SEC4","Watch 1","Scenario activated (ON) in PROD","","–","Prod","Dev Team","High"),
("SEC4","Watch 1","Smoke test: Submit test request → scenario fires and calls scenario 01","Confirm event captured and payload forwarded","–","Prod","Dev Team","High"),

("SUB","Watch 2: Project Tasks Update (APAC, AMER – Single & Multi)","","","","","",""),
("SEC4","Watch 2","Scenario cloned from PREVIEW to PROD","","Preview Scenario","Prod Scenario","Dev Team","High"),
("SEC4","Watch 2","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC4","Watch 2","All monitored template task IDs updated (Targeting Criteria, Schedule, Solution & Languages, Governance, Email Summary, MCZ Pre-Build, all language version tasks)","4 templates × all monitored task IDs","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC4","Watch 2","Scenario activated (ON) in PROD","","–","Prod","Dev Team","High"),
("SEC4","Watch 2","Smoke test: Manually update a monitored task → scenario fires","Confirm scenario detects update across all 4 templates","–","Prod","Dev Team","High"),

("SUB","Watch 3: Project Tasks Update (Profile & Content Auto Update)","","","","","",""),
("SEC4","Watch 3","Scenario cloned from PREVIEW to PROD","","Preview Scenario","Prod Scenario","Dev Team","High"),
("SEC4","Watch 3","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC4","Watch 3","Profile and Content parent task IDs updated for all 4 PROD templates","","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC4","Watch 3","Scenario activated (ON) in PROD","","–","Prod","Dev Team","High"),
("SEC4","Watch 3","Smoke test: Complete all child tasks → parent auto-completes → scenario fires","","–","Prod","Dev Team","High"),

("SUB","Watch 4: Campaign Orchestration – Watch SnapLogic Doc Update","","","","","",""),
("SEC4","Watch 4","Scenario cloned from PREVIEW to PROD","","Preview Scenario","Prod Scenario","Dev Team","High"),
("SEC4","Watch 4","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC4","Watch 4","MCZ Pre-Build Confirmation task document section filter configured for PROD","Watches for SnapLogic-created document versions","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC4","Watch 4","HTTP module: webhook URL of scenario 15 updated to PROD URL","","Preview S15 URL","Prod S15 URL","Dev Team","High"),
("SEC4","Watch 4","Scenario activated (ON) in PROD","","–","Prod","Dev Team","High"),
("SEC4","Watch 4","Smoke test: Document version created on MCZ Pre-Build task → scenario fires","","–","Prod","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 5 – FUSION: WEBHOOK SCENARIOS (15 Scenarios)", "sec5"),
# ══════════════════════════════════════════════════════════════════════════════

("SUB","Scenario 00 – External Lookup Language Selection","","","","","",""),
("SEC5","Scen 00","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 00","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 00","Template task IDs updated for APAC and AMER Single CTA templates (language extraction)","Used to build language dropdown values","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 00","Webhook URL updated in Request Form External Lookup configuration","External lookup on request form must point to PROD webhook","Preview Webhook","Prod Webhook","Dev Team","High"),
("SEC5","Scen 00","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 00","Smoke test: Open request form → Language dropdown populates correctly for APAC and AMER","","–","Prod","Dev Team","High"),

("SUB","Scenario 01 – New Request to Marketer & Operations Project","","","","","",""),
("SEC5","Scen 01","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 01","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 01","APAC and AMER Team IDs updated in Set Variable module","","Preview Team IDs","Prod Team IDs","Dev Team","High"),
("SEC5","Scen 01","Portfolio ID updated in Set Variable module","","Preview Portfolio ID","Prod Portfolio ID","Dev Team","High"),
("SEC5","Scen 01","All 4 project template IDs updated in Set Variable module","","Preview Template IDs","Prod Template IDs","Dev Team","High"),
("SEC5","Scen 01","Base URL updated to PROD Workfront URL (for navigation links in update messages)","","Preview Base URL","Prod Base URL","Dev Team","High"),
("SEC5","Scen 01","Marketer ID updated","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 01","APAC and AMER team owner routing updated with PROD team owner data","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 01","HTTP module: webhook URL of scenario 02 updated to PROD URL","","Preview S02 URL","Prod S02 URL","Dev Team","High"),
("SEC5","Scen 01","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 01","Smoke test: Request submitted → PROD project created, correct template and owner assigned","","–","Prod","Dev Team","High"),

("SUB","Scenario 02 – Request Content Mapping to Task","","","","","",""),
("SEC5","Scen 02","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 02","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 02","APAC-specific targeting field mappings verified (verticals, personas, roles, GTM segment, POI, etc.)","All fields in APAC update module mapped to correct PROD task form fields","Preview","Prod","Dev Team","High"),
("SEC5","Scen 02","AMER-specific targeting field mappings verified (NOAM/LATAM segments, Product Buying Group, industry, suppressions, etc.)","All fields in AMER update module mapped correctly","Preview","Prod","Dev Team","High"),
("SEC5","Scen 02","HTTP module: webhook URL of scenario 04 (Planning update) updated to PROD URL","","Preview S04 URL","Prod S04 URL","Dev Team","High"),
("SEC5","Scen 02","Language task cancellation logic verified – unused language tasks set to Cancelled","All language tasks EXCEPT selected language marked Cancelled at 100%","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 02","Draft.js HTML conversion module functional in PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 02","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 02","Smoke test: Request converted → language task updated, unused tasks cancelled","","–","Prod","Dev Team","High"),

("SUB","Scenario 03 – New Request Overview","","","","","",""),
("SEC5","Scen 03","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 03","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 03","Adobe I/O overviewSummary endpoint updated to PROD URL","Preview: /23294-dxcampaignautomation-stage/v1/overviewsummary","Stage: .../overviewsummary","Prod: /14257-918erinrhinoceros/v1/overviewSummary","Dev Team","High"),
("SEC5","Scen 03","HTTP module: webhook URL calling scenario 05 (validation) updated to PROD URL","","Preview S05 URL","Prod S05 URL","Dev Team","High"),
("SEC5","Scen 03","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 03","Smoke test: Overview generated and posted on Issue, Project, and Language task","","–","Prod","Dev Team","High"),

("SUB","Scenario 04 – Watch Updates on Projects & Tasks (Marketers & Ops)","","","","","",""),
("SEC5","Scen 04","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 04","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 04","Workfront Planning connection updated to PROD","","Preview Planning Conn","Prod Planning Conn","Dev Team","High"),
("SEC5","Scen 04","Requests Planning table ID updated in all modules","","Preview Table ID","Prod Table ID","Dev Team","High"),
("SEC5","Scen 04","Campaign Request Data Planning table ID updated in all modules","","Preview Table ID","Prod Table ID","Dev Team","High"),
("SEC5","Scen 04","Draft.js HTML conversion for email body functional","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 04","All router filters and template task IDs updated","","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 04","HTTP module: webhook URL calling scenario 05 updated to PROD URL","","Preview S05 URL","Prod S05 URL","Dev Team","High"),
("SEC5","Scen 04","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 04","Smoke test: Planning records created and updated on request conversion","","–","Prod","Dev Team","High"),

("SUB","Scenario 05 – Marketer Project Tasks Validation","","","","","",""),
("SEC5","Scen 05","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 05","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 05","Workfront Planning connection updated (Field List table)","","Preview Planning Conn","Prod Planning Conn","Dev Team","High"),
("SEC5","Scen 05","All template task IDs updated in router filters (Targeting, Content, Language, Profile, Governance IDs across all 4 templates)","4 templates × all task types","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 05","Webhook URL of scenario 05.1 updated to PROD URL in HTTP module","","Preview S05.1 URL","Prod S05.1 URL","Dev Team","High"),
("SEC5","Scen 05","Webhook URL of scenario 06 updated to PROD URL in HTTP module","","Preview S06 URL","Prod S06 URL","Dev Team","High"),
("SEC5","Scen 05","APJ SFDC task template IDs updated in APAC sub-route","Used for APAC Salesforce campaign ID generation = Yes flow","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 05","Email Governance template task IDs updated","","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 05","Profile and Content task IDs updated for completion aggregation check","Must equal 2 completed tasks before governance trigger fires","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 05","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 05","Smoke test: Task update → change tracked, validation triggered, correct route selected","","–","Prod","Dev Team","High"),

("SUB","Scenario 05.1 – Validation Summary","","","","","",""),
("SEC5","Scen 05.1","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 05.1","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 05.1","Workfront Planning connections updated (Validation_rules table + Field List table)","","Preview Table IDs","Prod Table IDs","Dev Team","High"),
("SEC5","Scen 05.1","Adobe I/O validationSummary endpoint updated to PROD URL","Preview: /23294-.../v1/validationsummary","Stage: .../validationsummary","Prod: /14257-918erinrhinoceros/v1/validationSummary","Dev Team","High"),
("SEC5","Scen 05.1","Template task IDs updated (Target Criteria, Language Content, Email Governance for all 4 templates)","Determines route taken (targeting vs content vs governance)","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 05.1","Sleep guards (3-second) retained before Planning table reads","Required to avoid race conditions on Planning record retrieval","Preview","Prod","Dev Team","Medium"),
("SEC5","Scen 05.1","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 05.1","Smoke test: Validation runs → Critical issue blocks task at 50%; Non-critical posts advisory note","","–","Prod","Dev Team","High"),

("SUB","Scenario 06 – Overall Summary & Email Governance Assignment","","","","","",""),
("SEC5","Scen 06","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 06","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 06","Workfront Planning connection updated (Field List table)","","Preview Planning Conn","Prod Planning Conn","Dev Team","High"),
("SEC5","Scen 06","Email Governance Team APAC ID updated","","Preview Team ID","Prod Team ID","Dev Team","High"),
("SEC5","Scen 06","Email Governance Team AMER ID updated","","Preview Team ID","Prod Team ID","Dev Team","High"),
("SEC5","Scen 06","Email Governance template task IDs updated for all 4 templates","","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 06","Adobe I/O overAllSummary endpoint updated to PROD URL","","Stage: Stage endpoint","Prod: /14257-918erinrhinoceros/v1/overAllSummary","Dev Team","High"),
("SEC5","Scen 06","Email Governance assignee notification HTML message reviewed for PROD","Verify links and team names are correct for PROD","Preview","Prod","Dev Team","Medium"),
("SEC5","Scen 06","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 06","Smoke test: All tasks complete → summary posted, governance team assigned and notified by region","","–","Prod","Dev Team","High"),

("SUB","Scenario 07 – Email Governance Approval","","","","","",""),
("SEC5","Scen 07","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 07","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 07","APAC and AMER Ops team IDs updated","","Preview Team IDs","Prod Team IDs","Dev Team","High"),
("SEC5","Scen 07","Pre-check, Email Summary, Build SFDC template task IDs updated for all 4 templates","Sub-routes A, B, C require PROD task IDs","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 07","Language content task IDs and APJ SFDC build task IDs updated","Used for APAC campaign with SF ID generation = Yes","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 07","Operation Queue project ID updated (target for approved request move)","","Preview Project ID","Prod Project ID","Dev Team","High"),
("SEC5","Scen 07","Email Governance Approval template task IDs updated","","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 07","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 07","Smoke test (Approval): Governance approves → project moved to Ops Queue, marketer notified","","–","Prod","Dev Team","High"),
("SEC5","Scen 07","Smoke test (Rejection): Governance rejects → project status = Cancelled, marketer notified","","–","Prod","Dev Team","High"),
("SEC5","Scen 07","Corner case: Governance marks task complete without approval value → task reset to New","Filter: status = CPL but Approval field empty → revert to New","Preview","Prod","Dev Team","High"),

("SUB","Scenario 08 – Marketer Access Revoke after Email Governance Approval","","","","","",""),
("SEC5","Scen 08","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 08","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 08","Targeting and Content task IDs updated for access revocation scope","Only completed Targeting + Content tasks affected; not governance/build tasks","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 08","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 08","Smoke test: Post-approval → marketer access set to VIEW on completed content/targeting tasks","","–","Prod","Dev Team","High"),

("SUB","Scenario 11 – Email Program Summary Changes","","","","","",""),
("SEC5","Scen 11","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 11","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 11","Workfront Planning connection updated","","Preview Planning Conn","Prod Planning Conn","Dev Team","High"),
("SEC5","Scen 11","Email Program Summary template task IDs updated for all 4 templates","Webhook filter on this task ID","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 11","Email Governance task ID filter updated","Route 1 checks if Email Gov is Complete before proceeding","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 11","Program Shell Planning table connected to PROD (region, CTA type, gated/ungated, sub-region mapping)","Japan sub-region handled separately","Preview Table ID","Prod Table ID","Dev Team","High"),
("SEC5","Scen 11","MCZ Program Name and Folder name build logic verified in Fusion (built from Requests Planning table)","Regex and string construction rules match PROD naming conventions","Preview","Prod","Dev Team","High"),
("SEC5","Scen 11","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 11","Smoke test: Email Program Summary task completes → MCZ pre-build fields (Shell, Name, Folder) populated in task form","","–","Prod","Dev Team","High"),

("SUB","Scenario 12 – MCZ Pre-Build Changes","","","","","",""),
("SEC5","Scen 12","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 12","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 12","MCZ Pre-Build Confirmation task IDs updated for all 4 templates","Webhook filter on MCZ Program Shell, Program Name, Program Folder field changes","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 12","Sync to Issue and Task custom form verified for PROD field names","Route 1: template changes; Route 2: field changes (Shell, Name, Folder)","Preview","Prod","Dev Team","High"),
("SEC5","Scen 12","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 12","Smoke test: Update MCZ fields in task → synced to Issue record and task comments","","–","Prod","Dev Team","High"),

("SUB","Scenario 13 – MCZ Build JSON","","","","","",""),
("SEC5","Scen 13","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 13","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 13","Workfront Planning connections updated (Requests, Campaign Request Data, Tokens, MCZ Sync Constants tables)","4 separate Planning connections required","Preview Table IDs","Prod Table IDs","Dev Team","High"),
("SEC5","Scen 13","MCZ Build template task IDs updated for all 4 templates","Main filter: newState.status = CPL AND templateTask matches one of 4 IDs","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 13","Adobe I/O mczSyncObject endpoint updated to PROD URL","","Stage: .../mczSyncObject","Prod: /14257-918erinrhinoceros/v1/mczSyncObject","Dev Team","High"),
("SEC5","Scen 13","Fusion Datastore updated to PROD datastore for document ID dedup tracking","overwrite: false prevents duplicate builds","Preview Datastore","Prod Datastore","Dev Team","High"),
("SEC5","Scen 13","Document upload to MCZ Pre-Build Confirmation task section verified","Document created in PROD WF task document section","Preview","Prod","Dev Team","High"),
("SEC5","Scen 13","HTTP module: webhook URL of scenario 14 updated to PROD URL","","Preview S14 URL","Prod S14 URL","Dev Team","High"),
("SEC5","Scen 13","Prerequisite guard (Sub-Route B) task IDs updated","Guards against out-of-sequence build task completion","Preview Task IDs","Prod Task IDs","Dev Team","High"),
("SEC5","Scen 13","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 13","Smoke test: MCZ Build task marked complete → JSON assembled, uploaded as doc, notification posted on task","","–","Prod","Dev Team","High"),

("SUB","Scenario 14 – SnapLogic API Call","","","","","",""),
("SEC5","Scen 14","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 14","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 14","SnapLogic PROD API URL configured in HTTP Module 2","Verify with SnapLogic team","Preview API URL","Prod API URL","Dev Team","High"),
("SEC5","Scen 14","IMS/OAuth PROD credentials configured in HTTP Module 1 (authentication)","","Preview Creds","Prod Creds","Dev Team","High"),
("SEC5","Scen 14","Document download module connected to PROD Workfront","Binary → string conversion functional","Preview","Prod","Dev Team","High"),
("SEC5","Scen 14","syncLevel filter verified (only payloads with syncLevel attribute proceed)","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 14","Error handler for invalid JSON document format active","","Preview","Prod","Dev Team","Medium"),
("SEC5","Scen 14","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 14","Smoke test: Document ID received → document fetched, parsed, SnapLogic PROD API called","","–","Prod","Dev Team","High"),

("SUB","Scenario 15 – SnapLogic / Marketo References","","","","","",""),
("SEC5","Scen 15","Scenario cloned to PROD","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 15","Workfront connection updated to PROD","","Preview WF Conn","Prod WF Conn","Dev Team","High"),
("SEC5","Scen 15","Workfront Planning connection updated (Requests table – Sync Status field)","","Preview Table ID","Prod Table ID","Dev Team","High"),
("SEC5","Scen 15","Adobe I/O processResponse endpoint updated to PROD URL","","Stage: Stage endpoint","Prod: /14257-918erinrhinoceros/v1/processResponse","Dev Team","High"),
("SEC5","Scen 15","Success route: Marketo Program URL and Folder URL extraction verified","Links must navigate to PROD Marketo","Preview","Prod","Dev Team","High"),
("SEC5","Scen 15","Error routes: All 5 types handled (parent folder not found, already exists, search key failure, cache, missing folder/program name)","Each error type has dedicated logic path","Preview","Prod","Dev Team","High"),
("SEC5","Scen 15","On error: Task status reset to In Progress in Requests table for retry","","Preview","Prod","Dev Team","High"),
("SEC5","Scen 15","Scenario activated (ON)","","–","Prod","Dev Team","High"),
("SEC5","Scen 15","Smoke test (Success): SnapLogic response received → Marketo links posted on project, Planning Sync Status updated","","–","Prod","Dev Team","High"),
("SEC5","Scen 15","Smoke test (Error): Error response → error details posted, task reset to In Progress","","–","Prod","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 6 – ADOBE I/O RUNTIME ACTIONS (5 Actions)", "sec6"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC6","General","All 5 actions deployed under package 'fusion-dev' in PROD Adobe I/O namespace","Package name must be fusion-dev","Namespace: 23294-dxcampaignautomation-stage","Namespace: 14257-918erinrhinoceros","Adobe Admin","High"),
("SEC6","General","require-adobe-auth: true confirmed on all 5 actions in PROD","Security requirement; do not deploy without auth","Stage config","Prod config","Adobe Admin","High"),

("SUB","Action 1 – validationSummary","","","","","",""),
("SEC6","validationSummary","Action deployed and PROD endpoint active","","Stage: /23294-.../v1/validationsummary","Prod: /14257-918erinrhinoceros/v1/validationSummary","Dev Team","High"),
("SEC6","validationSummary","Test with APAC payload: Subject (≤90 chars), Preview Text (40–130), SFDC ID (^701[A-Za-z0-9]{15}$), CTA URL (HTTPS), Banner Image, Launch Date (business days)","All 6 validation types must return correct results","Stage","Prod","Dev Team","High"),
("SEC6","validationSummary","Test with AMER payload: SFDC Internal Campaign ID, Marketing Hub URL, NOAM/LATAM targeting fields","","Stage","Prod","Dev Team","High"),
("SEC6","validationSummary","CTA URL parameter check: s_iid and s_rtid mandatory; trackingid, mv, click advisory; differs by region","Verify APAC vs AMERICAS logic correctly applied","Stage","Prod","Dev Team","High"),
("SEC6","validationSummary","Multi-CTA validation: all required fields checked for each CTA section (1–5) based on numberOfCTAs value","Empty field check across all sections","Stage","Prod","Dev Team","High"),
("SEC6","validationSummary","Response: Critical Issues vs Recommendations split correctly; HTML summary returned","","Stage","Prod","Dev Team","High"),

("SUB","Action 2 – overAllSummary","","","","","",""),
("SEC6","overAllSummary","Action deployed and PROD endpoint active","","Stage: Stage endpoint","Prod: /14257-918erinrhinoceros/v1/overAllSummary","Dev Team","High"),
("SEC6","overAllSummary","Test with full campaign field payload → formatted HTML summary output verified","Summary posted as Workfront project update","Stage","Prod","Dev Team","High"),

("SUB","Action 3 – overviewSummary","","","","","",""),
("SEC6","overviewSummary","Action deployed and PROD endpoint active","","Stage: /23294-.../v1/overviewsummary","Prod: /14257-918erinrhinoceros/v1/overviewSummary","Dev Team","High"),
("SEC6","overviewSummary","Test with Issue + Project + Language content data → overview generated and returned","Overview posted on Issue, Project and Language task","Stage","Prod","Dev Team","High"),

("SUB","Action 4 – mczSyncObject","","","","","",""),
("SEC6","mczSyncObject","Action deployed and PROD endpoint active","","Stage: /23294-.../v1/mczSyncObject","Prod: /14257-918erinrhinoceros/v1/mczSyncObject","Dev Team","High"),
("SEC6","mczSyncObject","Test with full payload (request data + campaign data + program shell + tokens + sync constants) → transferSet JSON returned","","Stage","Prod","Dev Team","High"),
("SEC6","mczSyncObject","Token matching: request fields matched to token definitions, then campaign data fields matched; merged into token array","Sub-routes 1, 2, 4 logic verified","Stage","Prod","Dev Team","High"),
("SEC6","mczSyncObject","APAC tokens verified: 77 tokens across CTA sections 1–5 generated correctly","Tokens S.No 1–77 from documentation","Stage","Prod","Dev Team","High"),
("SEC6","mczSyncObject","AMER tokens verified: same 77 tokens with AMER-specific values","","Stage","Prod","Dev Team","High"),

("SUB","Action 5 – processResponse","","","","","",""),
("SEC6","processResponse","Action deployed and PROD endpoint active","","Stage: Stage endpoint","Prod: /14257-918erinrhinoceros/v1/processResponse","Dev Team","High"),
("SEC6","processResponse","Success response: Marketo Program URL and Folder URL extracted and returned correctly","Links to PROD Marketo program and folder","Stage","Prod","Dev Team","High"),
("SEC6","processResponse","Error response: all 5 error types handled with descriptive output and next steps","Parent folder not found, already exists, search key failure, cache, missing name","Stage","Prod","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 7 – WORKFRONT PLANNING TABLES", "sec7"),
# ══════════════════════════════════════════════════════════════════════════════

("SUB","Core Tables","","","","","",""),
("SEC7","Core","Requests Table exists in PROD Planning workspace","Primary campaign record; central data source for Fusion scenarios","Stage","Prod","Dev Team","High"),
("SEC7","Core","Requests Table: all key fields present (Request ID, WF issue ID, project ID, campaign launch date, targeting criteria, POI details, fiscal details, Campaign Request Data record reference)","","Stage","Prod","Dev Team","High"),
("SEC7","Core","Campaign Request Data Table exists in PROD","One record per request × language combination","Stage","Prod","Dev Team","High"),
("SEC7","Core","Campaign Request Data Table: all CTA content fields present for CTA sections 1–5 (email subject, headline, body, CTA text, CTA URL, image, SFDC fields)","","Stage","Prod","Dev Team","High"),
("SEC7","Core","Field List Table exists and populated in PROD","Field Name, Label, Type, Region, Description, Tokens, Planning Table references; used by scenarios 05, 05.1, 06","Stage","Prod","Dev Team","High"),
("SEC7","Core","Tokens Table populated in PROD – all 77 tokens present","Token names, types, planning field mappings, ref/ver metadata","Stage","Prod","Dev Team","High"),
("SEC7","Core","Program Shell Table populated in PROD with correct shell mapping matrix","Region (APAC/AMER), CTA type (single/multi), gated/ungated, sub-region (Japan) combinations covered","Stage","Prod","Dev Team","High"),
("SEC7","Core","Program Shell mapping verified for APAC: all sub-region and gating type combinations","","Stage","Prod","Ops Team","High"),
("SEC7","Core","Program Shell mapping verified for AMER: all combinations","","Stage","Prod","Ops Team","High"),
("SEC7","Core","MCZ Sync Constants Table populated with correct feature toggle values","Program name replacement, folder name replacement flags configured correctly","Stage","Prod","Dev Team","High"),
("SEC7","Core","POI List Table populated (all Adobe products, DB values, token attributes)","Used for POI mapping and token generation","Stage","Prod","Dev Team","High"),
("SEC7","Core","Fiscal Table populated with Adobe fiscal calendar data (FY, fiscal quarter, fiscal month)","Based on campaign launch date → fiscal values derived and passed to MCZ as tokens","Stage","Prod","Dev Team","High"),
("SEC7","Core","Marketo Fields Table populated (internal Fusion logic reference)","","Stage","Prod","Dev Team","Medium"),
("SEC7","Core","Marketo Field References Table populated (product labels, DB values, Marketo mappings, industry classifications)","","Stage","Prod","Dev Team","High"),

("SUB","Lookup Tables (11 Tables)","","","","","",""),
("SEC7","Lookup","Lookup: Solutions – all solution abbreviations and attributes populated","Solution abbreviations used in token generation and naming","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Target Contact Regions – all region codes present","","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Target Contact Country – all country codes and abbreviations present","Country mapped to country code for token generation","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Target Contact Language – all APAC and AMER languages present","Language codes used for task creation and token values","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Target Contact MarketArea – populated","","Stage","Prod","Dev Team","Medium"),
("SEC7","Lookup","Lookup: Target Company Industry – all industry verticals present","Used in targeting criteria and token generation","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Target Contact Sub Region – all sub-regions for APAC and AMER","","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Teams – all team names and routing codes present","","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Validation_Types – all validation type rules present","Regex and rule metadata used by validationSummary action","Stage","Prod","Dev Team","High"),
("SEC7","Lookup","Lookup: Users – user list populated","","Stage","Prod","Dev Team","Medium"),
("SEC7","Lookup","Lookup: Business Unit – all business units present","","Stage","Prod","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 8 – VALIDATION RULES", "sec8"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC8","Rules","Email SFDC Campaign ID rule loaded","Regex: ^701[A-Za-z0-9]{15}$  |  Advice: Must start with 7011 or 701Ke","Stage","Prod","Dev Team","High"),
("SEC8","Rules","Preview Text length rule loaded","Regex: ^.{40,130}$  |  40–130 characters","Stage","Prod","Dev Team","High"),
("SEC8","Rules","Subject line length rule loaded","Regex: ^.{0,89}$  |  Max 90 characters","Stage","Prod","Dev Team","High"),
("SEC8","Rules","Email CTA Link format rule loaded","Regex: ^$|^(https?:\\/\\/)[^\\s]+$  |  Valid HTTPS URL","Stage","Prod","Dev Team","High"),
("SEC8","Rules","SFDC Internal Campaign ID rule loaded","Regex: ^701[A-Za-z0-9]{15}$  |  18 chars, starts 7011/701Ke","Stage","Prod","Dev Team","High"),
("SEC8","Rules","Banner Image URL format rule loaded","Regex: ^$|^(https?:\\/\\/)[^\\s]+$  |  Valid HTTPS URL","Stage","Prod","Dev Team","High"),
("SEC8","Rules","Marketing Hub URL format rule loaded","Regex: ^$|^(https?:\\/\\/)[^\\s]+$  |  Valid HTTPS URL","Stage","Prod","Dev Team","High"),
("SEC8","Rules","CTA URL parameter validation active: s_iid, s_rtid mandatory; trackingid, mv, click advisory by region","Validated per region (AMERICAS vs APAC) inside validationSummary action","Stage","Prod","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 9 – MARKETO TOKENS & MCZ", "sec9"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC9","Tokens","All 77 tokens verified in PROD Marketo Program Shell – APAC","Tokens created at 100% MCZ Pre-Build task completion","Stage MCZ","Prod MCZ","Ops Team","High"),
("SEC9","Tokens","All 77 tokens verified in PROD Marketo Program Shell – AMER","","Stage MCZ","Prod MCZ","Ops Team","High"),
("SEC9","Tokens","Common tokens S.No 1–33 verified (coded_folder_name, Fiscal_FY, Fiscal_M, Fiscal_Q, Hardcoded POI, POI, Program Shell Abbreviation, Region, Sub Region, Request ID, Scheduled Date, Solutions, Solutions Abbreviations, From Name, From Address, Reply-To, Language, Email Subject, Preview Text, Headline, Banner Image, Email Body, CTA Text, CTA Link, SFDC IDs, click)","See token table in technical documentation","Stage","Prod","Ops Team","High"),
("SEC9","Tokens","CTA section tokens 2–5 verified (Email Headline, Body, Image, CTA Text, CTA Link, SFDC Vehicle/Internal Campaign ID, SFDC Offer ID, click per section)","Tokens S.No 34–73; one set per additional CTA section","Stage","Prod","Ops Team","High"),
("SEC9","Tokens","APAC-specific tokens auto-created on MCZ provisioning verified","","Stage MCZ","Prod MCZ","Ops Team","High"),
("SEC9","Tokens","AMER-specific tokens auto-created on MCZ provisioning verified","","Stage MCZ","Prod MCZ","Ops Team","High"),
("SEC9","MCZ","SnapLogic PROD API confirmed connected to Marketo PROD (not sandbox)","Critical: confirm with SnapLogic team before go-live","Stage API","Prod API","Ops Team","High"),
("SEC9","MCZ","SnapLogic document retrieval confirmed from PROD Workfront document section","Document ID lookup must resolve to PROD WF docs","Stage","Prod","Ops Team","High"),
("SEC9","MCZ","Marketo PROD folder structure (program folders, shells) pre-verified","Ensure destination folders exist before first provisioning","Stage MCZ","Prod MCZ","Ops Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 10 – NOTIFICATION EMAILS", "sec10"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC10","Emails","New Request Submitted: marketer receives confirmation email with request + project details","Triggered after scenario 01 project creation","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Language Task Update: marketer notified after language-specific task created in project","Triggered by scenario 02","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Validation Summary: marketer receives validation result notification; also posted in project activity","Triggered by scenario 05.1","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Assignment to Email Governance Team: correct regional team (APAC or AMER) notified with required action","Triggered by scenario 06","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Email Governance Task Completion: marketer notified of approval; content change no longer allowed after this point","Triggered by scenario 07","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Pre-Build Confirmation: Email Governance Team receives build details and required approval actions","Triggered after Email Program Summary task completion (scenario 11)","Stage","Prod","Dev Team","High"),
("SEC10","Emails","Final MCZ Build Notification: confirmation sent after successful MCZ build","Triggered by scenario 15 success route","Stage","Prod","Dev Team","High"),
("SEC10","Emails","All email notification links (project URLs, task URLs) point to PROD Workfront","Base URL must use PROD WF domain","Preview Base URL","Prod Base URL","Dev Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 11 – INTEGRATION & END-TO-END TESTING", "sec11"),
# ══════════════════════════════════════════════════════════════════════════════

("SUB","E2E-01: APAC Single CTA – Full Flow","","","","","",""),
("SEC11","E2E-01","Submit APAC Single CTA request → correct project template selected (Email Blast-APAC-INF)","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Language dropdown populates APAC languages only (scenario 00 external lookup)","","–","Prod","QA Team","High"),
("SEC11","E2E-01","APAC-specific targeting criteria fields mapped to task form (verticals, roles, personas, GTM segment, POI)","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Unused language tasks set to Cancelled; selected language task active","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Overview generated and posted on Issue, Project, and Language task","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Validation summary posted on task (no critical errors in clean test)","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Email Governance Team APAC assigned and notified","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Governance approves → project moved to Ops Queue, marketer notified, access revoked to VIEW","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Email Program Summary task completes → MCZ Pre-Build data (Shell, Name, Folder) populated in task form","","–","Prod","QA Team","High"),
("SEC11","E2E-01","MCZ Build JSON assembled, uploaded as document to MCZ Pre-Build task section, notification posted","","–","Prod","QA Team","High"),
("SEC11","E2E-01","SnapLogic PROD API called with correct document ID","","–","Prod","QA Team","High"),
("SEC11","E2E-01","Marketo PROD: program shell created with all 77 tokens correctly populated","","–","Prod","QA Team","High"),
("SEC11","E2E-01","SnapLogic success response → Marketo Program URL posted on project, Planning Sync Status updated to success","","–","Prod","QA Team","High"),

("SUB","E2E-02: APAC Multi-CTA (3 CTAs)","","","","","",""),
("SEC11","E2E-02","Submit APAC Multi-CTA request selecting 3 CTAs → all 3 CTA content sections mapped to task form","","–","Prod","QA Team","High"),
("SEC11","E2E-02","Validation: CTA URL parameters (s_iid, s_rtid) validated for all 3 CTA URLs","","–","Prod","QA Team","High"),
("SEC11","E2E-02","Marketo: token sections 2 and 3 (CTA -2, CTA -3) generated in PROD program shell","","–","Prod","QA Team","High"),
("SEC11","E2E-02","Full flow to MCZ success verified end-to-end","","–","Prod","QA Team","High"),

("SUB","E2E-03: AMER Single CTA – Full Flow","","","","","",""),
("SEC11","E2E-03","Submit AMER Single CTA request → correct project template selected (Email Blast-AMER-INF)","","–","Prod","QA Team","High"),
("SEC11","E2E-03","Enterprise GTM Segments field visible and mapped correctly (AMER only)","","–","Prod","QA Team","High"),
("SEC11","E2E-03","AMER-specific targeting fields mapped (NOAM/LATAM segments, Product Buying Group, industry, suppressions, GM-SOR)","","–","Prod","QA Team","High"),
("SEC11","E2E-03","AMER language dropdown populates AMER-specific languages only","","–","Prod","QA Team","High"),
("SEC11","E2E-03","Full flow to MCZ success verified end-to-end","","–","Prod","QA Team","High"),

("SUB","E2E-04: AMER Multi-CTA","","","","","",""),
("SEC11","E2E-04","Submit AMER Multi-CTA → multi-CTA token sections 2–5 generated correctly in Marketo PROD","","–","Prod","QA Team","High"),
("SEC11","E2E-04","All AMER-specific fields validated (NOAM/LATAM Account Segment, Product Buying Group, Adobe Department, Job Level)","","–","Prod","QA Team","High"),

("SUB","E2E-05: Email Governance Rejection","","","","","",""),
("SEC11","E2E-05","Governance rejects campaign → project status set to Cancelled","","–","Prod","QA Team","High"),
("SEC11","E2E-05","Marketer receives rejection notification with reason","","–","Prod","QA Team","High"),
("SEC11","E2E-05","No MCZ provisioning triggered after rejection","","–","Prod","QA Team","High"),

("SUB","E2E-06: Validation Critical Failure","","","","","",""),
("SEC11","E2E-06","Submit with invalid SFDC ID → task flagged at 50% (blocked), marketer notified with correction link","","–","Prod","QA Team","High"),
("SEC11","E2E-06","Submit with invalid CTA URL (no HTTPS) → critical flag raised, task blocked","","–","Prod","QA Team","High"),
("SEC11","E2E-06","Non-critical issue (advisory) → soft note posted, task NOT blocked","","–","Prod","QA Team","High"),

("SUB","E2E-07: SnapLogic Error Responses","","","","","",""),
("SEC11","E2E-07","Error 'parent folder not found' → error details posted on project, task reset to In Progress in Planning","","–","Prod","QA Team","High"),
("SEC11","E2E-07","Error 'search key failure' → error handled, Planning Sync Status updated to error","","–","Prod","QA Team","High"),
("SEC11","E2E-07","Error 'missing folder name or program name' → descriptive error with corrective action posted","","–","Prod","QA Team","High"),

("SUB","E2E-08: APAC Campaign with Salesforce ID Generation = Yes","","","","","",""),
("SEC11","E2E-08","SFDC = Yes on APAC request → 2 APJ-specific Salesforce build tasks activated in APAC project (scenario 07 sub-route C)","Only applies to APAC; AMER bypasses this step","–","Prod","QA Team","High"),
("SEC11","E2E-08","Route 4 re-validation triggered before Ops pick-up (region = APAC + SFDC = Yes)","","–","Prod","QA Team","High"),

# ══════════════════════════════════════════════════════════════════════════════
("SECTION", "SECTION 12 – POST-RELEASE SIGN-OFF", "sec12"),
# ══════════════════════════════════════════════════════════════════════════════
("SEC12","Post-Release","First live APAC campaign request monitored end-to-end in PROD","Confirm all steps complete and Marketo program created","–","Prod","Ops Team","High"),
("SEC12","Post-Release","First live AMER campaign request monitored end-to-end in PROD","","–","Prod","Ops Team","High"),
("SEC12","Post-Release","Hypercare period defined (recommended minimum 2 weeks)","On-call support defined for critical issues post go-live","–","Prod","Ops Team","High"),
("SEC12","Post-Release","All PREVIEW Fusion scenarios in Stage deactivated or archived","Prevent accidental Stage runs interfering with PROD","Preview","–","Dev Team","Medium"),
("SEC12","Post-Release","PROD Fusion scenario error notifications configured","Alert on scenario failure or error rate spike","–","Prod","Dev Team","High"),
("SEC12","Post-Release","Workfront Planning data flow confirmed in PROD (records flowing correctly into all tables)","Spot-check 2–3 requests in Planning tables","–","Prod","Dev Team","High"),
("SEC12","Post-Release","Operations team trained on PROD dashboards, workflows and escalation process","","–","Prod","Ops Team","High"),
("SEC12","Post-Release","Marketer team communication sent about new request process in PROD","Include how-to guide and support contact","–","Prod","Ops Team","Medium"),
("SEC12","Post-Release","Stakeholder sign-off obtained from Marketing Operations lead","Written or email approval","–","Prod","Ops Team","High"),
("SEC12","Post-Release","Go-live confirmation document completed (date, sign-off names, known issues)","Archive for audit trail","–","Prod","Ops Team","High"),

]  # end rows

# ── Render rows ───────────────────────────────────────────────────────────────
row_num   = 1    # checklist item counter
data_row  = 2    # excel row counter (1 = header)
alt       = False

# Section color map
SEC_COLOR = {
    "SECTION": None,
    "SUB":     None,
    "SEC1":  C["sec1"],  "SEC2":  C["sec2"],  "SEC3":  C["sec3"],
    "SEC4":  C["sec4"],  "SEC5":  C["sec5"],  "SEC6":  C["sec6"],
    "SEC7":  C["sec7"],  "SEC8":  C["sec8"],  "SEC9":  C["sec9"],
    "SEC10": C["sec10"], "SEC11": C["sec11"], "SEC12": C["sec12"],
}

SEC_FG = {
    "SEC1":  C["sec1_fg"],  "SEC2":  C["sec2_fg"],  "SEC3":  C["sec3_fg"],
    "SEC4":  C["sec4_fg"],  "SEC5":  C["sec5_fg"],  "SEC6":  C["sec6_fg"],
    "SEC7":  C["sec7_fg"],  "SEC8":  C["sec8_fg"],  "SEC9":  C["sec9_fg"],
    "SEC10": C["sec10_fg"], "SEC11": C["sec11_fg"], "SEC12": C["sec12_fg"],
}

STATUS_OPTIONS = '"To Do,In Progress,Done,N/A,Blocked"'
dv = DataValidation(type="list", formula1=STATUS_OPTIONS, allow_blank=True)
ws.add_data_validation(dv)

num_cols = len(COLS)

for r in rows:
    kind = r[0]

    if kind == "SECTION":
        # ── Full-width section header ──
        _, label, color_key = r
        ws.append([""] * num_cols)
        ws.merge_cells(start_row=data_row, start_column=1,
                       end_row=data_row,   end_column=num_cols)
        cell = ws.cell(data_row, 1)
        cell.value = f"  {label}"
        cell.fill  = fill(C[color_key])
        cell.font  = Font(bold=True, color="FFFFFF", size=12, name="Calibri")
        cell.alignment = align("left", "center", False)
        ws.row_dimensions[data_row].height = 22
        data_row += 1
        alt = False

    elif kind == "SUB":
        # ── Sub-section header ──
        _, label = r[0], r[1]
        ws.append([""] * num_cols)
        ws.merge_cells(start_row=data_row, start_column=1,
                       end_row=data_row,   end_column=num_cols)
        cell = ws.cell(data_row, 1)
        cell.value = f"    ▸  {label}"
        cell.fill  = fill(C["sub"])
        cell.font  = Font(bold=True, color=C["sub_fg"], size=10, name="Calibri")
        cell.alignment = align("left", "center", False)
        for ci in range(1, num_cols + 1):
            ws.cell(data_row, ci).border = border_thin()
        ws.row_dimensions[data_row].height = 18
        data_row += 1
        alt = False

    else:
        # ── Data row ──
        sec_key, sub, item, detail, stage_ref, prod_ref, owner, priority = r
        bg = C["row_b"] if alt else C["row_a"]
        alt = not alt

        values = [row_num, "", sub, item, detail, stage_ref, prod_ref, owner, priority, "To Do", "", ""]
        ws.append(values)

        for ci in range(1, num_cols + 1):
            cell = ws.cell(data_row, ci)
            cell.border = border_thin()
            cell.alignment = align("left" if ci > 2 else "center")

            if ci == 1:  # #
                cell.font = Font(bold=True, size=9, color="555555", name="Calibri")
                cell.fill = fill(bg)
            elif ci == 9:  # Priority
                if priority == "High":
                    cell.fill = fill(C["high"])
                    cell.font = Font(bold=True, color=C["high_fg"], size=10, name="Calibri")
                elif priority == "Medium":
                    cell.fill = fill(C["med"])
                    cell.font = Font(bold=True, color=C["med_fg"], size=10, name="Calibri")
                else:
                    cell.fill = fill(C["low"])
                    cell.font = Font(bold=True, color=C["low_fg"], size=10, name="Calibri")
            elif ci == 10:  # Status
                cell.fill = fill("EBF5FF")
                cell.font = Font(size=10, color="0052B3", name="Calibri")
                dv.add(cell)
            else:
                cell.fill = fill(bg)
                cell.font = font(size=10)

        ws.row_dimensions[data_row].height = 16
        row_num += 1
        data_row += 1

# ── Summary row at the bottom ──────────────────────────────────────────────
ws.append([""] * num_cols)
data_row += 1
ws.append([""] * num_cols)
ws.merge_cells(start_row=data_row, start_column=1,
               end_row=data_row,   end_column=num_cols)
summary_cell = ws.cell(data_row, 1)
summary_cell.value = f"  TOTAL CHECKLIST ITEMS: {row_num - 1}  |  Sections: Pre-Release (9) · Workfront Config (32) · Fusion Common (8) · Watch Events (24) · Webhook Scenarios (99) · Adobe I/O (17) · Planning Tables (25) · Validation Rules (8) · MCZ/Marketo (9) · Notifications (8) · E2E Testing (33) · Post-Release (10)"
summary_cell.fill = fill(C["hdr"])
summary_cell.font = Font(bold=True, color="FFFFFF", size=9, name="Calibri")
summary_cell.alignment = align("left", "center", False)
ws.row_dimensions[data_row].height = 16

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/home/user/projectDesign/Production_Release_Checklist.xlsx"
wb.save(out)
print(f"Saved: {out}  ({row_num - 1} items)")
