# Campaign Orchestration Platform – User Stories

> **Reference Pattern:** Follows ADO Backlog structure for Epic: *Campaign Orchestration Platform Build*
> Stories are derived from the 18-task backlog spanning Intake & Request Management, Data & Lookup Management, Validation Framework, Campaign Project Automation, and MCZ Integration & Provisioning.

---

## Epic: Campaign Orchestration Platform Build

---

### US-001: APAC Intake Form – Base Configuration

**Title:** Configure standardized Workfront intake form for APAC email campaign requests

**As a** Marketing Operations user in the APAC region,
**I want** a dynamic and standardized intake form within the Enterprise Marketing & Operations Request Queue — including a Send Date field above Targeting Criteria and APAC-specific targeting fields rendered when Region = APAC,
**So that** I can submit complete, accurate, and region-consistent campaign requests aligned with global EMEA standards.

**Feature:** Intake & Request Management
**Task Reference:** Task 1

> **Design Note:** The APAC and AMER intake forms share the same solution design and form structure. Region-specific differences are limited to a subset of Targeting Criteria fields unique to each region. Send Date, content fields, and CTA sections are identical across both forms.

---

### US-002: AMER Intake Form – Base Configuration

**Title:** Configure standardized Workfront intake form for AMER email campaign requests

**As a** Marketing Operations user in the AMER region,
**I want** a dynamic and standardized intake form with the Enterprise GTM Segments field (AMER-only), a Send Date field above Targeting Criteria, and AMER-specific targeting fields rendered when Region = AMER — all within the Enterprise Marketing & Operations Request Queue,
**So that** I can submit consistent and complete campaign requests that align with EMEA global standards while accommodating AMER-specific requirements.

**Feature:** Intake & Request Management
**Task Reference:** Task 2

> **Design Note:** Built from the same shared solution design as the APAC form. Only the region-specific Targeting Criteria fields (and the Enterprise GTM Segments field) differ.

---

### US-003: Dynamic Targeting Criteria – Copy from Last Request

**Title:** Allow marketers to automatically copy targeting from their most recent campaign request

**As a** marketer submitting a repeat or similar campaign,
**I want** to select "Copy targeting from my last request" during intake form submission,
**So that** the targeting criteria from my most recent campaign are automatically applied, the targeting task is marked complete, and I can refine it later if needed.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-004: Dynamic Targeting Criteria – Copy from Specific Request

**Title:** Allow marketers to copy targeting from a selected past campaign request

**As a** marketer who wants to reuse a known successful targeting setup,
**I want** to select "Copy targeting from a specific request" and provide a Request ID,
**So that** the exact targeting criteria from that specified request are copied into my new campaign request, and the targeting task is marked complete.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-005: Dynamic Targeting Criteria – Add Targeting Now

**Title:** Allow marketers to define targeting criteria inline during request submission, with shared and region-specific fields rendered based on selected region

**As a** marketer who wants full control over targeting from the start,
**I want** to select "Add targeting criteria now" and have the targeting fields rendered inline — common fields shared across APAC and AMER, plus the small subset of region-specific targeting fields applicable to my selected region (Simple or Detailed mode),
**So that** I can provide complete and accurate targeting information upfront without seeing irrelevant fields from other regions, enabling faster downstream processing and campaign comparison.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-006: Dynamic Targeting Criteria – Provide Targeting Later

**Title:** Allow marketers to defer targeting submission to a later stage

**As a** marketer who does not yet have finalized targeting data or is awaiting approvals,
**I want** to select "Provide targeting later" during intake form submission,
**So that** the request is created and linked to me without requiring targeting input now, and I can fill in targeting details later within the assigned task.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-007: Dynamic Content Option – Provide Content Later

**Title:** Allow marketers to submit a campaign request without providing content immediately

**As a** marketer who needs to submit a campaign request before content is finalized,
**I want** to select "Provide content later" as the content option,
**So that** the request is created with a pending content task that can be completed after submission.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-008: Dynamic Content Option – Copy from Last Request

**Title:** Allow marketers to copy content from their most recent campaign request

