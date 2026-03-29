# Campaign Orchestration Platform – Project Overview

## Summary

The **Campaign Orchestration Platform** is an end-to-end marketing automation solution built on top of Adobe Workfront, Workfront Planning, Workfront Fusion, Adobe I/O, and SnapLogic. It streamlines the lifecycle of enterprise email campaigns across three regions — **APAC, AMER, and EMEA** — from intake request submission to automated MCZ (Marketo) provisioning.

The platform replaces fragmented, region-specific manual processes with a unified, governed, and automated orchestration engine.

---

## Business Context

Marketing Operations teams in APAC and AMER currently rely on inconsistent intake forms, ad-hoc targeting definitions, and manual project creation workflows. This causes:

- Incomplete or inconsistent campaign requests
- Duplicate data entry across systems (Workfront, Airtable, Marketo)
- Delayed campaign timelines due to manual handoffs
- Difficulty enforcing taxonomy and governance standards

The Campaign Orchestration Platform addresses these gaps by introducing standardized intake forms, automated project scaffolding, validation logic, and seamless integration with downstream provisioning systems.

---

## Platform Architecture – Key Components

### 1. Workfront Intake Forms (APAC & AMER)

Standardized request forms built within the **Enterprise Marketing & Operations Request Queue**. These forms:

- Dynamically render fields based on user selections (region, targeting option, content option)
- Reuse global EMEA field definitions to ensure cross-region consistency
- Enforce taxonomy and naming conventions via a central reference document
- Support four **Targeting Criteria** modes and four **Campaign Content** modes
- Include a **Send Date** field (existing, validated across APAC/AMER/EMEA) positioned above Targeting Criteria

**Queue Topic:** Enterprise Campaign Operations Requests (APAC / AMER)

> **Solution Design Note:** The APAC and AMER intake forms share the **same solution design and form structure**. The only region-specific difference is in the **Targeting Criteria section** — a small subset of targeting fields are unique to each region (APAC-specific vs. AMER-specific), while all remaining fields (including Send Date, content sections, and CTA fields) are identical. Both forms are configured from a single shared design; region routing determines which targeting fields are rendered.

---

### 2. Intake Request Flow (User Journey)

A marketer initiates a request by navigating to Workfront → Hamburger Menu → Requests.

**Step-by-step form flow:**

| Step | Field | Behavior |
|------|-------|----------|
| 1 | Request Queue | Enterprise Marketing & Operations Request Queue (existing) |
| 2 | Queue Topic | APAC or AMER Enterprise Campaign Operations Requests |
| 3 | Subject | Free text (existing field) |
| 4 | Region | APAC / AMER (existing field + options) |
| 5 | Sub-Region | Filtered by Region (existing field) |
| 6 | Country | Filtered by Sub-Region (existing field) |
| 7 | Enterprise GTM Segments | Shown only when Region = AMER (existing field) |
| 8 | Requesting Team | Dropdown (existing field) |
| 9 | Request Type | Email Program (Batch) – existing field |
| 10 | Send Date | Campaign send date selector – existing field, validated and reused across APAC and AMER; positioned above Targeting Criteria |
| 11 | Targeting Criteria | Radio button – 4 options (conditional logic) |
| 12 | Content Option | Radio button – 4 options (conditional logic) |

---

### 3. Targeting Criteria Options

| Option | Label | Behavior |
|--------|-------|----------|
| 1 | Copy from Last Request | Auto-pulls targeting from most recent request; task created and marked complete |
| 2 | Copy from Specific Request | User provides Request ID; targeting copied; task marked complete |
| 3 | Add Targeting Now | Displays all region-specific targeting fields inline; full control upfront |
| 4 | Provide Targeting Later | Task created and linked to requester; targeting added manually later |

When **Option 3** is selected, the form renders all existing targeting criteria fields for the selected region (APAC/AMER), consolidated across EMEA standards.

---

### 4. Campaign Content Options

| Option | Label | Behavior |
|--------|-------|----------|
| 1 | Provide Content Later | Task added to timeline; content added post-submission |
| 2 | Copy from Last Request | Copies content from most recent matching request; task marked complete |
| 3 | Use Content from Specific Request | Requires Request ID input; content copied; task marked complete |
| 4 | Add Content Now | Renders CTA Type (Single/Multi), Number of CTAs (2–5 for Multi), and dynamic content sections per CTA |

