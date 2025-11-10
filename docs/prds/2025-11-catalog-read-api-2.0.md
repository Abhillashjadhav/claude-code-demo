# Catalog Read API 2.0
Overview
Project Objective
Enable external partners (PIMs, direct suppliers) and internal Wayfair systems to read complete product data in the new CDF 2.0 model via a GraphQL Read API with full parity to PA 2.0 (option grouping, pipeline status, barriers, composites/kits), while maintaining backward compatibility with legacy identifiers through an ID Mapper.
Primary users: PIM developers, supplier integrators, internal merchandising and analytics tools.
Contextual Information & Data
Read API 1.0 (legacy identifiers) serves ~91 suppliers via 11 PIMs with ~9M annual reads.
CDF 2.0 and PA 2.0 introduce new identifiers (MPLVID/MPLID/ChoiceID), option grouping, and richer    pipeline/barrier states not readable via v1.
Lack of read parity and identifier mismatch forces support tickets and slows CDF 2.0 adoption.
Goal is to launch Read API 2.0 alongside CDF 2.0 go‑live to avoid migration blockers.
OKRs & Success Metrics
Objective: Enable supplier and internal adoption of CDF 2.0 with clear, self-serve product visibility.
 • KR1: Ship Read API 2.0 to production by XX.
 • KR2: ≥80% of active suppliers adopt v2 by.
 • KR3: Reduce catalog status/support tickets ≥XX% by.
 • KR4: Meet SLAs — XX% uptime; <XXms p95 single‑product; <XXs p95 option groups; freshness <XXs p95.
Dependencies & Project Involvement
Team
Contribution
Role
POC
Catalog API (Read)
Owns API design, build, rollout
Product / Eng Leads
TBD
CDF 2.0 Platform
GraphQL Federation, ID Mapper service
Dependency Owner
TBD
PA 2.0
Option grouping schema, validation, pipeline exposure
Partner Team
TBD
Barrier Platform
Barrier/validation reason surface & codes
Partner Team
TBD
GST / Merchandising
Status workflows, double‑classing resolution
Stakeholder
TBD
BD / DevRel / Tech Writing
Partner comms, docs & migration guides
Enabler
TBD

General Artifacts
Deliverable
Description and Purpose
PRD (this doc)
Defines scope, requirements, risks, and delivery plan
Draft GraphQL Schema
Field names/types for getProduct, getOptionGrouping, listProducts
Error Code Catalog
Stable codes, messages, remediation links
Migration Guide
v1→v2 identifier mapping & query examples
Query Cookbook
Persisted query IDs and best‑practice patterns
Release Comms Plan
Timeline and messaging to PIMs/suppliers

Problem & Solution Requirements
Problem Summary
Suppliers cannot read products using CDF 2.0 identifiers or retrieve option grouping, pipeline status, and barrier information through Read API 1.0. This mismatch between PA 2.0 writes and v1 reads causes confusion, extra integration effort, and support tickets, delaying CDF 2.0 adoption.
Solution Summary
Deliver a GraphQL Read API 2.0 with full PA 2.0 read parity, including option grouping, composites/kits, sanitized pipeline step visibility, and barrier details. Provide transparent migration through an ID Mapper that translates legacy identifiers to MPLVID, plus deterministic pagination, signed media URLs, and clear SLAs to ensure reliable partner integrations.
Risks
 • CDF 2.0 or ID Mapper delays could slip launch.
 • Mapping data quality issues could misroute reads.
 • Performance regressions under peak traffic could degrade SLAs.
 • Supplier migration resistance could require extended v1 support.
 • Data exposure mistakes (unsanitized internals) could create security/compliance risk.
Requirements In Scope
 NOTE: All examples and copy are draft and may change before development.

