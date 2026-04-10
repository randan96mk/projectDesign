# Campaign Orchestration Platform – Design & Implementation Diagram

## High-Level Architecture Diagram

```
+----------------------------------------------------------------------------------------------------------------------------------+
|                                    CAMPAIGN ORCHESTRATION PLATFORM – END-TO-END FLOW                                            |
+----------------------------------------------------------------------------------------------------------------------------------+

 MARKETER (USER)                   WORKFRONT                      WORKFRONT FUSION               WORKFRONT PLANNING
 ─────────────────                 ─────────────────────          ────────────────────           ──────────────────────

  [Hamburger Menu]
       │
       ▼
  [Request Queue]─────────────────►[Intake Form: APAC/AMER]
                                         │
                                         │  Dynamic Field Rendering
                                         │  - Region / Sub-Region / Country
                                         │  - Enterprise GTM Segments (AMER only)
                                         │  - Request Type: Email Program (Batch)
                                         │  - Targeting Criteria (Options 1-4)
                                         │  - Content Option (Options 1-4)
                                         │
                                         ▼
                                   [Request Created]──────────────►[Watch Event Trigger]
                                                                         │
                                                                         │ Filter:
                                                                         │ - Queue = APAC/AMER
                                                                         │ - Type = Email Batch
                                                                         ▼
                                                                   [Fusion Scenario 1]
                                                                   Process Intake Request
                                                                         │
                                                             ┌───────────┴───────────┐
                                                             ▼                       ▼
                                                    [Adobe I/O Action]        [Planning Table]
                                                    Generate Request          Campaign Request
                                                    Overview Summary          Data Store
                                                             │
                                                             ▼
                                                   [Fusion Scenario 2]
                                                   Unified Project Creation
                                                             │
                                                             ▼
                                                   [Workfront Project]─────────────────────────►[Planning Table]
                                                   Unified Campaign Project                      Validation Rules
                                                   (APAC or AMER Template)                            │
                                                             │                                        │
                                                             ▼                                        ▼
                                                   [Phase 1: Email Governance]          [Adobe I/O / Fusion Function]
                                                             │                          Validation Summary Logic
                                                             │                                        │
                                                   [Watch Event Trigger]◄───────────────────────────┘
                                                   S4: Email Governance Watch
                                                             │
                                                             ▼
                                                   [Phase 2 Activated]
                                                   Operations Tasks within
                                                   Unified Campaign Project
                                                             │
                                                             ▼
                                                   [MCZ Provisioning Flow]
```

---

## MCZ Provisioning Integration Flow

```
  WORKFRONT PLANNING                WORKFRONT FUSION               SNAPLOGIC               ADOBE MARKETO (MCZ)
  ──────────────────               ────────────────────           ───────────             ────────────────────

  [MCZ Taxonomy Lookup]
  - Shells
  - Folders             ──────────►[Fusion / Adobe I/O]
  - Tokens                         MCZ Sync Object
  - Programs                       Generation Logic
                                         │
                                         │  .JSON Payload
                                         ▼
                                   [Fusion Scenario]──────────────►[SnapLogic API]
                                   SnapLogic API                   Ingest & Transform
                                   Invocation                      MCZ Payload
                                                                         │
                                                                         ▼
                                                                   [Marketo API]
                                                                   Provision Campaign
                                                                   Shells / Programs
                                                                         │
                                                                         │  Response
                                                                         ▼
                                   [Watch Event]◄──────────────────[SnapLogic Response]
                                   SnapLogic Response               Success / Failure
                                   Processing                        Status
                                         │
                                         ▼
                                   [Workfront Update]
                                   Campaign Provisioning
                                   Status Updated
```

---

## Intake Form – Conditional Logic Flow

