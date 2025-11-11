# Catalog Read API 2.0 - Stakeholder Demo Guide

## What is This Demo?

This is a **working prototype** of the Catalog Read API 2.0 that demonstrates how suppliers and internal systems will read product data in the new CDF 2.0 model. Think of it as a preview of what the real API will do.

**Key Point:** This validates that we can deliver all the requirements in the PRD before building the full production system.

---

## The Big Picture: What Problem Does This Solve?

### Current Problem (API 1.0)
- Suppliers can't read products using new CDF 2.0 identifiers (MPLVID/MPLID)
- Can't see option grouping (e.g., a chair in multiple colors)
- Can't see pipeline status or barriers blocking go-live
- Missing composite/kit product structure

### Our Solution (API 2.0 - This Demo)
✅ Read products with CDF 2.0 identifiers
✅ View variant groups (option families)
✅ See sanitized pipeline status
✅ Get actionable barrier information
✅ Support composites/kits
✅ Backward compatible with legacy IDs

---

## How to Use the Demo

### For Non-Technical Stakeholders

**URL:** https://catalog-read-api-demo.onrender.com/

1. **Overview Tab** - See statistics and features at a glance
2. **Quick Examples Tab** - Click pre-configured examples:
   - Click any card to see real data
   - JSON will appear below (explained in next section)
3. **Get Product Tab** - Enter an MPLVID to query specific products
4. **List Products Tab** - Filter products by market, barriers, type, etc.

### For Technical Stakeholders

Use the API directly:
```bash
curl "https://catalog-read-api-demo.onrender.com/v2/product?mplvid=MPLV-12345"
```

---

## Understanding the JSON Response

### Example: Office Chair (LIVE Product)

**Query:** Click "Office Chair (LIVE)" in Quick Examples

**You'll see JSON like this:**

```json
{
  "mplvid": "MPLV-12345",           ← New CDF 2.0 identifier
  "mplid": "MPL-100",                ← Product family ID
  "name": "Modern Office Chair - Black",
  "statusSummary": "LIVE",           ← Product is visible to customers
  "marketContext": "US",             ← Available in US market

  "legacyIds": {                     ← Backward compatibility
    "sku": "SKU-CHAIR-BLK-001",
    "optionId": "OPT-12345"
  },

  "pipelineStatus": {                ← Processing status
    "overallStatus": "COMPLETED",
    "steps": [
      {
        "name": "Content Validation",
        "status": "COMPLETED",       ← All validation passed
        "completedAt": "2025-11-08T10:05:00Z"
      },
      {
        "name": "Image Moderation",
        "status": "COMPLETED",       ← Images approved
        "completedAt": "2025-11-08T10:10:00Z"
      },
      {
        "name": "Publish",
        "status": "COMPLETED",       ← Live on site
        "completedAt": "2025-11-08T14:30:00Z"
      }
    ]
  },

  "statusDetails": {
    "barrierReasons": [],            ← No barriers blocking go-live
    "validationErrors": [],          ← No errors
    "missingRecommendedAttributes": []
  },

  "variantGroupId": "VG-1001",       ← Part of a variant family
  "variantAttributes": [             ← This variant is "Black"
    {
      "displayName": "Color",
      "value": "Black",
      "rank": 1
    }
  ]
}
```

### What to Validate: ✅ Checklist

**For a LIVE Product (like MPLV-12345):**
- [ ] `statusSummary` = "LIVE"
- [ ] `pipelineStatus.overallStatus` = "COMPLETED"
- [ ] `barrierReasons` = empty array `[]`
- [ ] All pipeline steps show `status: "COMPLETED"`
- [ ] Has both new IDs (`mplvid`) and legacy IDs (`legacyIds.sku`)

**This proves:** ✅ Product successfully went through validation and is live

---

### Example: Standing Desk (BLOCKED Product with Barriers)

**Query:** Click "Desk (BLOCKED)" in Quick Examples

**Key fields to examine:**

```json
{
  "statusSummary": "BLOCKED",        ← Product can't go live

  "pipelineStatus": {
    "overallStatus": "BLOCKED",
    "steps": [
      {
        "name": "Content Validation",
        "status": "FAILED",          ← Step failed
        "message": "Missing required attributes"
      }
    ]
  },

  "statusDetails": {
    "barrierReasons": [              ← WHY it's blocked
      {
        "code": "MISSING_REQUIRED_ATTRIBUTE",
        "message": "Required attribute 'weight_capacity' is missing",
        "fieldPath": "attributes.weight_capacity",
        "severity": "ERROR",
        "actionableSteps": [
          "Add weight capacity specification"
        ],
        "remediationUrl": "https://docs.example.com/barriers/missing-required-attribute"
      }
    ],
    "validationErrors": [
      {
        "code": "INVALID_DIMENSION",
        "message": "Height value exceeds maximum allowed",
        "fieldPath": "attributes.height",
        "severity": "ERROR"
      }
    ]
  }
}
```

### What to Validate: ✅ Checklist