Phase
User Story
Functional Requirements
System Requirement
Sample Queries
Integration Setup Information
Single Product
As a PIM developer, I want to retrieve a product by MPLVID (optionally by market) with all CDF 2.0 fields so that I can render a complete, accurate view and help suppliers self-diagnose issues.
Retrieve full product object for a given mplvid (or legacy ID):• Identifiers: mplvid, mplid, supplierPartId, legacyIds { sku, optionId, ocid }. Note: selections use selectedChoices { choiceId } which map 1:1 to legacy PiID values; MPLID reuses legacy SKU value to ease migration.
• Market context: include marketContext in requests and entity keys; it is part of the federated keys for MarketplaceListing and MarketplaceListingVariant.
• Core Info: name, description, featureBullets, classId, className, marketContext, availableMarkets, lastUpdated. Customer-facing projections come from MPL/MPLV; supplier/internal reads should align to the Product Graph S2S model.
Status: supplier-facing statusSummary derived from findability and barrier state; finalize public status/enum with Barrier/Findability owners before schema lock.
Pipeline (sanitized): pipelineStatus { overallStatus, steps { code, name, status, startedAt, completedAt, message } } with supplier-facing step names only; finalize the public step catalog/mapping rules with Barrier/Findability.
Barriers/Validations: statusDetails { barrierReasons[], validationErrors[], doubleClassingInfo, missingRecommendedAttributes[] } with code (stable), fieldPath, severity, actionableSteps, remediationUrl, addedBy (sanitized). Use Barrier Platform's code catalog and links.
Option Grouping: variantGroupId, variantType, optionCategories[], variantAttributes[] (displayName, value, rank, thumbnailUrl). Source variantGroupId and ranks from PA/PMP grouping surfaces.
Components: for productType ∈ {COMPOSITE, KIT} return components[] { mplvid, quantity, relationship, redacted } (cross‑supplier details redacted). Until Product Graph S2S exposes native composition, federate from Merch Kit Service or legacy Product Cache relationships.
Media: imagery[]/videos[]/documents[] { url, moderationStatus, mediaUrlExpiresAt } (signed URLs; conditional GET/ETag recommended as API policy for efficiency).
Keys supported: lookup by mplvid + market (dependency on variantId+market key), and via legacy identifiers through the ID Mapper during transition; fallback resolution via internalSku + selections + market is supported by MPL keys.
Behavior:• If marketContext is not configured → return default market + warning including availableMarkets (API policy).• Nullability rules: invalid attributes return null + corresponding validation entry (API policy).• Identifier stability: mplvid is durable; grouping metadata reflects PA/PMP updates over time.
Performance: p95 <XXms (single);
Freshness: <XXs p95 for attributes/status/pipeline;

Availability: XX% mo.

Security: OAuth2; strict tenant isolation; cross-supplier component redaction.

Consistency: eventual for most fields; strong for identifiers/market config.

Errors: 403 unauthorized, 404 not found. For market misconfiguration, return data with a warning via GraphQL errors[].extensions and include availableMarkets.



A, B, F
OAuth2 Client Credentials; Authorization: Bearer.Use If-None-Match/ETag to poll efficiently. Respect rate limits (10 parts/sec st).Persisted query IDs recommended for common reads.
Variant Group (Variants)
As a PIM developer, I want to fetch all variants in a group by variantGroupId with option metadata so that I can display/manage variant families and verify grouping.
Retrieve group-level view::• Return mplid, marketContext, and grouping metadata that reflect PA/PMP option grouping.
• optionCategories[] { categoryName, displayName, rank, description, isCustomCategory, moderationStatus }.
• variants[] (lightweight): mplvid, name, variantType, optionValues[] { categoryName, value, displayName, rank }, leadImageUrl, link to getProduct.
• groupingMetadata { suggestedBySupplier, wayfairModified, lastModifiedAt }.
Pagination: cursor pagination with deterministic ordering and 24h cursor validity (API policy).


p95 <XXs up to 850 variants; deterministic ordering; cursors valid 24h; eventual consistency <XXs p95 on grouping updates.
C
Same auth; use cursor pagination; cache TTL 30s; show moderation status for custom categories.
Pipeline Status
As a PIM developer, I want sanitized pipeline step status with timestamps so that I can show where processing stands and set expectations.
Expose sanitized processing view:• pipelineStatus { overallStatus, steps { code, name, status, startedAt, completedAt, message } } using supplier-friendly step names.

• Partial unavailability: if pipeline source is down, return product data and pipelineStatus = null with a documented warning.

Polling guidance (policy): provide a lightweight status-only persisted query and support ETag/If-None-Match for efficient polling.


Freshness <XXs p95; status precedence documented (if brief mismatch, status wins for go-live).
A, D
Poll PROCESSING items every 1–5 min; use ETag to avoid re-downloading; provide a "status-only" persisted query for lightweight polling.
Barriers & Validations
As a supplier support analyst, I want barrier/validation codes with field paths and remediation links so that I can resolve issues without tickets.
Barrier and validation payloads:• statusDetails { code (stable), message, fieldPath, severity (ERROR/WARNING), actionableSteps[], remediationUrl, addedBy (sanitized) }.