---

### 4a. Add Content Now – Detailed Field Structure

When the marketer selects **"Add content now"**, the following fields are rendered dynamically:

**CTA Configuration:**
- **CTA Type** — Single CTA (default) / Multi CTA
- **Number of CTAs** — Dropdown (2, 3, 4, 5); shown only when Multi CTA is selected; default = 2

**Base Content Fields (always shown when "Add content now" is selected):**

| Field Label | Field Type | Description |
|-------------|------------|-------------|
| Subject Line | Open text | Email subject line |
| Preview Text | Open text | Inbox preview text |
| Email Call-to-Action Text | Open text | Main CTA button label |
| Email Call-to-Action URL | Open text | URL for the main CTA |
| Email Headline | Open text | Email headline text |
| Email Banner Image | Open text (URL) | URL for banner image in email header |
| Email Body | Rich text editor | Main email body content |
| Content Image | Open text (URL) | Image URL within email body content area |

**Additional CTA Sections (dynamically rendered based on CTA count selection):**

Each additional CTA section (CTA 2 through CTA 5) contains:

| Field Label | Field Type |
|-------------|------------|
| CTA N Email Headline | Open text |
| CTA N Email Body | Rich text editor |
| CTA N Email Call-to-Action Text | Open text |
| CTA N Email Call-to-Action URL | Open text |
| CTA N Content Image | Open text (URL) |

Maximum supported: **CTA 5** (5 total CTAs for Multi CTA type).

---

### 4b. Salesforce Campaign ID Tracking

A checkbox field is displayed on the intake form:

> **"Do you require Salesforce Campaign ID Creation as part of this request?"**

- When **unchecked**: no additional tracking action is taken
- When **checked**: Fusion scenario automatically adds a dedicated **SFDC Campaign Tracking task** to the operations project. The operations team fills in the following tracking values within that task, which are then consumed during sync object generation:

| Field | Description |
|-------|-------------|
| Salesforce Campaign ID (s_rtid) | External SFDC tracking ID in the CTA URL |
| Internal SFDC ID (s_iid) | Internal Salesforce campaign identifier |
| Gated / Ungated | Content gate status |
| Button Type | CTA button type (e.g., Button, Text Link) |

These values are resolved per-CTA URL during MCZ sync object generation.

---

### 5. Workfront Fusion Scenarios

Automated integration layer responsible for:

- **Intake Processing Scenario:** Watches for new requests in the queue (APAC/AMER, Email Program type); triggers downstream orchestration
- **Marketer Project Creation Scenario:** Automatically creates a structured Workfront project for the marketer based on validated request data
- **Email Governance Watch Event:** Monitors completion of the Email Governance task within marketer projects
- **Operations Project Creation Scenario:** Creates operations team projects based on routing logic (region, team, CTA type)
- **SnapLogic API Invocation Scenario:** Transmits MCZ payloads to SnapLogic for downstream Marketo provisioning
- **SnapLogic Response Watch Event:** Detects and processes responses from SnapLogic to update provisioning status

---

### 6. Workfront Planning Tables

Workfront Planning acts as the campaign data, lookup management, and enrichment layer. Tables are connected via **PL (Planning Link) connections** so that selecting a value in the request table automatically enriches adjacent fields from the linked lookup table.

#### 6a. Campaign Request Data Table (Core Table)

Stores structured intake request data and serves as the central record for campaign orchestration.

| Field | Description |
|-------|-------------|
| Request ID | Unique Workfront request identifier |
| Parent Request ID | Set when this record is a child (additional-language) request |
| Child Request IDs | List of linked child requests for this parent campaign |
| Region | APAC / AMER |
| Sub-Region | Filtered by region |
| Country | Filtered by sub-region |
| Requesting Team | Team submitting the request |
| Campaign Type | Single CTA / Multi CTA |
| CTA Count | Number of CTAs (1–5) |
| Targeting Option | Options 1–4 |
| Content Option | Options 1–4 |
| Send Date | Campaign send date |
| Solution | Linked to Solutions lookup table via PL connection |
| Industry | Linked to Industry lookup table via PL connection |
| POI (Product of Interest) | Specific Adobe product targeted; linked via PL connection; used for token and program shell naming |
| Team Code | Linked to Team lookup table via PL connection |
| Content Document ID | Workfront Document ID of the `content.js` JSON file attached to the Content task |
| Sync Object Document ID | Workfront Document ID of the MCZ sync object JSON file |
| Marketer Project ID | Linked Workfront marketer project |
| Operations Project ID | Linked Workfront operations project |
| Status | Current campaign lifecycle status |
| SFDC Tracking Required | Boolean flag from intake form checkbox |

