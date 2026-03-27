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

**Queue Topic:** Enterprise Campaign Operations Requests (APAC / AMER)

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
| 10 | Targeting Criteria | Radio button – 4 options (conditional logic) |
| 11 | Content Option | Radio button – 4 options (conditional logic) |

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

### 7. Adobe I/O Actions & Fusion Functions

Reusable logic components (JavaScript-based) for:

- Generating **Request Overview Summaries** from intake data
- Producing **Validation Summary Reports** by referencing Planning lookup tables
- Generating **MCZ Sync Object payloads** (.JSON structure) for SnapLogic

---

### 8. SnapLogic Integration

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
│   └── Task 6: Migrate Lookup Tables from Airtable to Workfront Planning
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
| Data & Lookup Management | Workfront Planning |
| Automation & Integration Layer | Workfront Fusion |
| Custom Logic & Scripts | Adobe I/O (JavaScript Actions) |
| Middleware / API Gateway | SnapLogic |
| Marketing Automation Platform | Adobe Marketo (MCZ) |
| Legacy Lookup Source | Airtable (being migrated) |
| Payload Format | JSON |
| UI Design Reference | Miro |
| Taxonomy Reference | SharePoint Excel |

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
- [ ] Existing fields reused without duplication
- [ ] Taxonomy documented, reviewed, and approved
- [ ] All Fusion scenarios tested end-to-end
- [ ] Planning tables populated and validated
- [ ] Adobe I/O scripts tested in staging
- [ ] MCZ payloads successfully processed via SnapLogic
- [ ] Stakeholder acceptance obtained for each feature
- [ ] All components deployed to production