```
  NOTE: APAC and AMER share the same form structure and solution design.
        Only the Targeting Criteria section has region-specific fields.
        All other fields (including Send Date and content sections) are identical.

  USER SELECTS: Request Type = Email Program (Batch)
       │
       ▼
  ┌────────────────────────────────────────────────────────────────┐
  │  SEND DATE                                                     │
  │  Campaign send date selector                                   │
  │  Existing field – reused across APAC and AMER without change   │
  └────────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌────────────────────────────────────────────────────────────────┐
  │                   TARGETING CRITERIA                           │
  │                                                                │
  │  ○ Option 1: Copy from Last Request                           │
  │      └──► Auto-copy; Task created + marked complete           │
  │                                                                │
  │  ○ Option 2: Copy from Specific Request                       │
  │      └──► Show [Request ID field]                             │
  │           Copy targeting; Task marked complete                 │
  │                                                                │
  │  ○ Option 3: Add Targeting Now                                │
  │      └──► Show targeting fields for selected region:          │
  │           Shared fields (APAC + AMER common targeting)        │
  │           + APAC-specific fields  (if Region = APAC)          │
  │           + AMER-specific fields  (if Region = AMER)          │
  │           Simple / Detailed toggle                             │
  │           Industry, Comments, Notes fields                     │
  │           Task marked complete                                 │
  │                                                                │
  │  ○ Option 4: Provide Targeting Later                          │
  │      └──► Task created, linked to requester                   │
  │           Targeting added manually later                       │
  └────────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌────────────────────────────────────────────────────────────────┐
  │                   CONTENT OPTION                               │
  │                                                                │
  │  ○ Option 1: Provide Content Later                            │
  │      └──► Task added to timeline; no content fields shown     │
  │                                                                │
  │  ○ Option 2: Copy from Last Request                           │
  │      └──► Auto-copy; Task marked complete                     │
  │                                                                │
  │  ○ Option 3: Use Content from Specific Request                │
  │      └──► Show [Request ID field]                             │
  │           Copy content; Task marked complete                   │
  │                                                                │
  │  ○ Option 4: Add Content Now                                  │
  │      └──► Show [CTA Type: Single / Multi]                     │
  │           If Multi → Show [Number of CTAs: 2–5]               │
  │           Dynamically render content sections per CTA count   │
  │           Task validated                                       │
  └────────────────────────────────────────────────────────────────┘
```

---

## Multi-CTA Content Section – Dynamic Rendering Logic

```
  CTA Type = Multi CTA Selected
       │
       ▼
  Number of CTAs selected (2 / 3 / 4 / 5)   [default = 2]
       │
       ▼
  ┌───────────────────────────────────────────────────────────┐
  │  BASE CONTENT (always shown when "Add content now")       │
  │  ├── Subject Line             (open text)                 │
  │  ├── Preview Text             (open text)                 │
  │  ├── Email Headline           (open text)                 │
  │  ├── Email Banner Image       (open text)                 │
  │  ├── Email Body               (rich text)                 │
  │  ├── Content Image            (open text)                 │
  │  ├── Email Call-to-Action Text (open text)                │
  │  └── Email Call-to-Action URL  (open text)                │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 2  (shown when CTA count >= 2)            │
  │  ├── CTA 2 Email Headline     (open text)                 │
  │  ├── CTA 2 Email Body         (rich text)                 │
  │  ├── CTA 2 CTA Text           (open text)                 │
  │  ├── CTA 2 CTA URL            (open text)                 │
  │  └── CTA 2 Content Image      (open text)                 │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 3  (shown when CTA count >= 3)            │
  │  ├── CTA 3 Email Headline     (open text)                 │
  │  ├── CTA 3 Email Body         (rich text)                 │
  │  ├── CTA 3 CTA Text           (open text)                 │
  │  ├── CTA 3 CTA URL            (open text)                 │
  │  └── CTA 3 Content Image      (open text)                 │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 4  (shown when CTA count >= 4)            │
  │  └── [same 5 fields as CTA 2/3 pattern]                   │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 5  (shown when CTA count = 5)             │
  │  └── [same 5 fields as CTA 2/3 pattern]                   │
  └───────────────────────────────────────────────────────────┘
       │
       ▼
  All sections follow EMEA naming conventions and approved taxonomy

  ─────────────────────────────────────────────────────────────
  SFDC TRACKING  (conditional – shown when checkbox checked)
  ─────────────────────────────────────────────────────────────
  ☑ Do you require Salesforce Campaign ID Creation?
       │
       ▼
  [No additional form fields shown]
  A SFDC Campaign Tracking task is automatically added
  to the Operations project by Fusion Scenario S5.
  Operations team fills in:
    ├── Salesforce Campaign ID (s_rtid)
    ├── Internal SFDC ID (s_iid)
    ├── Gated / Ungated
    └── Button Type
  These values feed into the sync object during MCZ build.
```