**PL Connection Enrichment:** When Solution, Industry, POI, or Team is set/updated, the PL connections pull enriched attributes (e.g., solution abbreviation, POI token prefix, team routing code) from the respective lookup tables automatically.

#### 6b. Solutions Lookup Table
Stores solution definitions used across campaigns.

| Field | Description |
|-------|-------------|
| Solution ID | Unique ID |
| Solution Name | Full name (e.g., Adobe Experience Cloud) |
| Solution Abbreviation | Short code used in token and program naming |
| Region Applicability | Applicable regions |

#### 6c. Industry Lookup Table
Stores industry vertical definitions for targeting enrichment.

#### 6d. POI (Product of Interest) Lookup Table
Stores specific Adobe products targeted by campaigns. POI values are used during token construction and MCZ program shell selection.

#### 6e. Team Lookup Table
Stores team definitions including routing codes used by Fusion scenario routing logic.

#### 6f. Validation Rules Lookup Table

| Field | Description |
|-------|-------------|
| Rule ID | Unique rule identifier |
| Rule Name | Descriptive name |
| Rule Type | Field validation / completeness / compliance |
| Validation Logic | Condition expression |
| Error Message | Message shown when rule fails |
| Severity | Error / Warning / Info |
| Region Scope | APAC / AMER / EMEA / Global |
| Active Flag | Enable/disable rule |

#### 6g. Interactive Message Templates Lookup Table

Stores reusable automated message templates with dynamic placeholders used in Issues, Projects, and Tasks.

Placeholders include: `{Name}`, `{CampaignID}`, `{Region}`, `{SendDate}`, `{MCZLink}`, `{ValidationStatus}`

#### 6h. MCZ Taxonomy Lookup Table (Shells, Folders)

Stores MCZ program infrastructure definitions used during provisioning.

| Field | Description |
|-------|-------------|
| Shell ID | Unique shell identifier |
| Shell Name | MCZ program shell template name |
| Region | Mapped region |
| Campaign Type | Single CTA / Multi CTA |
| Solution | Linked to Solutions lookup |
| POI | Linked to POI lookup |
| Folder Path | Target folder path in Marketo |
| Token Set Reference | Linked to Tokens lookup table |

#### 6i. Tokens Lookup Table

Stores Marketo token definitions used in sync object generation.

| Field | Description |
|-------|-------------|
| Token Name | Marketo token name (e.g., `{{my.emailSubjectLine}}`) |
| Token Type | Program-level / Folder / Content |
| Default Value | Default if campaign value is not set |
| Campaign Field Mapping | Which campaign field supplies the value |
| Solution Applicability | Applicable solutions |

#### 6j. Program Shell Table

Stores dynamically selectable program shell templates for MCZ provisioning, mapped by Solution + POI + Region + Campaign Type combinations.

---

### 7. Workfront Fusion Scenarios – Detailed Flow

#### Scenario 1: Intake Request Processing (S1)

**Trigger:** Watch Event – new request created
**Filter:** Queue = Enterprise Marketing & Operations, Type = Email Program (Batch), Region = APAC or AMER

**Flow:**
1. Event captured on request submit
2. Request data extracted from intake form fields
3. Routing determined: region, team, CTA type (Single/Multi), targeting option, content option
4. Adobe I/O module called → **Overview Build Action** (builds initial overview from request data)
5. Planning request table record created with all intake data
6. Proceeds to Scenario 2 (Marketer Project Creation)

---

#### Scenario 2: Marketer Project Creation (S2)

**Trigger:** Completion of S1 with validated request data