**As a** marketer reusing content from a recent campaign,
**I want** to select "Copy content from my last request",
**So that** the content is automatically populated from my most recent matching request, the content task is marked complete, and I can edit it within the task if needed.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-009: Dynamic Content Option – Use Content from Specific Request

**Title:** Allow marketers to reference and copy content from a specific past request

**As a** marketer wanting to reuse content from a particular past campaign,
**I want** to select "Use content from a specific request" and enter a Request ID,
**So that** the content from that request is copied into my new campaign, the task is marked complete, and I retain the ability to make edits later.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-010: Dynamic Content Option – Add Content Now with Multi-CTA Support

**Title:** Allow marketers to submit multi-CTA campaign content during intake form

**As a** marketer with ready content for a multi-CTA email campaign,
**I want** to select "Add content now", choose CTA Type as Multi CTA, select the number of CTAs (2–5), and have content sections dynamically generated per CTA,
**So that** I can provide all campaign content upfront and have it validated during the request submission process.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-011: Fusion Scenario – Intake Request Processing Trigger

**Title:** Automatically detect and process new APAC/AMER email campaign intake requests via Workfront Fusion

**As a** campaign operations system,
**I want** a Workfront Fusion scenario to watch for newly created requests in the Enterprise Marketing & Operations Request Queue filtered by region (APAC/AMER) and request type (Email Program Batch),
**So that** campaign orchestration is automatically initiated upon request submission without manual intervention.

**Feature:** Intake & Request Management
**Task Reference:** Task 3

---

### US-012: Campaign Request Data Storage in Workfront Planning

**Title:** Persist structured campaign request data in a Workfront Planning table

**As a** campaign operations system,
**I want** all captured intake form data to be stored in a structured Workfront Planning table (Campaign Request Data),
**So that** downstream automation scenarios and validation logic have reliable, queryable access to campaign request details.

**Feature:** Intake & Request Management
**Task Reference:** Task 4

---

### US-013: Request Overview Summary Generation

**Title:** Automatically generate a human-readable request overview for each campaign submission

**As a** campaign operations manager,
**I want** a Fusion Function or Adobe I/O action to generate a structured overview summary for each campaign request based on the intake form data,
**So that** all stakeholders have a clear, consolidated view of the campaign details without manually reviewing raw form data.

**Feature:** Intake & Request Management
**Task Reference:** Task 5

---

### US-014: Migrate Airtable Lookup Tables to Workfront Planning

**Title:** Recreate all Airtable lookup tables within Workfront Planning

**As a** campaign operations architect,
**I want** all existing Airtable lookup tables to be migrated and recreated within Workfront Planning,
**So that** the campaign orchestration platform operates on a single, governed data platform and eliminates dependency on Airtable.

**Feature:** Data & Lookup Management
**Task Reference:** Task 6

---

### US-015: Validation Rules Lookup Table

**Title:** Create a Workfront Planning lookup table for campaign validation rules

**As a** campaign operations system,
**I want** a dedicated Workfront Planning table to store all campaign validation rules (including rule type, logic, error messages, severity, and region scope),
**So that** validation logic can reference a centralized, maintainable rule set rather than hardcoded conditions.

**Feature:** Validation Framework
**Task Reference:** Task 7

---

### US-016: Interactive Message Templates with Dynamic Placeholders

**Title:** Create a lookup table for reusable automated message templates with dynamic placeholders

**As a** campaign operations system,
**I want** a Workfront Planning lookup table storing message templates containing dynamic placeholders (e.g., `{Name}`, `{CampaignID}`, `{SendDate}`, `{Region}`),
**So that** automated notifications sent via Issues, Projects, and Tasks are personalized, consistent, and easy to maintain.

**Feature:** Validation Framework
**Task Reference:** Task 8

---

### US-017: Request Validation Summary Generation

**Title:** Automatically generate a validation summary for each campaign request

**As a** campaign operations system,
**I want** a Fusion Function or Adobe I/O action to evaluate each campaign request against the Validation Rules lookup table and produce a structured validation summary,
**So that** incomplete or non-compliant requests are flagged before any downstream project or provisioning activity begins.

**Feature:** Validation Framework
**Task Reference:** Task 9

---

### US-018: Marketer Campaign Project Template Design