---

## Data Flow Diagram – Planning Tables and PL Connection Enrichment

```
  ┌─────────────────────────────────────────────────────────────────────────────────────┐
  │                          WORKFRONT PLANNING – DATA LAYER                            │
  │                   (PL = Planning Link Connection between tables)                    │
  └─────────────────────────────────────────────────────────────────────────────────────┘

  LOOKUP TABLES (Read-Only Reference Data – migrated from Airtable for APAC/AMER; EMEA continues on Airtable)
  ─────────────────────────────────────────────────────────────────
   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
   │  Solutions      │  │  Industry       │  │  POI            │  │  Team           │
   │  Lookup         │  │  Lookup         │  │  (Product of    │  │  Lookup         │
   │                 │  │                 │  │  Interest)      │  │                 │
   │ - Solution ID   │  │ - Industry ID   │  │ - POI ID        │  │ - Team ID       │
   │ - Solution Name │  │ - Industry Name │  │ - Product Name  │  │ - Team Name     │
   │ - Abbreviation  │  │ - Vertical Code │  │ - Token Prefix  │  │ - Routing Code  │
   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
            │ PL                  │ PL                  │ PL                  │ PL
            └────────────┬────────┘                    └─────────┬───────────┘
                         ▼                                        ▼
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │                        CAMPAIGN REQUEST DATA TABLE (Core)                        │
  │                                                                                  │
  │  - Request ID           - Parent Request ID     - Child Request IDs              │
  │  - Region               - Sub-Region            - Country                        │
  │  - Requesting Team      - Campaign Type         - CTA Count                      │
  │  - Targeting Option     - Content Option        - Send Date                      │
  │  - Solution ──────────► [PL: pulls Abbreviation from Solutions Lookup]           │
  │  - Industry ──────────► [PL: pulls Vertical Code from Industry Lookup]           │
  │  - POI ───────────────► [PL: pulls Token Prefix from POI Lookup]                 │
  │  - Team ──────────────► [PL: pulls Routing Code from Team Lookup]                │
  │  - Content Document ID  - Sync Object Document ID                                │
  │  - Marketer Project ID  - Operations Project ID                                  │
  │  - SFDC Tracking Flag   - Status                                                 │
  └──────────────────────────────────────────────────────────────────────────────────┘
              │                                         │
              │ enriched data flows into                │
              ▼                                         ▼
  ┌────────────────────────┐           ┌────────────────────────────────────────┐
  │  Validation Rules      │           │  Interactive Message Templates          │
  │  Lookup Table          │           │  Lookup Table                          │
  │                        │           │                                        │
  │  - Rule ID             │           │  - Template ID / Name                  │
  │  - Rule Type           │           │  - Message Body                        │
  │  - Validation Logic    │           │  - Placeholders:                       │
  │  - Error Message       │           │    {Name}, {CampaignID}, {Region}      │
  │  - Severity            │           │    {SendDate}, {MCZLink}               │
  │  - Region Scope        │           │  - Usage: Issue / Project / Task       │
  └──────────┬─────────────┘           └──────────────────┬─────────────────────┘
             │                                             │
             └──────────────┬──────────────────────────────┘
                            ▼
              [Adobe I/O: validation-summary action]
              [Adobe I/O: overview-build action]
                            │
                            ▼
              [Workfront: Marketer Project / Operations Project]
              Validation + Overview summaries written to project

  ─────────────────────────────────────────────────────────────────────────────────────
  MCZ PROVISIONING LOOKUP TABLES
  ─────────────────────────────────────────────────────────────────────────────────────
   ┌────────────────────────────┐    ┌─────────────────────────────┐
   │  Program Shell Table       │    │  Tokens Lookup Table         │
   │                            │    │                             │
   │  - Shell ID / Name         │    │  - Token Name               │
   │  - Region                  │    │  - Token Type               │
   │  - Campaign Type           │    │  - Default Value            │
   │  - Solution (PL link)      │    │  - Campaign Field Mapping   │
   │  - POI (PL link)           │    │  - Solution Applicability   │
   │  - Folder Path             │    └──────────────┬──────────────┘
   │  - Token Set Reference     │                   │
   └──────────────┬─────────────┘                   │
                  │                                  │
                  └────────────────┬─────────────────┘
                                   ▼
                    [Adobe I/O: sync-object-build action]
                    Constructs MCZ Sync Object (.JSON)
                    Document stored as Workfront attachment
                    Document ID ──► recorded in Request Table
                                   │
                                   ▼
                    [Fusion: SnapLogic API Invocation]
                    Document ID sent to SnapLogic
                                   │
                                   ▼
                    SnapLogic processes → Marketo API → MCZ program created
```