**For a BLOCKED Product (like MPLV-54321):**
- [ ] `statusSummary` = "BLOCKED"
- [ ] `pipelineStatus.overallStatus` = "BLOCKED"
- [ ] `barrierReasons` array has items (not empty)
- [ ] Each barrier has:
  - [ ] Stable `code` (e.g., "MISSING_REQUIRED_ATTRIBUTE")
  - [ ] Clear `message` explaining the issue
  - [ ] `fieldPath` pointing to the problem field
  - [ ] `actionableSteps` telling supplier what to do
  - [ ] `remediationUrl` linking to documentation
- [ ] `validationErrors` array shows specific field errors

**This proves:** ✅ Suppliers can self-diagnose and fix issues without support tickets

---

### Example: Variant Group (Option Grouping)

**Query:** Click "Chair Variants (GROUP)" in Quick Examples

**Key fields to examine:**

```json
{
  "variantGroupId": "VG-1001",
  "mplid": "MPL-100",

  "optionCategories": [              ← Options that vary
    {
      "categoryName": "color",
      "displayName": "Color",
      "rank": 1,
      "description": "Chair color options"
    }
  ],

  "variants": [                      ← All variants in this group
    {
      "mplvid": "MPLV-12345",
      "name": "Modern Office Chair - Black",
      "statusSummary": "LIVE",
      "optionValues": [
        {
          "categoryName": "color",
          "value": "Black",
          "rank": 1
        }
      ]
    },
    {
      "mplvid": "MPLV-12346",
      "name": "Modern Office Chair - White",
      "statusSummary": "LIVE",
      "optionValues": [
        {
          "categoryName": "color",
          "value": "White",
          "rank": 2
        }
      ]
    },
    {
      "mplvid": "MPLV-12347",
      "name": "Modern Office Chair - Gray",
      "statusSummary": "PROCESSING"
    }
  ],

  "groupingMetadata": {
    "suggestedBySupplier": true,     ← Supplier created this grouping
    "wayfairModified": false,
    "lastModifiedAt": "2025-11-08T14:00:00Z"
  }
}
```

### What to Validate: ✅ Checklist

**For Variant Groups (like VG-1001):**
- [ ] `variantGroupId` identifies the group
- [ ] `optionCategories` lists what varies (Color, Size, etc.)
- [ ] `variants` array contains all variants in the family
- [ ] Each variant has:
  - [ ] Unique `mplvid`
  - [ ] Individual `statusSummary`
  - [ ] `optionValues` showing its variation
- [ ] `groupingMetadata` shows modification history

**This proves:** ✅ Suppliers can manage variant families and see all options together

---

### Example: Composite Product (Bundle)

**Query:** Click "Office Bundle (COMPOSITE)" in Quick Examples

**Key fields to examine:**

```json
{
  "mplvid": "MPLV-99999",
  "name": "Home Office Bundle",
  "productType": "COMPOSITE",        ← This is a bundle/kit

  "components": [                    ← What's included
    {
      "mplvid": "MPLV-54321",        ← Standing Desk
      "quantity": 1,
      "relationship": "COMPONENT",
      "componentType": "DESK",
      "redacted": false              ← Full info visible (same supplier)
    },
    {
      "mplvid": "MPLV-12345",        ← Office Chair
      "quantity": 1,
      "relationship": "COMPONENT",
      "componentType": "CHAIR",
      "redacted": false
    }
  ]
}
```

### What to Validate: ✅ Checklist

**For Composite Products (like MPLV-99999):**
- [ ] `productType` = "COMPOSITE" or "KIT"
- [ ] `components` array is not empty
- [ ] Each component has:
  - [ ] Valid `mplvid` (references another product)
  - [ ] `quantity` (how many)
  - [ ] `relationship` (COMPONENT or KIT_CHILD)
  - [ ] `redacted` flag (true if cross-supplier, false if same supplier)

**This proves:** ✅ Suppliers can see composite/kit structure with proper access control

---

## Key Validation Scenarios by PRD Requirement

### ✅ PRD Requirement: "Single Product Read"
**Test:** Get product MPLV-12345
**Validate:**
- Has all identifier types (mplvid, mplid, legacyIds)
- Has core info (name, description, class)
- Has status (statusSummary, pipelineStatus)
- Has media (imagery, videos with signed URLs)

### ✅ PRD Requirement: "Barriers & Validations"
**Test:** Get product MPLV-54321 or MPLV-88888
**Validate:**
- `barrierReasons` has stable codes
- Each barrier has fieldPath, severity, actionableSteps
- `remediationUrl` points to documentation
- `validationErrors` shows field-level issues

### ✅ PRD Requirement: "Option Grouping"
**Test:** Get variant group VG-1001
**Validate:**
- `optionCategories` defines what varies
- `variants` lists all options
- Each variant has `optionValues` with rank
- Shows modification history