**Title:** Design a Workfront project template for marketer campaign execution

**As a** campaign project manager,
**I want** a Workfront project template pre-configured with all standard phases, tasks, and associated forms for email campaign execution,
**So that** every marketer campaign project is created consistently and the team doesn't need to manually build project structures for each campaign.

**Feature:** Campaign Project Automation
**Task Reference:** Task 10

---

### US-019: Operations Project Templates by Routing Logic

**Title:** Design multiple operations project templates based on region, team, and CTA type

**As a** campaign operations team lead,
**I want** distinct Workfront project templates for each routing combination (APAC/AMER × Single CTA/Multi CTA),
**So that** operations projects are automatically structured with the correct tasks and assignments matching the specific campaign configuration.

**Feature:** Campaign Project Automation
**Task Reference:** Task 11

---

### US-020: Fusion Scenario – Automated Marketer Project Creation

**Title:** Automatically create marketer campaign projects from validated intake requests via Workfront Fusion

**As a** campaign operations system,
**I want** a Workfront Fusion scenario to automatically create a marketer project from the validated campaign request using the appropriate project template,
**So that** the campaign execution lifecycle begins immediately upon request validation without requiring manual project setup.

**Feature:** Campaign Project Automation
**Task Reference:** Task 12

---

### US-021: Email Governance Task Completion Watch Event

**Title:** Monitor completion of the Email Governance task within marketer projects

**As a** campaign operations system,
**I want** a Workfront Fusion watch event to trigger when the Email Governance task within a marketer project is marked complete,
**So that** the downstream operations project creation process is automatically initiated at the right point in the workflow.

**Feature:** Campaign Project Automation
**Task Reference:** Task 13

---

### US-022: Fusion Scenario – Automated Operations Project Creation

**Title:** Automatically create operations projects based on routing logic via Workfront Fusion

**As a** campaign operations system,
**I want** a Workfront Fusion scenario to evaluate campaign routing conditions (region, team, CTA type) and automatically create the appropriate operations project using the matched template,
**So that** operations teams receive fully structured projects without manual coordination from campaign managers.

**Feature:** Campaign Project Automation
**Task Reference:** Task 14

---

### US-023: MCZ Taxonomy Lookup Table in Workfront Planning

**Title:** Create a Workfront Planning table to store MCZ taxonomy data for Marketo provisioning

**As a** campaign operations system,
**I want** a Workfront Planning table containing MCZ taxonomy data (shells, folders, tokens, programs) with regional and campaign-type mappings,
**So that** MCZ payload generation logic has reliable reference data for constructing Marketo-compliant API payloads.

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 15

---

### US-024: MCZ Sync Object Payload Generation

**Title:** Generate MCZ Sync Object JSON payloads for SnapLogic using Fusion or Adobe I/O

**As a** campaign operations system,
**I want** a Workfront Fusion Function or Adobe I/O action to generate a valid MCZ Sync Object (.JSON structure) by combining campaign request data with MCZ taxonomy lookup data,
**So that** SnapLogic receives a well-formed payload ready for Marketo API integration without manual JSON construction.

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 16

---

### US-025: Fusion Scenario – SnapLogic API Invocation

**Title:** Transmit MCZ payloads to SnapLogic via a dedicated Workfront Fusion scenario

**As a** campaign operations system,
**I want** a Workfront Fusion scenario to invoke the SnapLogic API with the generated MCZ Sync Object payload,
**So that** campaign provisioning requests are automatically submitted to the downstream Marketo platform without manual data transfer.

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 17

---

### US-026: SnapLogic Response Processing Watch Event

**Title:** Detect and process SnapLogic provisioning responses to update campaign status in Workfront

**As a** campaign operations system,
**I want** a Workfront Fusion watch event to monitor SnapLogic response documents and process success or failure states,
**So that** Workfront campaign records are automatically updated with the MCZ provisioning status, enabling real-time visibility into provisioning outcomes.

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 18

---

### US-027: Taxonomy Governance – Central Reference Maintenance

**Title:** Maintain a central taxonomy and field naming reference document for all regions