**Flow:**
1. Correct marketer project template selected based on CTA type (Single CTA / Multi CTA) and region
2. Marketer project created in Workfront using selected template
3. Project assigned to correct team and owner(s) based on region
4. Project start date set
5. All intake form data transferred to respective marketer project task forms
6. If content was provided ("Add content now"): content fields copied to the Content task within the marketer project
7. Adobe I/O module called → **content.js Generation Action** — builds initial JSON document; stored as Workfront Document attachment on the Content task
8. Planning request table updated: Marketer Project ID and Content Document ID recorded
9. Adobe I/O module called → **Validation Summary Action** — initial validation run; results printed on marketer project
10. If parent marketer project selected (child/net-language request): content routed to the corresponding language task within the existing project (no new project created)

---

#### Scenario 3: Content and Task Change Watcher (S3 – Continuous)

**Trigger:** Watch Event – any task value update within a marketer campaign project

**Flow:**
1. Detects changes to content task values, targeting task values, or any language-specific task
2. Adobe I/O module called → **Overview Build Action** — re-generates overview with updated values; writes to marketer project
3. Adobe I/O module called → **Validation Summary Action** — re-evaluates all validation rules; updated summary written to marketer project
4. `content.js` document updated as a new version on the Content task attachment

---

#### Scenario 4: Email Governance Task Completion Watch (S4)

**Trigger:** Watch Event – Task Name = "Email Governance Task", Status = Complete, within a Marketer Campaign Project

**Flow:**
1. Governance task completion detected
2. Adobe I/O module called → **Overview Summary Generation Action** — final overview summary built and written to the Operations project
3. Operations project tasks that are pending overview data are marked complete
4. Pre-Sync Summary task in Operations project is set to **In Progress**

---

#### Scenario 5: Operations Project Creation (S5)

**Trigger:** Initiated from S2 after marketer project creation; operations project is created in parallel

**Flow:**
1. Routing logic evaluates: Region + Team + CTA Type (Single/Multi)
2. Correct operations project template selected
3. Operations project created and assigned to operations team
4. If SFDC tracking was requested: **SFDC Tracking task** added to the operations project
5. Planning request table updated: Operations Project ID recorded

---

#### Scenario 6: Sync Object Build and SnapLogic API Invocation (S6)

**Trigger:** Completion of the Pre-Sync Summary task in the Operations project (after MCZ details review cycle)

**Sub-flow – MCZ Review Cycle (within S6):**
1. Ops Email Summary task completion detected in Operations project
2. Adobe I/O module called → **Sync Object Build Action** — constructs MCZ sync object JSON from `content.js` + lookup enrichment + tokens + program shells + SFDC tracking IDs (if applicable)
3. Sync object JSON stored as Workfront Document; Document ID saved to Planning request table
4. MCZ details written to the **MCZ-Pre-Sync Summary task** in Operations project for review
5. Operations team reviews MCZ details:
   - **If changes needed:** team updates field values → Fusion detects update → Adobe I/O Sync Object Build Action re-triggered → updated MCZ details posted back to task → review cycle repeats
   - **If approved:** MCZ-Pre-Sync Summary task marked complete
6. On task complete: Adobe I/O Overview Summary Action re-run → final overview regenerated
7. **Build task** in Operations project set to **In Progress**
8. On Build task complete: sync object Document ID sent to SnapLogic API

**SnapLogic API Call:**
- Fusion invokes SnapLogic API with sync object Document ID
- SnapLogic fetches the sync object document from Workfront, processes it, calls Marketo API
- MCZ program provisioned in Marketo

---

#### Scenario 7: SnapLogic Response Watch and Processing (S7)

**Trigger:** Watch Event – sync object document updated with new version (SnapLogic writes response as document version)

**Flow:**
1. Document version update detected on the sync object document
2. Adobe I/O module called → **SnapLogic Response Processor Action** — decodes the response JSON
3. Response decoded: MCZ program URL, success/failure status, provisioning details extracted
4. Workfront update:
   - MCZ links and program details written to Operations and Marketer projects
   - Relevant tasks in both projects marked complete
   - **QA task** in Operations project set to **In Progress**
5. Planning request table updated with MCZ program details and final status
6. Operations team verifies MCZ details in Marketo and proceeds with QA

