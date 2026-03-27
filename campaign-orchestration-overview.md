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
| 4 | Add Content Now | Renders CTA Type (Single/Multi), Number of CTAs (2–7 for Multi), and dynamic content sections per CTA |

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

Workfront Planning acts as the campaign data and lookup management layer:

| Table | Purpose |
|-------|---------|
| Campaign Request Data | Stores structured campaign request data from intake forms |
| Validation Rules | Stores campaign validation rules used during request processing |
| Interactive Message Templates | Stores dynamic message templates with placeholders (e.g., `{Name}`, `{CampaignID}`) |
| MCZ Taxonomy Lookup | Stores MCZ shells, folders, tokens, and programs for Marketo provisioning |

Existing Airtable lookup tables are migrated into Workfront Planning as part of this initiative.

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
