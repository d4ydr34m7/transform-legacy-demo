# Transaction Flow - Data Flow Diagrams

## Overview

Text-based data flow diagrams showing transaction management and data movement in the transform-legacy-demo system.

---

## Transaction Flow Diagram

### Complete Transaction Lifecycle

```
┌────────────────────────────────────────────────────────────┐
│                  TRANSACTION FLOW                          │
└────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌────────────────────┐
│  1. BEGIN          │
│  jdo.begin()       │
└──────────┬─────────┘
           │
           ▼
┌────────────────────┐
│  2. ACTIVE         │
│  Transaction open  │
└──────────┬─────────┘
           │
           │ Execute Business Logic
           │
           ▼
┌────────────────────┐
│  3. BUSINESS LOGIC │
│  - Get customer ID │
│  - Get customer name│
│  - Format string   │
└──────────┬─────────┘
           │
           │ Success?
           ├─────────────┬────────────────┐
           │ YES         │ NO             │
           ▼             ▼                │
┌────────────────┐  ┌────────────────┐   │
│  4a. COMMIT    │  │  4b. CATCH     │   │
│  jdo.commit()  │  │  Exception     │   │
└────────┬───────┘  └────────┬───────┘   │
         │                   │            │
         │                   ▼            │
         │          ┌────────────────┐   │
         │          │  5. ROLLBACK   │   │
         │          │  jdo.rollback()│   │
         │          └────────┬───────┘   │
         │                   │            │
         ▼                   ▼            │
┌────────────────┐  ┌────────────────┐   │
│  COMMITTED     │  │  ROLLED BACK   │   │
└────────┬───────┘  └────────┬───────┘   │
         │                   │            │
         │                   │ throw e    │
         ▼                   ▼            │
      [Return]            [Exception] ────┘
         │                   │
         ▼                   ▼
       [END]               [END]
```

---

## Data Flow: formatDisplay Operation

### Input to Output Flow

```
INPUT: Customer Object
  │
  ├─ Field: id (String)
  │
  └─ Field: name (String)
      │
      ▼
TRANSACTION: BEGIN
      │
      ▼
EXTRACTION: Get Fields
      │
      ├─ customer.getId() → String id
      │
      └─ customer.getName() → String name
      │
      ▼
TRANSFORMATION: Format
      │
      └─ Concatenate: id + ":" + name
         │
         ▼
RESULT: formatted string
      │
      ▼
TRANSACTION: COMMIT
      │
      ▼
OUTPUT: String ("id:name")
```

---

## State Transition Diagram

### Transaction States

```
┌────────────┐
│   NONE     │ (Initial State)
└──────┬─────┘
       │
       │ begin()
       │
       ▼
┌────────────┐
│  ACTIVE    │ (Transaction in Progress)
└──────┬─────┘
       │
       ├──────────────┬─────────────┐
       │ commit()     │ rollback()  │
       │              │             │
       ▼              ▼             │
┌──────────┐   ┌─────────────┐     │
│COMMITTED │   │ ROLLED_BACK │     │
└──────────┘   └─────────────┘     │
       │              │             │
       └──────────────┴─────────────┘
                │
                ▼
             [END]
```

---

## Data Transformation Pipeline

### Step-by-Step Data Flow

```
Step 1: Input
─────────────
Customer object
  ├─ id: "CUST-001"
  └─ name: "John Doe"

Step 2: Extraction
──────────────────
Extract fields:
  id_value = "CUST-001"
  name_value = "John Doe"

Step 3: Transformation
──────────────────────
Concatenate with delimiter:
  result = id_value + ":" + name_value
  result = "CUST-001:John Doe"

Step 4: Output
──────────────
Return String:
  "CUST-001:John Doe"
```

---

## Transaction Boundary Flow

```
┌─────────────────────────────────────────────────┐
│          METHOD EXECUTION BOUNDARY              │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │     TRANSACTION BOUNDARY                  │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  BEGIN                              │ │ │
│  │  └───────────────┬─────────────────────┘ │ │
│  │                  │                        │ │
│  │  ┌───────────────▼─────────────────────┐ │ │
│  │  │  BUSINESS LOGIC                     │ │ │
│  │  │  (Inside Transaction)               │ │ │
│  │  └───────────────┬─────────────────────┘ │ │
│  │                  │                        │ │
│  │  ┌───────────────▼─────────────────────┐ │ │
│  │  │  COMMIT or ROLLBACK                 │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Error Flow

### Exception Propagation

```
Business Logic Error
         │
         │ RuntimeException
         ▼
    Catch Block
         │
         ├─→ Rollback Transaction
         │
         └─→ Re-throw Exception
                  │
                  ▼
            Caller Handles
```

---

## Data Flow Summary

### formatDisplay() Data Flow

| Step | Component | Input | Output | Transaction State |
|------|-----------|-------|--------|------------------|
| 1 | CustomerService | Customer | - | NONE |
| 2 | LegacyJdoManager | begin() | void | ACTIVE |
| 3 | Customer | getId() | String | ACTIVE |
| 4 | Customer | getName() | String | ACTIVE |
| 5 | CustomerService | concatenate | String | ACTIVE |
| 6 | LegacyJdoManager | commit() | void | COMMITTED |
| 7 | CustomerService | return | String | COMMITTED |

---

## Query Flow

### buildFindByIdQuery() Data Flow

```
INPUT: Customer ID (String)
  │
  ▼
CustomerDao.buildFindByIdQuery()
  │
  ├─→ Delegate to LegacyQueries.byCustomerId()
  │      │
  │      ├─→ Concatenate query template with ID
  │      │   "SELECT FROM ... WHERE id == '" + id + "'"
  │      │
  │      └─→ Return query string
  │
  └─→ Return query string
      │
      ▼
OUTPUT: Query String
```

**⚠️ Security Issue**: ID value directly embedded in query string (SQL injection)

---

## Control Flow vs Data Flow

### Control Flow (Execution Path)

```
CustomerService.formatDisplay()
  │
  ├─→ LegacyJdoManager.begin()
  ├─→ Customer.getId()
  ├─→ Customer.getName()
  ├─→ String concatenation
  ├─→ LegacyJdoManager.commit()
  └─→ return
```

### Data Flow (Information Movement)

```
Customer object
  │
  ├─→ id field → String id
  ├─→ name field → String name
  │
  └─→ Concatenation → String result
                        │
                        └─→ Return value
```

---

## Related Documentation

- [Workflows](../behavior/workflows.md) - Transaction workflows
- [Sequence Diagrams](../behavioral/sequence-diagrams.md) - Interaction sequences
- [Error Handling](../behavior/error-handling.md) - Error flows

---

*Last Updated: January 2026*  
*Diagram Format: Text-based ASCII*  
*Transaction Pattern: Manual (begin/commit/rollback)*