---

## Project Template Structure

```
  +-----------------------------------------------------------------------+
  |          UNIFIED CAMPAIGN PROJECT TEMPLATE                            |
  |          2 templates: APAC and AMER (region-based only)              |
  |          Single CTA and Multi CTA use the SAME template               |
  |          Multi CTA: Build task duration = standard + 1 day            |
  +-----------------------------------------------------------------------+
  |                                                                       |
  |  ── PHASE 1: MARKETING TEAM MILESTONES ─────────────────────────── │
  |                                                                       |
  |  +--> Email Governance Task    [completion triggers Phase 2 tasks]   |
  |  +--> Targeting Criteria Task  [form: region-specific targeting]      |
  |  +--> Content Task             [form: CTA content fields]             |
  |  |     +--> content.js JSON document attached here (versioned)        |
  |  |     +--> overview summary and validation summary printed here      |
  |  +--> [Language Task 1]        [for net-language child requests]      |
  |  +--> [Language Task 2]        [additional language if submitted]     |
  |  +--> Overview Build Task      [updated by Adobe I/O on each change]  |
  |  +--> Validation Summary Task  [updated by Adobe I/O on each change]  |
  |                                                                       |
  |  ── PHASE 2: OPERATIONS TEAM MILESTONES ────────────────────────── │
  |  [Activated when Email Governance Task is marked complete]            |
  |                                                                       |
  |  +--> Campaign Overview Summary task  [auto-written by Adobe I/O]     |
  |  +--> [SFDC Tracking task]            [added by Fusion S2 if flag set]|
  |  +--> Ops Email Summary task          [completion triggers sync build]|
  |  +--> MCZ-Pre-Sync Summary task       [MCZ details written here]      |
  |  +--> Build task                      [set In Progress on approval;   |
  |  |                                     +1 day duration for Multi CTA] |
  |  +--> SnapLogic Submission task       [triggered on Build task done]  |
  |  +--> QA Task                         [set In Progress on MCZ success]|
  |  +--> Post-Launch / Verification task [ops team verifies MCZ]         |
  |                                                                       |
  |  Automated owners assigned per region; start dates set by Fusion      |
  +-----------------------------------------------------------------------+
```

---

## Fusion Scenario Trigger Map