Double-classing: isDoubleClassed, classIds[], primaryClassId, resolutionStatus, resolutionNotes.


Error contract via GraphQL errors[].extensions; no stack traces/PII; freshness <60s p95; links resolve to developer docs.
A, E
Render codes verbatim in partner UIs; track code frequencies; map codes → help-center pages in docs.
Bulk Filtering & Pagination
As a PIM developer, I want to list products with filters (market, class, status, type, lastUpdated) and cursor pagination so that I can reliably sync large catalogs.
List and sync:• Provide a GraphQL connection (edges/node/cursor, pageInfo) with cursor-based pagination and deterministic ordering; snapshot semantics per page are API policy.

Filters:• marketContext, classId, supplierPartId, productType, hasBarriers, lastUpdatedAfter (policy). Align any "status" filters to the finalized supplier-facing status/enum.
p95 <Xs; page size ≤XX; cursors expire after 24h; query complexity limits (depth ≤5, breadth ≤100 fields).
D, E, H
Use incremental sync by lastUpdatedAfter + cursor; exponential backoff on 429/5xx with jitter; prefer lightweight node shapes for bulk.
Composites / Kits
As a PIM developer, I want to read composite/kit components (MPLVIDs, quantities, relationships) with cross-supplier redaction so that I can validate complex structures safely.
Component structure:• components[] { mplvid, quantity, relationship (COMPONENT | KIT_CHILD), componentType, redacted}.
Edge behaviors:• Cross-supplier children → redacted = true (omit restricted details).• Deactivated or missing child → deterministic placeholder plus a validation entry.
Source of truth (current):• Until Product Graph S2S exposes native composition, federate from Merch Kit Service or legacy Product Cache relationships (e.g., componentSkus/kitChildren).
KIT_CHILD), componentType, redacted }.<br>**Edge behaviors:**<br>• Cross-supplier: return mplvid, relationship, quantity, redacted=true(omit restricted details).<br>• Deactivated child: component showsstatus=DEACTIVATED; parent may include barrier warning.<br>• Missing child: placeholder name "Unknown Component", status=null` + validation entry.• Circular references: prevented upstream; never returned.
p95 <XXms (single); strict authZ per component; consistency <XXs p95 for structure changes.
F
Legacy IDs (Migration)
As a supplier integrator, I want to query with legacy IDs (SKU+Option) and receive MPLVIDs so that I can migrate to v2 without refactoring upstream systems.
Legacy identifier support:• Accept legacy identifiers and translate via the ID Mapper (SKU, SKU+PiID, OCID ↔ MPL/MPLV) for products created before the cutoff; return both legacy and CDF 2.0 IDs in responses.
Guidance:• Prefer MPLVID/MPLID for new integrations; treat ID Mapper as transitional to accelerate CDF 2.0 adoption.
Errors:• Use standard HTTP/GraphQL error semantics; coordinate specific mapping failure categories/messages with the ID Mapper team instead of introducing custom codes.


Mapping adds ≤XXms p95; mapper availability XX%; audit trail of translations.
B
Prefer MPLVID long-term; monitor mapping error rates; backoff on 5xx; include requestId in support tickets.
Efficient Polling & Media
As a PIM developer, I want conditional GETs and signed media URLs with expiry so that I minimize bandwidth and avoid broken media.
Efficiency features:• Support ETag/If-None-Match → 304 on unchanged; Last-Modified optional.• Media objects include mediaUrl (signed), mediaUrlExpiresAt, moderationStatus.• Thumbnail guidance for variant chips; 403 from CDN after expiry is expected; fetch fresh via API when expired.• Rate-limit headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset; Retry-After on 429.
Signed URLs default ~XXm; cache TTL ~XXs; 304s shouldn't decrement partner rate budget where feasible; uphold XX% availability.
A
Always handle 403 on media by re-querying; avoid hotlinking outside partner tools; respect Retry-After and use jittered exponential backoff.


Requirements Out of Scope
• Pricing/costs (Pricing API).
 • Inventory/stock (Inventory API).
 • Webhooks/real‑time alerts (polling only for v2).
 • Bulk export async jobs (future).
 • Waymore rich content; performance analytics dashboards.
Analytics Plan
Action
Description
Purpose
Owner
getProduct query
Read single product
Measure adoption/latency
Catalog API
getOptionGrouping query
Read variant group
Monitor variant workloads
Catalog API
listProducts query
Bulk/filter reads
Capacity & usage patterns
Catalog API
Barrier code surfaces
Count per code & resolution time
Track self‑serve effectiveness
Barrier Platform
429 & retry metrics
Rate‑limit/backoff behavior
Prevent retry storms
SRE
ID mapping success rate
% successful translations
Data quality KPI
CDF/ID Mapper



Problem Discovery Artifacts
Deliverable
Description and Purpose
Supplier Interviews (notes)
Pain points with v1 reads and identifier mismatch
Ticket Analysis
Baseline volume for status/visibility issues
Tech Spike Findings
Latency tests for federation and ID Mapper

Delivery Milestones & GTM Release Plan
Project Milestones
Project Milestone(s)
Brief Description
Estimated LOE
PRD Approval (Gate 1)
Cross‑functional sign‑off; open critical decisions resolved
M
Schema Lock (Gate 2)
Finalize GraphQL schema & docs
M
Build Core Endpoints
Implement getProduct, getOptionGrouping, listProducts
L
Integrate Dependencies
CDF Federation, ID Mapper, Barrier, pipeline status
L
Performance & Security
Load tests, signed media, authZ redaction
M
Sandbox Ready (Gate 3)
Seed data; top 5 PIMs begin testing
M
Go/No‑Go (Gate 4)
SLA validation; P1/P2 bug review
S
Production Launch
Jul 15, 2026 target
S



Dependency Timelines
Dependent Team
Dependency
Timeline
CDF 2.0
Federation API stable


CDF 2.0
ID Mapper prod‑ready (SLA set)


PA 2.0
Option grouping parity complete


Barrier Platform
Reason codes & docs stable




Appendix
Glossary
 Definition for any terms or acronyms used in the document that may be unfamiliar
Term
Definition
MPLVID
MarketplaceListingVariantID — CDF 2.0 identifier for a specific product variant
MPLID
MarketplaceListingID — CDF 2.0 identifier for a product listing/group
ChoiceID
Identifier for an option choice within a variant group
PACM
Product Addition Composable Module — step in PA 2.0 pipeline
Barrier Platform
System applying go‑live barriers when validations/business rules fail
ID Mapper
Service translating legacy (SKU+Option+BrandCatalogID) ↔ CDF 2.0 IDs
Option Grouping
Organizing variants by options (e.g., Color, Size)
Composite
Product composed of multiple components sold as one
Kit
Bundle of standalone products sold together
Market Context
Market‑specific configuration (e.g., US, UK, CA, DE)


Change Log:
Running record of impactful changes in planning, strategy, solution, or delivery to reference later on as needed
Participants
Date
Decision / Change














Resources -
https://docs.google.com/document/d/1hReczerLm4HzmoqFZ8eXtJmaIZEM_bqwJMHqIohCBB4
https://docs.google.com/presentation/d/1dHCjCjK-T1Ehm9D9_vCa7w2shqYhjGC2dTxWn6zQbGY
https://docs.csnzoo.com/wayfair-shared/marketplace-listing-graphql/MPL_v.s_MPLV/index.html
https://docs.csnzoo.com/wayfair-shared/marketplace-listing-graphql/mpl_in_the_graph/index.html
https://docs.csnzoo.com/wayfair-shared/marketplace-listing-graphql/explore_MPL_related_entities_and_types/index.html
https://docs.csnzoo.com/wayfair-shared/marketplace-listing-graphql/faq/index.html
https://docs.csnzoo.com/wayfair-shared/graphql-documentation/subgraph/implement/sku-conversion-using-directive/index.html
https://docs.google.com/document/d/16UNspBU-MYg6DySLAM9DksZt9Hy1HA9BW-Y2E7Tth8w
https://infohub.corp.wayfair.com/display/SDIY/Variant+Groups+Management++feature+using+Cursor
https://projecthub.service.csnzoo.com/browse/CATSV-3202
https://docs.csnzoo.com/wayfair-shared/marketplace-listing-graphql/how_to_use_MPLV_represent_kits/index.html
https://infohub.corp.wayfair.com/display/MENG/Kit+Service+APIs
https://infohub.corp.wayfair.com/pages/viewpage.action?pageId=197417473
https://docs.google.com/document/d/15fOEDvKg75yT4suOZacGPzz8XEClYLE9SAt_2CDM-38
https://docs.google.com/document/d/11zpz_fBJsndoLvWCqY9d3uSGaqG8gdO2rQfoAfv99QQ