**As a** Marketing Operations governance lead,
**I want** a centrally maintained taxonomy reference document (Excel/SharePoint) that defines all intake form field labels, variable names, backend values, data types, and parent-child relationships,
**So that** all regions (APAC, AMER, EMEA) follow consistent naming conventions and new fields can be validated against the reference before implementation.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-028: Test Queue Validation Before Production Deployment

**Title:** Validate all intake form changes in a temporary test queue before production migration

**As a** Workfront platform administrator,
**I want** all new intake form configurations to be first deployed and tested in a temporary/test queue topic,
**So that** configuration errors are caught before impacting live campaign request submissions in production.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-029: Cross-Region Targeting Criteria Standardization

**Title:** Define a standardized targeting model that minimizes region-specific field variations

**As a** Marketing Operations architect,
**I want** to analyze targeting fields across APAC, AMER, and EMEA and define a consolidated, standardized targeting model,
**So that** maintenance overhead is reduced, cross-region reporting is simplified, and targeting field duplication is eliminated.

**Feature:** Intake & Request Management
**Task Reference:** Task 1, Task 2

---

### US-030: Adobe I/O Scripts for Business Logic Execution

**Title:** Implement reusable Adobe I/O JavaScript actions for campaign logic execution

**As a** platform engineer,
**I want** reusable Adobe I/O JavaScript actions to handle business logic (overview generation, validation, MCZ payload building) that is too complex or stateful for native Fusion modules,
**So that** orchestration logic is maintainable, version-controlled, and testable independently of Workfront Fusion scenarios.

**Feature:** Validation Framework / MCZ Integration & Provisioning
**Task Reference:** Task 5, Task 9, Task 16

---

### US-031: Content Task – JSON Document Attachment (content.js)

**Title:** Generate and store campaign content as a structured JSON document attached to the Workfront content task

**As a** campaign operations system,
**I want** Adobe I/O to generate a structured `content.js` JSON file that captures all campaign content, lookup enrichment data, validation results, and overview summaries — and store it as a versioned document attachment under the marketer project's Content task,
**So that** all campaign data is consolidated in one reference document that Fusion scenarios and Adobe I/O actions can read and update throughout the campaign lifecycle, compensating for Workfront Planning column field limitations.

**Acceptance Notes:**
- The file is created and updated as a Workfront Document on the Content task
- Each update creates a new version of the document (versioned attachment)
- Content is updated whenever marketer task values change (content addition, edits, language additions)
- The JSON includes: intake content, CTA sections, lookup-enriched fields, validation summary, overview summary, sync object data

**Feature:** Campaign Project Automation
**Task Reference:** Task 5, Task 10, Task 12

---

### US-032: Planning Request Table – Parent/Child Net Language Request Linking

**Title:** Link additional-language campaign requests as child records to the parent request in the Planning request table

**As a** campaign operations system,
**I want** the Workfront Planning request table to support parent and child request relationships — where the parent is the original campaign request (main language) and a child is a new intake request submitted for the same campaign in a different language, linked by selecting the existing marketer project during submission,
**So that** all language variants of a campaign are tracked under one parent campaign record, content from each child request is automatically transferred to the corresponding language task in the existing marketer project, and the Planning table reflects the full multi-language scope of the campaign.

**Acceptance Notes:**
- Child request submission uses the standard intake form with an additional field to select the parent marketer project
- Fusion scenario detects the parent project reference and routes content to the correct language task
- The Planning request table stores both parent Request ID and child Request ID with relationship links
- Document IDs (content.js, sync object) are tracked at the parent record level

**Feature:** Intake & Request Management / Data & Lookup Management
**Task Reference:** Task 3, Task 4, Task 12

---

### US-033: Planning Table Enrichment via PL Connections (Solution, Industry, POI, Team)

**Title:** Automatically enrich Planning request table records using PL connections to lookup tables for solution, industry, POI, and team data

**As a** campaign operations system,
**I want** the Workfront Planning request table to be connected to lookup tables (Solution, Industry, Product of Interest, Team) via Planning Link (PL) connections,
**So that** when a field value (e.g., Solution) is set or updated in the request table, the connected lookup table automatically supplies enriched attributes (e.g., solution abbreviation, POI tokens, team codes) that are then used during sync object and token generation — without requiring manual data entry.