```
  ┌────────────────────────────────────────────────────────────────────────────────────┐
  │                         WORKFRONT FUSION SCENARIO TRIGGERS                         │
  ├─────────────────────────────┬──────────────────────────────────────────────────────┤
  │  Scenario                   │  Trigger Condition                                   │
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S1: Intake Processing      │  New Request created                                 │
  │                             │  Queue = Enterprise Mktg & Ops                       │
  │                             │  Type = Email Program (Batch)                        │
  │                             │  Region = APAC or AMER                               │
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S2: Unified Project        │  S1 completes successfully                           │
  │  Creation                   │  Request data validated                              │
  │                             │  Template selected by region (APAC or AMER)          │
  │                             │  Multi CTA: Build task duration set to +1 day        │
  │                             │  If SFDC flag: SFDC Tracking task added to project   │
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S3: Task Change Watcher    │  Watch Event: Task value updated                     │
  │  (Continuous)               │  Within a Unified Campaign Project                   │
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S4: Email Governance       │  Watch Event: Task Status = Complete                 │
  │  Task Watch                 │  Task Name = "Email Governance Task"                 │
  │                             │  Project = Unified Campaign Project                  │
  │                             │  Activates Phase 2 (Operations) tasks in project     │
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S6: Sync Object Build      │  Ops Email Summary task complete in unified project  │
  │  + SnapLogic API Call       │  MCZ review cycle -> Pre-Sync task complete          │
  │                             │  Build task complete -> sends Document ID to Snaplogic│
  ├─────────────────────────────┼──────────────────────────────────────────────────────┤
  │  S7: SnapLogic Response     │  Watch Event: Sync object document updated           │
  │  Watch + Processing         │  with new version (SnapLogic response payload)       │
  │                             │  Decode -> update unified project -> QA task In Progress│
  └─────────────────────────────┴──────────────────────────────────────────────────────┘
```

---

## End-to-End Fusion and Adobe I/O Orchestration Flow

```
  [REQUEST SUBMIT]
       |
       v
  S1: Watch Event --> Filter (APAC/AMER, Email Batch)
       |
       +---> Adobe I/O: overview-build --> initial overview written to marketer project
       +---> Planning: Request Table record created
       |
       v
  S2: Unified Project Creation
       |
       +---> Select template by region (APAC or AMER)
       +---> Create unified project --> assign team/owner --> set start date
       +---> If Multi CTA: set Build task duration = standard + 1 day
       +---> Transfer intake form data --> project task forms
       +---> If content provided: copy content fields to Content task
       +---> Adobe I/O: content.js generated --> stored as WF Document on Content task
       |         +--> Document ID saved to Planning Request Table
       +---> Adobe I/O: validation-summary --> validation results on unified project
       +---> If SFDC flag: add SFDC Tracking task to Phase 2 of unified project
       |
       |  [If child/net-language request: route to existing unified project language task]

  ------------------------- CONTINUOUS LOOP -----------------------------------------
  S3: Task Change Watcher (fires on any task update in unified project)
       +---> Adobe I/O: overview-build --> updated overview on unified project
       +---> Adobe I/O: validation-summary --> re-evaluated; updated on project
       +--> content.js: new version saved on Content task document
  -----------------------------------------------------------------------------------

       |
       v
  S4: Email Governance Task Completed (unified project — Phase 1 → Phase 2 trigger)
       |
       +---> Adobe I/O: overview-summary-ops --> ops-level overview written to unified project
       +---> Phase 2 pre-sync pending tasks --> marked complete
       +--> MCZ-Pre-Sync Summary task --> set In Progress

       |
       v
  S6: Pre-Sync Summary task In Progress (unified project — Phase 2)
       |
       +---> Adobe I/O: sync-object-build
       |         +--> input: content.js + tokens + program shells + SFDC IDs
       |         +--> output: MCZ Sync Object JSON --> WF Document
       |         |            Document ID --> Planning Request Table
       |         +--> MCZ details text --> written to MCZ-Pre-Sync Summary task
       |
       +--> [REVIEW LOOP]
       |     Operations team reviews MCZ details
       |     +--> Changes needed? --> update fields --> re-trigger sync-object-build --> loop
       |     +--> Approved? --> mark MCZ-Pre-Sync Summary task Complete
       |
       +---> Adobe I/O: overview-summary-ops --> final overview regenerated
       +--> Ops Build task --> set In Progress
                 |
                 +--> Build task Complete --> Fusion sends Sync Object Document ID to SnapLogic

       |
       v
  SnapLogic processes Sync Object --> Marketo API --> MCZ program provisioned

       |
       v
  S7: SnapLogic Response Watch
       |
       +---> Sync object document version update detected
       +---> Adobe I/O: snaplogic-response-processor
       |         +--> input: SnapLogic response JSON (new document version)
       |         +--> output: MCZ program URL + status + task flags + QA flag
       |
       +---> Workfront updates:
       |     +--> MCZ links written to unified project
       |     +--> Relevant tasks in unified project --> marked Complete
       |     +--> QA task in unified project --> set In Progress
       +--> Planning Request Table --> updated with MCZ program details and final status
```

