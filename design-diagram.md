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
                                                   Marketer Project Creation
                                                             │
                                                             ▼
                                                   [Workfront Project]─────────────────────────►[Planning Table]
                                                   Marketer Campaign                             Validation Rules
                                                   Project (Template)                                 │
                                                             │                                        │
                                                             ▼                                        ▼
                                                   [Email Governance Task]              [Adobe I/O / Fusion Function]
                                                             │                          Validation Summary Logic
                                                             │                                        │
                                                   [Watch Event Trigger]◄───────────────────────────┘
                                                   Task Completion Monitor
                                                             │
                                                             ▼
                                                   [Fusion Scenario 3]
                                                   Operations Project Creation
                                                   (Routing: Region/Team/CTA Type)
                                                             │
                                                   ┌─────────┴──────────┐
                                                   ▼                    ▼
                                            [Ops Project:         [Ops Project:
                                             APAC Team]            AMER Team]
                                                   │                    │
                                                   └─────────┬──────────┘
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
  USER SELECTS: Request Type = Email Program (Batch)
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
  │      └──► Show all region targeting fields (APAC/AMER/EMEA)  │
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
  │           If Multi → Show [Number of CTAs: 2–7]               │
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
  │  ├── Email Banner Image URL   (open text)                 │
  │  ├── Email Body               (rich text)                 │
  │  ├── Content Image URL        (open text)                 │
  │  ├── CTA Text                 (open text)                 │
  │  └── CTA URL                  (open text)                 │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 2  (shown when CTA count >= 2)            │
  │  ├── CTA 2 Email Headline     (open text)                 │
  │  ├── CTA 2 Email Body         (rich text)                 │
  │  ├── CTA 2 CTA Text           (open text)                 │
  │  ├── CTA 2 CTA URL            (open text)                 │
  │  └── CTA 2 Content Image URL  (open text)                 │
  ├───────────────────────────────────────────────────────────┤
  │  ADDITIONAL CTA 3  (shown when CTA count >= 3)            │
  │  ├── CTA 3 Email Headline     (open text)                 │
  │  ├── CTA 3 Email Body         (rich text)                 │
  │  ├── CTA 3 CTA Text           (open text)                 │
  │  ├── CTA 3 CTA URL            (open text)                 │
  │  └── CTA 3 Content Image URL  (open text)                 │
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

  LOOKUP TABLES (Read-Only Reference Data – migrated from Airtable)
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
  ┌───────────────────────────────────────────────────┐
  │        MARKETER CAMPAIGN PROJECT TEMPLATE         │
  ├───────────────────────────────────────────────────┤
  │  Phase 1: Campaign Intake & Governance            │
  │  ├── Email Governance Review Task                 │
  │  │     └── [Form Attached: Governance Checklist]  │
  │  └── Targeting & Content Confirmation Task        │
  │                                                   │
  │  Phase 2: Campaign Setup                          │
  │  ├── Targeting Criteria Task                      │
  │  │     └── [Form: Region-specific Targeting]      │
  │  └── Content Task                                 │
  │        └── [Form: CTA Content Fields]             │
  │                                                   │
  │  Phase 3: Review & Approval                       │
  │  └── Stakeholder Review Task                      │
  └───────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────┐
  │        OPERATIONS PROJECT TEMPLATES               │
  │        (Routing: Region × CTA Type)               │
  ├───────────────────────────────────────────────────┤
  │                                                   │
  │  Template A: APAC – Single CTA                    │
  │  Template B: APAC – Multi CTA                     │
  │  Template C: AMER – Single CTA                    │
  │  Template D: AMER – Multi CTA                     │
  │  Template E: EMEA – Single CTA (reference)        │
  │  Template F: EMEA – Multi CTA (reference)         │
  │                                                   │
  │  Each template contains:                          │
  │  ├── Ops Setup Tasks                              │
  │  ├── MCZ Provisioning Tasks                       │
  │  ├── QA / Validation Tasks                        │
  │  └── Launch & Post-Launch Tasks                   │
  └───────────────────────────────────────────────────┘
```

---

## Fusion Scenario Trigger Map

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                    WORKFRONT FUSION SCENARIO TRIGGERS                    │
  ├──────────────────────┬───────────────────────────────────────────────────┤
  │  Scenario            │  Trigger Condition                                │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S1: Intake          │  New Request created                              │
  │  Processing          │  Queue = Enterprise Mktg & Ops                    │
  │                      │  Type = Email Program (Batch)                     │
  │                      │  Region = APAC or AMER                            │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S2: Marketer        │  S1 completes successfully                        │
  │  Project Creation    │  Request validated                                 │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S3: Email Gov       │  Watch Event: Task Status = Complete              │
  │  Watch Event         │  Task Name = "Email Governance"                   │
  │                      │  Project = Marketer Campaign Project              │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S4: Ops Project     │  S3 watch event fires                             │
  │  Creation            │  Routing logic evaluates:                         │
  │                      │  Region + Team + CTA Type                         │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S5: SnapLogic       │  MCZ Sync Object generated                        │
  │  API Invocation      │  Ops Project provisioning task triggered          │
  ├──────────────────────┼───────────────────────────────────────────────────┤
  │  S6: SnapLogic       │  Watch for document update in Workfront           │
  │  Response Watch      │  SnapLogic response field populated               │
  │                      │  Process success/failure status                   │
  └──────────────────────┴───────────────────────────────────────────────────┘
```