---

### 8. Adobe I/O Actions – Standalone JavaScript Actions

Each Adobe I/O action operates as an **independent, stateless JavaScript function**. It accepts a JSON object as input, performs its logic, and returns a JSON response. Fusion calls these actions via the Adobe I/O module — never embedding the logic natively in Fusion.

#### Action 1: Overview Build (`overview-build`)

**Purpose:** Generate a formatted request overview summary from the current campaign data
**Input:** `content.js` JSON object (campaign fields, CTA data, targeting, metadata)
**Output:** Formatted HTML/text overview string
**Trigger:** Any marketer project task value change; initial request processing
**Usage:** Written to marketer project description or task note

---

#### Action 2: Validation Summary (`validation-summary`)

**Purpose:** Evaluate all campaign fields against the validation rules table and produce a structured validation report
**Input:** `content.js` JSON + validation rules payload
**Output:** Validation summary JSON (rule-by-rule results, severity, overall pass/fail)
**Trigger:** Any marketer project task value change
**Usage:** Printed on marketer project; blocks downstream steps if critical failures exist

---

#### Action 3: Overview Summary Generation (`overview-summary-ops`)

**Purpose:** Generate the final campaign overview summary for the Operations project after Email Governance task completion
**Input:** `content.js` JSON (final state)
**Output:** Formatted operations-level overview summary string
**Trigger:** Email Governance task completion in marketer project
**Usage:** Written to Operations project; makes ops pre-sync tasks visible

---

#### Action 4: Sync Object Build (`sync-object-build`)

**Purpose:** Construct the MCZ Sync Object JSON payload from all campaign data, enriched lookups, tokens, program shells, and SFDC tracking IDs
**Input:** `content.js` JSON + token data + program shell reference + SFDC tracking IDs (if applicable)
**Output:**
- MCZ Sync Object JSON (stored as Workfront Document)
- Human-readable MCZ details string (written to MCZ-Pre-Sync Summary task)
**Trigger:** Pre-sync step in Operations project (after ops email summary completion and on any MCZ detail correction)
**Usage:** Sync object document ID tracked in Planning request table; MCZ details rendered for ops team review

---

#### Action 5: SnapLogic Response Processor (`snaplogic-response-processor`)

**Purpose:** Decode and interpret the SnapLogic provisioning response and produce structured update instructions
**Input:** SnapLogic response JSON (new version of the sync object document)
**Output:** Structured JSON with:
- MCZ program URL and access links
- Provisioning status (success / failure / partial)
- Task completion flags for marketer and operations projects
- QA readiness flag
**Trigger:** Sync object document version update detected by Fusion watch event
**Usage:** Fusion applies output to update both projects, complete tasks, and set QA task to In Progress

---

### 9. content.js – Campaign Content JSON Document

The `content.js` file is the central data artifact for each campaign. It is:

- **Format:** JSON
- **Storage:** Workfront Document attachment on the Content task within the marketer project (versioned)
- **Purpose:** Consolidates all campaign data that Workfront Planning column fields alone cannot hold
- **Created by:** Adobe I/O `overview-build` action during initial Fusion S2 processing
- **Updated by:** Adobe I/O actions on every relevant marketer task change event

**Document structure includes:**
- Intake metadata (region, team, request type, send date)
- CTA content sections (subject, preview text, headline, body, CTA text, CTA URL, images) for all CTAs (1–5)
- Targeting data (option selected + field values if provided)
- Enriched lookup data (Solution abbreviation, Industry, POI token prefix, Team code)
- Token values resolved from the Tokens lookup table
- Validation summary (latest run)
- Overview summary (latest run)
- Sync object reference (Document ID once generated)
- SFDC tracking fields (if applicable)

The Document ID of this file is stored in the Planning request table for cross-reference.

---

### 10. SnapLogic Integration

SnapLogic acts as the middleware for Adobe MCZ (Marketo) API integration:

- Receives MCZ payload JSON from Workfront Fusion
- Processes and maps data to Marketo API specifications
- Returns provisioning response (success/failure) back to Workfront via watch events

---

## ADO Work Item Hierarchy