---

## content.js Document Lifecycle

```
  [S2: Unified Project Created]
       |
       v
  Adobe I/O: overview-build creates initial content.js
       |
       v
  content.js v1 --> stored as WF Document attachment on Content task (Phase 1)
       |               Document ID saved in Planning Request Table
       |
       | [Any marketer task update - S3 fires]
       v
  Adobe I/O: overview-build + validation-summary update content.js
       |
       v
  content.js v2, v3 ... vN --> new version on same WF Document (versioned)

  +-----------------------------------------------------------+
  |               content.js JSON Structure                   |
  +-----------------------------------------------------------+
  |  metadata:     region, team, type, send date, request IDs |
  |  content:      subject, preview, headline, banner, body   |
  |                CTA text/URL, content image                |
  |  additionalCTAs: [ CTA2{...}, CTA3{...}, CTA4{...},       |
  |                    CTA5{...} ]                            |
  |  targeting:    option, field values                       |
  |  enrichment:   solution abbr, industry, POI prefix, team  |
  |  tokens:       [ {name, value, type}, ... ]               |
  |  validation:   { rules: [...], overallStatus, timestamp } |
  |  overview:     { marketerSummary, opsSummary, timestamp } |
  |  syncObject:   { documentId, status, mcz: {...} }         |
  |  sfdc:         { required, rtid, s_iid, gated, buttonType}|
  +-----------------------------------------------------------+
```

---

## Operations Phase – Task Structure and Key Milestones

> **Note:** Operations tasks are now Phase 2 of the Unified Campaign Project (see Project Template
> Structure above). There is no longer a separate Operations Project. Phase 2 is activated when
> the Email Governance Task (Phase 1) is marked complete. Fusion S5 (Ops Project Creation) has
> been eliminated; all project creation is handled by S2 (Unified Project Creation).

```
  +------------------------------------------------------------------+
  |         UNIFIED PROJECT — PHASE 2: OPERATIONS TASK FLOW         |
  |         (Activated by Email Governance Task completion)          |
  +------------------------------------------------------------------+
  |                                                                  |
  |  [Triggered by S4 when Email Governance Task marked complete]    |
  |                                                                  |
  |  Overview and Setup                                              |
  |  +--> Campaign Overview Summary task   [auto-completed by S4]    |
  |  +--> [SFDC Tracking task]             [if SFDC flag set; added  |
  |                                         to project by S2]        |
  |  +--> Ops Email Summary task           [completion triggers S6]  |
  |                                                                  |
  |  Pre-Sync MCZ Review                                             |
  |  +--> MCZ-Pre-Sync Summary task        [review / approve]        |
  |  |     +--> MCZ details written here by Adobe I/O               |
  |  |     +--> Ops team reviews / requests corrections             |
  |  +--> Build task (+1 day for Multi CTA) [set In Progress on      |
  |                                           Pre-Sync approval]     |
  |                                                                  |
  |  Provisioning and QA                                             |
  |  +--> SnapLogic submission             [Build task completion]   |
  |  +--> QA Task                          [set In Progress on       |
  |                                         MCZ success response]   |
  |  +--> Post-Launch / Verification task                            |
  +------------------------------------------------------------------+
```