**Acceptance Notes:**
- PL connections are established between the request table and each relevant lookup table
- Example: selecting a Solution populates its abbreviation from the Solutions lookup table; this abbreviation is used in token construction during sync object generation
- POI (Product of Interest) = specific Adobe product the campaign targets; used for token and program shell naming
- Enrichment triggers automatically as and when content is added or updated in the request table

**Feature:** Data & Lookup Management
**Task Reference:** Task 6, Task 15, Task 16

---

### US-034: Program Shell Lookup Table for Dynamic MCZ Program Shell Generation

**Title:** Create a Workfront Planning program shell lookup table to support dynamic Marketo program shell generation

**As a** campaign operations system,
**I want** a Workfront Planning table that stores program shell templates mapped by solution, region, campaign type, and POI,
**So that** the MCZ sync object generation logic can dynamically select the correct program shell configuration for each campaign and construct the Marketo program provisioning payload accurately.

**Acceptance Notes:**
- Table contains: Shell ID, Shell Name, Region, Campaign Type (Single/Multi CTA), Solution, POI mapping, Folder Path, Token Set reference
- Used by the Adobe I/O sync object generation action to resolve the correct shell for a given campaign
- Replaces manual shell lookup previously done in Airtable

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 15, Task 16

---

### US-035: Tokens Lookup Table in Workfront Planning

**Title:** Create a Workfront Planning tokens lookup table to store Marketo token definitions

**As a** campaign operations system,
**I want** a dedicated Workfront Planning table that stores all Marketo token definitions including token names, default values, and their mapping to campaign fields,
**So that** the Adobe I/O sync object generation action can dynamically populate token values from campaign request data and Planning enrichment, producing a complete and accurate token payload for Marketo provisioning.

**Acceptance Notes:**
- Tokens stored include: program-level tokens, folder tokens, content tokens, tracking tokens
- Token values are resolved dynamically using enriched data from the request table and PL-connected lookup tables
- Token table is referenced during sync object build by the Adobe I/O action

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 15, Task 16

---

### US-036: SFDC Campaign ID Tracking Task in Operations Project

**Title:** Automatically add a Salesforce Campaign ID tracking task to the operations project when SFDC ID creation is requested

**As a** campaign operations system,
**I want** the Fusion scenario to detect when the marketer has checked "Do you require Salesforce Campaign ID Creation as part of this request?" in the intake form and automatically add a dedicated SFDC Tracking task to the operations project,
**So that** the operations team can supply the required Salesforce tracking IDs (s_rtid, s_iid), gated/ungated flag, and button type — which are then included in the sync object during MCZ provisioning.

**Acceptance Notes:**
- Checkbox on intake form triggers task creation in the operations project
- SFDC Tracking task collects: Salesforce Campaign ID (rtid), Internal SFDC ID (s_iid), Gated/Ungated, Button Type
- These values are consumed by the Adobe I/O sync object generation action before sending to SnapLogic
- Task must be completed before the sync object build step can proceed

**Feature:** MCZ Integration & Provisioning / Campaign Project Automation
**Task Reference:** Task 14, Task 16

---

### US-037: Pre-Sync MCZ Details Review and Approval Cycle

**Title:** Enable operations team review and iterative correction of MCZ details before final sync object submission

**As a** campaign operations team member,
**I want** to review the generated MCZ details (shells, folders, tokens, program structure) in the MCZ-Pre-Sync Summary task before the sync object is submitted to SnapLogic, and be able to request changes that trigger a regeneration cycle,
**So that** any corrections to MCZ configuration are made and reviewed before an irreversible provisioning call is sent to Marketo via SnapLogic.

**Acceptance Notes:**
- On Ops email summary task completion → sync object is built → MCZ details are written to the MCZ-Pre-Sync Summary task
- Operations team reviews; if changes needed → they update fields → Fusion/Adobe I/O detects update → MCZ details regenerated and posted back for re-review
- When MCZ-Pre-Sync Summary task is marked complete → final overview summary is regenerated → Build task is set to In Progress
- Build task completion → sync object document ID is submitted to SnapLogic API

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 16, Task 17