```
Epic: Campaign Orchestration Platform Build
│
├── Feature: Intake & Request Management
│   ├── Task 1: Configure Workfront Intake Form – APAC
│   ├── Task 2: Configure Workfront Intake Form – AMER
│   ├── Task 3: Fusion Scenario – Process Intake Requests
│   ├── Task 4: Planning Table – Campaign Request Data
│   └── Task 5: Fusion/Adobe I/O – Request Overview Generation
│
├── Feature: Data & Lookup Management
│   └── Task 6: Migrate Lookup Tables from Airtable to Workfront Planning (APAC/AMER scope)
│
├── Feature: Validation Framework
│   ├── Task 7: Validation Rules Lookup Table
│   ├── Task 8: Interactive Message Template Lookup Table
│   └── Task 9: Request Validation Summary Logic
│
├── Feature: Campaign Project Automation
│   ├── Task 10: Marketer Campaign Project Template
│   ├── Task 11: Operations Project Templates (Routing Logic)
│   ├── Task 12: Fusion Scenario – Marketer Project Creation
│   ├── Task 13: Watch Event – Email Governance Task Completion
│   └── Task 14: Fusion Scenario – Operations Project Creation
│
└── Feature: MCZ Integration & Provisioning
    ├── Task 15: Planning Table – MCZ Taxonomy Lookup
    ├── Task 16: Fusion/Adobe I/O – MCZ Sync Object Generation
    ├── Task 17: Fusion Scenario – SnapLogic API Invocation
    └── Task 18: Watch Event – SnapLogic Response Processing
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Intake Forms & Project Management | Adobe Workfront |
| Data, Lookup Management & Enrichment | Workfront Planning (with PL connections) |
| Automation & Integration Layer | Workfront Fusion (7 scenarios) |
| Custom Logic & Scripts | Adobe I/O JavaScript Actions (5 actions) |
| Campaign Content JSON Document | Workfront Document (content.js, versioned) |
| Middleware / API Gateway | SnapLogic |
| Marketing Automation Platform | Adobe Marketo (MCZ) |
| Lookup Source (EMEA) | Airtable (active for EMEA region; APAC/AMER lookup tables migrated to Workfront Planning) |
| Payload Format | JSON (sync object, content.js, API responses) |
| UI Design Reference | Miro |
| Taxonomy Reference | SharePoint Excel |
| SFDC Tracking Values | Intake form CTA URL params (s_rtid, s_iid, gated flag, button type) entered by marketer, or supplied by Ops team in auto-created SFDC Tracking task — no external Salesforce system connection |

---

## Governance & Standards

- All form fields must follow **EMEA naming conventions** as the global standard
- Backend field values must use **approved taxonomy** (documented in central Excel reference)
- No production form should be modified directly — changes must be tested in a temporary/test queue first
- Stakeholder sign-off is required before production deployment
- A **central taxonomy reference document** must be maintained and updated as new fields are added

---

## Definition of Done (Platform-Level)

- [ ] All intake forms (APAC, AMER) dynamically render fields per conditional logic
- [ ] CTA content sections render correctly for Single CTA and Multi CTA (up to CTA 5)
- [ ] SFDC tracking checkbox correctly triggers ops project task via Fusion
- [ ] Existing fields reused without duplication; taxonomy documented and approved
- [ ] All 7 Fusion scenarios tested end-to-end
- [ ] All 5 Adobe I/O actions tested with JSON input/output validation
- [ ] content.js correctly created and versioned as Workfront Document on Content task
- [ ] Planning request table populated with parent/child linking and PL enrichment verified
- [ ] All lookup tables (Solutions, Industry, POI, Team, Validation Rules, Messages, MCZ Taxonomy, Tokens, Program Shell) migrated from Airtable to Workfront Planning and validated (APAC/AMER scope; EMEA remains on Airtable)
- [ ] PL connections verified: enrichment flows automatically on field value changes
- [ ] MCZ pre-sync review cycle tested (build → review → correction → resubmit → approve)
- [ ] MCZ payloads successfully processed via SnapLogic; MCZ programs provisioned in Marketo
- [ ] SnapLogic response processed; QA task set In Progress; MCZ links written to projects
- [ ] Stakeholder acceptance obtained for each feature
- [ ] All components deployed to production