### ✅ PRD Requirement: "Pipeline Status"
**Test:** Compare MPLV-12345 (COMPLETED) vs MPLV-12347 (PROCESSING)
**Validate:**
- Shows sanitized step names (not internal codes)
- Has timestamps (startedAt, completedAt)
- Shows step status (COMPLETED, PROCESSING, PENDING, FAILED)
- Includes helpful messages

### ✅ PRD Requirement: "Composites/Kits"
**Test:** Get product MPLV-99999
**Validate:**
- `productType` = "COMPOSITE"
- `components` array populated
- Each component has mplvid, quantity, relationship
- Cross-supplier redaction works (redacted flag)

### ✅ PRD Requirement: "Legacy ID Migration"
**Test:** Any product
**Validate:**
- Has both `mplvid` (new) and `legacyIds.sku` (old)
- Backward compatible for existing integrations

### ✅ PRD Requirement: "List & Filter"
**Test:** Use List Products tab with filters
**Validate:**
- Can filter by market (US, CA)
- Can filter by hasBarriers (true/false)
- Can filter by productType (SIMPLE, COMPOSITE, KIT)
- Can filter by lastUpdatedAfter timestamp
- Returns count and products array

---

## How to Present to Stakeholders

### 1. Start with the Problem
"Suppliers currently can't read products with CDF 2.0 identifiers or see barriers. This causes support tickets and slows adoption."

### 2. Show the Solution
"This demo proves we can deliver all PRD requirements. Let me show you..."

### 3. Walk Through Examples

**Example 1: Happy Path (LIVE Product)**
- "Here's a product that successfully went live"
- Point out: LIVE status, completed pipeline, no barriers
- "Supplier can see it's ready to sell"

**Example 2: Problem Product (BLOCKED)**
- "Here's a product blocked by barriers"
- Point out: Error codes, field paths, remediation links
- "Supplier can self-fix without calling support"

**Example 3: Variant Family**
- "Here's how option grouping works"
- Show: 3 color variants managed as a family
- "Supplier sees all options together"

**Example 4: Composite**
- "Here's a bundle with multiple components"
- Show: Component structure, quantities
- "Supplier can validate complex products"

### 4. Validation Points
"What to check in the JSON:"
- ✅ Status fields are clear (LIVE, BLOCKED, PROCESSING)
- ✅ Barriers have actionable error messages
- ✅ Pipeline shows progress with timestamps
- ✅ Grouping shows all variants together
- ✅ Both old and new identifiers present

### 5. Next Steps
"This validates the requirements. Next we'll build the production GraphQL API with federation, OAuth, and real-time data sources."

---

## FAQ: Common Questions

**Q: Why is the data in JSON format?**
A: This is how APIs return data. The production system will use GraphQL (similar structure). The dashboard makes it visual.

**Q: How do I know if the data is correct?**
A: Check the validation checklists above. Each example demonstrates a specific PRD requirement.

**Q: Can I add my own test data?**
A: Yes! Edit `data/products.json`, commit, and push. Render will auto-deploy.

**Q: Is this the final production API?**
A: No, this is a **requirements validation prototype**. Production will add GraphQL, OAuth, federation, and real data sources.

**Q: Why does the first request take 30 seconds?**
A: Free tier apps "sleep" after inactivity. This won't happen in production (paid tier).

**Q: What if I find a bug or missing feature?**
A: Great! That's the point of this demo - to find gaps before building production. File an issue or let the team know.

---

## Quick Reference: Available Test Data

### Products (use in "Get Product" tab)
- `MPLV-12345` - Office Chair Black (LIVE)
- `MPLV-12346` - Office Chair White (LIVE)
- `MPLV-12347` - Office Chair Gray (PROCESSING)
- `MPLV-54321` - Standing Desk (BLOCKED - has barriers)
- `MPLV-99999` - Office Bundle (COMPOSITE)
- `MPLV-77777` - Keyboard (LIVE, CA market)
- `MPLV-88888` - Monitor Stand (BLOCKED - double-classing issue)

### Variant Groups (use in "Variant Group" tab)
- `VG-1001` - Office Chair variants (3 colors)
- `VG-2001` - Standing Desk variants

### Filters (use in "List Products" tab)
- Market: US, CA
- Product Type: SIMPLE, COMPOSITE, KIT
- Has Barriers: true, false
- Last Updated After: 2025-11-01T00:00:00Z

---

## Success Metrics

After the demo, stakeholders should be able to answer:
- ✅ Can suppliers read products with CDF 2.0 identifiers? **YES**
- ✅ Can suppliers see why products are blocked? **YES**
- ✅ Can suppliers see variant grouping? **YES**
- ✅ Can suppliers see composite structure? **YES**
- ✅ Is the data actionable (clear errors, next steps)? **YES**
- ✅ Are we backward compatible with legacy IDs? **YES**

If all answers are YES, we've validated the PRD requirements! ✅

---

**Demo URL:** https://catalog-read-api-demo.onrender.com/
**PRD:** [docs/prds/2025-11-catalog-read-api-2.0.md](docs/prds/2025-11-catalog-read-api-2.0.md)
**GitHub:** https://github.com/Abhillashjadhav/claude-code-demo