---

### US-038: QA Task Initiation After MCZ Provisioning Success

**Title:** Automatically set the QA task to In Progress in both the operations and marketer projects after successful MCZ provisioning

**As a** campaign operations system,
**I want** the Fusion watch event processing the SnapLogic response to detect a successful provisioning status and automatically set the QA task to In Progress in the operations project (and complete relevant tasks in both projects),
**So that** the operations and marketing teams are immediately notified that MCZ provisioning is complete and the campaign is ready for quality assurance verification.

**Acceptance Notes:**
- Successful SnapLogic response → Workfront projects updated with MCZ program links (accessible URLs)
- Specific tasks in both marketer and operations projects are marked complete
- QA task in operations project is set to In Progress
- Response data decoded by Adobe I/O action and written to both projects

**Feature:** MCZ Integration & Provisioning / Campaign Project Automation
**Task Reference:** Task 18

---

### US-039: Adobe I/O Action – Overview Build Script

**Title:** Implement an Adobe I/O action to build and update the campaign request overview on the marketer project

**As a** platform engineer,
**I want** a standalone Adobe I/O JavaScript action that accepts the current campaign JSON object as input and generates a formatted request overview summary, updating it on the marketer project as a task note or description,
**So that** the overview is always current and reflects any changes made to campaign task values — and Fusion does not need to contain this complex formatting logic.

**Acceptance Notes:**
- Triggered by Fusion as an Adobe I/O module call whenever any marketer project task value changes
- Input: current content.js JSON object
- Output: formatted HTML/text overview string written to the marketer project
- Action runs independently and returns a JSON response

**Feature:** Campaign Project Automation / Validation Framework
**Task Reference:** Task 5, Task 12

---

### US-040: Adobe I/O Action – Validation Summary Script

**Title:** Implement an Adobe I/O action to evaluate campaign request data against validation rules and generate a validation summary

**As a** platform engineer,
**I want** a standalone Adobe I/O JavaScript action that takes the campaign JSON object as input, evaluates it against all applicable validation rules from the Planning validation rules table, and returns a structured validation summary,
**So that** incomplete or policy-violating campaign requests are flagged automatically and the summary is printed on the marketer project before any downstream provisioning activity begins.

**Acceptance Notes:**
- Triggered by Fusion whenever marketer task values change
- Re-evaluates and re-executes on every relevant change
- Input: content.js JSON + validation rules payload
- Output: validation summary JSON (rule results, severity, pass/fail status) written to project

**Feature:** Validation Framework
**Task Reference:** Task 9

---

### US-041: Adobe I/O Action – Sync Object Build and MCZ Details Generation

**Title:** Implement an Adobe I/O action to construct the MCZ sync object payload and generate MCZ provisioning details

**As a** platform engineer,
**I want** a standalone Adobe I/O JavaScript action that takes the campaign JSON object (including content, enriched lookup data, tokens, program shells) as input and produces a valid MCZ Sync Object JSON payload along with human-readable MCZ details,
**So that** the sync object is built using complex logic that cannot be replicated in Fusion natively, and the MCZ details can be reviewed by the operations team before submission to SnapLogic.

**Acceptance Notes:**
- Input: content.js JSON, token data, program shell reference, SFDC tracking IDs (if applicable)
- Output: MCZ Sync Object JSON (stored as Workfront document with tracked ID in Planning) + MCZ details text written to MCZ-Pre-Sync Summary task
- Document ID of the sync object JSON is recorded in the Planning request table

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 16

---

### US-042: Adobe I/O Action – SnapLogic Response Processor

**Title:** Implement an Adobe I/O action to decode and process the SnapLogic provisioning response

**As a** platform engineer,
**I want** a standalone Adobe I/O JavaScript action that takes the SnapLogic response JSON (returned as a new version of the same sync object document) as input, decodes the provisioning status and MCZ program details, and returns structured update instructions,
**So that** Fusion can apply the decoded results to update both the marketer and operations projects with MCZ links, task completion statuses, and QA readiness flags — without embedding this decoding logic in Fusion itself.

