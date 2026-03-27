# Campaign Orchestration Platform – User Stories

> **Reference Pattern:** Follows ADO Backlog structure for Epic: *Campaign Orchestration Platform Build*
> Stories are derived from the 18-task backlog spanning Intake & Request Management, Data & Lookup Management, Validation Framework, Campaign Project Automation, and MCZ Integration & Provisioning.

---

## Epic: Campaign Orchestration Platform Build

---

### US-001: APAC Intake Form – Base Configuration

**Title:** Configure standardized Workfront intake form for APAC email campaign requests

**As a** Marketing Operations user in the APAC region,
**I want** a dynamic and standardized intake form within the Enterprise Marketing & Operations Request Queue,
**So that** I can submit complete, accurate, and region-consistent campaign requests aligned with global EMEA standards.

**Feature:** Intake & Request Management
**Task Reference:** Task 1

---

### US-002: AMER Intake Form – Base Configuration

**Title:** Configure standardized Workfront intake form for AMER email campaign requests

**As a** Marketing Operations user in the AMER region,
**I want** a dynamic and standardized intake form with region-specific fields (e.g., Enterprise GTM Segments) within the Enterprise Marketing & Operations Request Queue,
**So that** I can submit consistent and complete campaign requests that align with EMEA global standards while accommodating AMER-specific requirements.

**Feature:** Intake & Request Management
**Task Reference:** Task 2

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

**Title:** Allow marketers to define targeting criteria inline during request submission

**As a** marketer who wants full control over targeting from the start,
**I want** to select "Add targeting criteria now" and have all region-specific targeting fields rendered inline (Simple or Detailed mode),
**So that** I can provide complete and accurate targeting information upfront, enabling faster downstream processing and campaign comparison.

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
**I want** to select "Add content now", choose CTA Type as Multi CTA, select the number of CTAs (2–7), and have content sections dynamically generated per CTA,
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
