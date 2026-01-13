# Workflows - Behavioral Documentation

## Overview

This document describes the workflows and transaction lifecycles in the transform-legacy-demo system.

---

## Workflow 1: Customer Display Transaction

### Workflow Description

**Name**: Format Customer Display with Transaction Management  
**Entry Point**: `CustomerService.formatDisplay(Customer c)`  
**Pattern**: Transaction Script

### Workflow Steps

```
1. BEGIN TRANSACTION
   └─→ jdo.begin()

2. EXTRACT DATA
   ├─→ Get customer ID: c.getId()
   └─→ Get customer name: c.getName()

3. FORMAT DATA
   └─→ Concatenate: id + ":" + name

4. COMMIT TRANSACTION
   └─→ jdo.commit()

5. RETURN RESULT
   └─→ return formatted string

ON ERROR:
   ├─→ ROLLBACK TRANSACTION: jdo.rollback()
   └─→ RE-THROW EXCEPTION
```

### Workflow Diagram

```
[START] → [BEGIN TX] → [Get ID] → [Get Name] → [Format] → [COMMIT TX] → [Return] → [END]
                │                                             │
                │                                             │
                └──────→ [Error] → [ROLLBACK TX] → [Throw] → [END]
```

### Transaction Lifecycle

```
State: NONE
   │
   │ jdo.begin()
   ▼
State: ACTIVE
   │
   ├─ Success Path
   │  │ jdo.commit()
   │  ▼
   │  State: COMMITTED → [Transaction Complete]
   │
   └─ Error Path
      │ jdo.rollback()
      ▼
      State: ROLLED_BACK → [Exception Thrown]
```

### Timing

- **Average Duration**: < 1ms (stub implementation)
- **Transaction Timeout**: None (no timeout configured)
- **Retry Policy**: None

---

## Workflow 2: Query Construction

### Workflow Description

**Name**: Build Customer Query by ID  
**Entry Point**: `CustomerDao.buildFindByIdQuery(String id)`

### Workflow Steps

```
1. RECEIVE INPUT
   └─→ Customer ID (String)

2. DELEGATE TO UTILITY
   └─→ LegacyQueries.byCustomerId(id)

3. CONSTRUCT QUERY
   └─→ Build query string with template

4. RETURN QUERY
   └─→ Return query string
```

### Workflow Diagram

```
[START] → [CustomerDao] → [LegacyQueries] → [Build Query] → [Return] → [END]
```

**Note**: No transaction, no error handling, no validation

---

## Transaction Patterns

### Pattern 1: Manual Transaction Management

**Implementation**: `CustomerService.formatDisplay()`

```java
public String formatDisplay(Customer c) {
    jdo.begin();                    // 1. START
    try {
        String out = c.getId() + ":" + c.getName();  // 2. WORK
        jdo.commit();               // 3. COMMIT
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();             // 4. ROLLBACK
        throw e;                     // 5. PROPAGATE
    }
}
```

**Characteristics**:
- ✅ Explicit transaction boundaries
- ✅ Try-catch-rollback pattern
- ⚠️ Verbose (boilerplate code)
- ⚠️ Error-prone (easy to forget rollback)
- 🔴 Only catches RuntimeException (not Error or Throwable)

---

### Pattern 2: No Transaction

**Implementation**: `CustomerDao.buildFindByIdQuery()`

```java
public String buildFindByIdQuery(String id) {
    return LegacyQueries.byCustomerId(id);
}
```

**Characteristics**:
- ✅ Simple, stateless
- ✅ No transaction overhead
- ✅ Read-only operation

---

## Data Flow Patterns

### Pattern 1: Service → Entity

```
CustomerService
    │
    │ 1. Receives Customer object
    │
    ├─→ 2. Calls c.getId()
    │        └─→ Returns String
    │
    ├─→ 3. Calls c.getName()
    │        └─→ Returns String
    │
    └─→ 4. Processes data (concatenation)
```

### Pattern 2: DAO → Query Utility

```
CustomerDao
    │
    │ 1. Receives String id
    │
    └─→ 2. Delegates to LegacyQueries.byCustomerId(id)
             │
             └─→ 3. Returns query string
```

---

## State Management

### Transaction State Machine

```
┌──────────┐
│  NONE    │ (Initial state)
└────┬─────┘
     │ begin()
     ▼
┌──────────┐
│  ACTIVE  │ (Transaction in progress)
└────┬─────┘
     │
     ├─ commit() ──→ COMMITTED (Success)
     │
     └─ rollback() → ROLLED_BACK (Failure)
```

### Entity State (not implemented, JDO concept)

```
TRANSIENT → (persist) → PERSISTENT → (commit) → DETACHED
```

---

## Concurrency Patterns

**Current**: ❌ No concurrency control

**Issues**:
- No synchronization
- No locking
- Not thread-safe
- Race conditions possible

**Recommendation**: Add concurrency control for production use

---

## Related Documentation

- [Business Logic](business-logic.md) - Business rules
- [Error Handling](error-handling.md) - Exception strategies
- [Transaction Flow](../diagrams/data-flow/transaction-flow.md) - Visual flows

---

*Last Updated: January 2026*  
*Workflows: 2*  
*Transaction Pattern: Manual*  
*Concurrency: None*