**Acceptance Notes:**
- Triggered by Fusion's SnapLogic response watch event when the sync object document is updated with a new version
- Input: SnapLogic response JSON
- Output: structured JSON with MCZ program URL, status (success/failure), task update instructions, QA flag
- Fusion uses the output to apply updates to Workfront projects and planning tables

**Feature:** MCZ Integration & Provisioning
**Task Reference:** Task 18

---

## Summary Table

| Story ID | Feature | Title |
|----------|---------|-------|
| US-001 | Intake & Request Management | APAC Intake Form – Base Configuration |
| US-002 | Intake & Request Management | AMER Intake Form – Base Configuration |
| US-003 | Intake & Request Management | Targeting – Copy from Last Request |
| US-004 | Intake & Request Management | Targeting – Copy from Specific Request |
| US-005 | Intake & Request Management | Targeting – Add Targeting Now |
| US-006 | Intake & Request Management | Targeting – Provide Targeting Later |
| US-007 | Intake & Request Management | Content – Provide Content Later |
| US-008 | Intake & Request Management | Content – Copy from Last Request |
| US-009 | Intake & Request Management | Content – Use Content from Specific Request |
| US-010 | Intake & Request Management | Content – Add Content Now (Multi-CTA) |
| US-011 | Intake & Request Management | Fusion – Intake Request Processing Trigger |
| US-012 | Intake & Request Management | Campaign Request Data Storage in Planning |
| US-013 | Intake & Request Management | Request Overview Summary Generation |
| US-014 | Data & Lookup Management | Migrate Airtable Lookup Tables to Planning |
| US-015 | Validation Framework | Validation Rules Lookup Table |
| US-016 | Validation Framework | Interactive Message Templates with Placeholders |
| US-017 | Validation Framework | Request Validation Summary Generation |
| US-018 | Campaign Project Automation | Marketer Campaign Project Template Design |
| US-019 | Campaign Project Automation | Operations Project Templates by Routing Logic |
| US-020 | Campaign Project Automation | Fusion – Automated Marketer Project Creation |
| US-021 | Campaign Project Automation | Email Governance Task Completion Watch Event |
| US-022 | Campaign Project Automation | Fusion – Automated Operations Project Creation |
| US-023 | MCZ Integration & Provisioning | MCZ Taxonomy Lookup Table in Planning |
| US-024 | MCZ Integration & Provisioning | MCZ Sync Object Payload Generation |
| US-025 | MCZ Integration & Provisioning | Fusion – SnapLogic API Invocation |
| US-026 | MCZ Integration & Provisioning | SnapLogic Response Processing Watch Event |
| US-027 | Intake & Request Management | Taxonomy Governance – Central Reference Maintenance |
| US-028 | Intake & Request Management | Test Queue Validation Before Production Deployment |
| US-029 | Intake & Request Management | Cross-Region Targeting Criteria Standardization |
| US-030 | Validation / MCZ Integration | Adobe I/O Scripts for Business Logic Execution |
| US-031 | Campaign Project Automation | Content Task – JSON Document Attachment (content.js) |
| US-032 | Intake & Request Management | Planning Request Table – Parent/Child Net Language Request Linking |
| US-033 | Data & Lookup Management | Planning Table Enrichment via PL Connections (Solution, Industry, POI, Team) |
| US-034 | MCZ Integration & Provisioning | Program Shell Lookup Table for Dynamic MCZ Generation |
| US-035 | MCZ Integration & Provisioning | Tokens Lookup Table in Workfront Planning |
| US-036 | MCZ Integration & Provisioning | SFDC Campaign ID Tracking Task in Operations Project |
| US-037 | MCZ Integration & Provisioning | Pre-Sync MCZ Details Review and Approval Cycle |
| US-038 | MCZ Integration & Provisioning | QA Task Initiation After MCZ Provisioning Success |
| US-039 | Campaign Project Automation | Adobe I/O Action – Overview Build Script |
| US-040 | Validation Framework | Adobe I/O Action – Validation Summary Script |
| US-041 | MCZ Integration & Provisioning | Adobe I/O Action – Sync Object Build and MCZ Details Generation |
| US-042 | MCZ Integration & Provisioning | Adobe I/O Action – SnapLogic Response Processor |
