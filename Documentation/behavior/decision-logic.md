# Decision Logic - Behavioral Documentation

## Overview

This document captures the decision patterns, conditional logic, and branching rules implemented in the transform-legacy-demo codebase. Decision logic defines how the system chooses between alternative execution paths based on conditions and business rules.

---

## Decision Logic Summary

**Total Decision Points**: 3  
**Complexity**: Low  
**Primary Decision Type**: Error handling and transaction management  
**Business Rule Decisions**: Minimal

---

## Decision Point 1: Transaction Outcome Decision

### Decision Description

**Decision ID**: DL-001  
**Name**: Transaction Commit or Rollback Decision  
**Location**: `CustomerService.formatDisplay()`  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerService.java`

### Decision Context

**Trigger**: During customer display formatting within a transaction  
**Timing**: After executing business logic, before returning result

### Decision Logic

```
IF operation succeeds THEN
    commit transaction
    return result
ELSE IF RuntimeException occurs THEN
    rollback transaction
    re-throw exception
END IF
```

### Decision Tree

```
                    [Execute formatDisplay]
                            │
                            ▼
                    [BEGIN Transaction]
                            │
                            ▼
                   [Execute Business Logic]
                            │
                    ┌───────┴───────┐
                    │               │
              [Success]         [Exception]
                    │               │
                    ▼               ▼
            [COMMIT Trans]    [ROLLBACK Trans]
                    │               │
                    ▼               ▼
            [Return Result]   [Re-throw Exception]
                    │               │
                    └───────┬───────┘
                            ▼
                         [END]
```

### Decision Table

| Condition | Transaction Action | Return Action | Exception Propagation |
|-----------|-------------------|---------------|----------------------|
| Operation succeeds | COMMIT | Return formatted string | None |
| RuntimeException thrown | ROLLBACK | None | Re-throw exception |
| Error/Throwable thrown | ⚠️ NONE (Bug) | None | Propagate uncaught |

### Implementation

```java
public String formatDisplay(Customer c) {
    jdo.begin();
    try {
        // Business logic
        String out = c.getId() + ":" + c.getName();
        
        // DECISION POINT: Success path
        jdo.commit();
        return out;
        
    } catch (RuntimeException e) {
        // DECISION POINT: Error path
        jdo.rollback();
        throw e;
    }
    // Missing: finally block or handling for Error/Throwable
}
```

### Decision Criteria

**Success Criteria**: No exception thrown during business logic execution  
**Failure Criteria**: RuntimeException thrown during business logic execution

**⚠️ Gap**: Does not handle Error or Throwable, only RuntimeException

---

## Decision Point 2: Query Construction Strategy

### Decision Description

**Decision ID**: DL-002  
**Name**: Query Template Selection  
**Location**: `LegacyQueries.byCustomerId()`  
**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyQueries.java`

### Decision Context

**Trigger**: When building a customer lookup query  
**Timing**: At query construction time

### Decision Logic

```
GIVEN customer ID
WHEN building query
THEN use equality comparison template
RETURN "SELECT FROM {entity} WHERE id == '{value}'"
```

### Decision Tree

```
        [Need to find customer by ID]
                    │
                    ▼
         [Select Query Strategy]
                    │
                    └─→ [Use Equality Match Template]
                            │
                            ▼
                   [Build Query String]
                            │
                            ▼
                    [Return Query]
```

### Decision Criteria

**Fixed Decision**: Always uses equality comparison (==)  
**No Alternatives**: Does not support:
- Partial matching (LIKE)
- Case-insensitive search
- Multiple ID lookup
- Range queries

**🔴 Critical Issue**: No input validation or sanitization - SQL injection risk

---

## Decision Point 3: Error Propagation Strategy

### Decision Description

**Decision ID**: DL-003  
**Name**: Exception Handling and Propagation Decision  
**Location**: `CustomerService.formatDisplay()`  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerService.java`

### Decision Context

**Trigger**: When exception occurs during transaction  
**Timing**: In catch block after business logic failure

### Decision Logic

```
IF RuntimeException occurs THEN
    rollback transaction
    re-throw same exception (no wrapping)
END IF
```

### Decision Tree

```
              [Exception Caught]
                      │
                      ▼
         [Check Exception Type]
                      │
              ┌───────┴───────┐
              │               │
      [RuntimeException]  [Other (Error/Throwable)]
              │               │
              ▼               ▼
        [Rollback]      [⚠️ No handling]
              │               │
              ▼               ▼
        [Re-throw]      [Propagates uncaught]
              │               │
              └───────┬───────┘
                      ▼
              [Caller handles]
```

### Decision Table

| Exception Type | Catch | Rollback | Wrap Exception | Propagation |
|---------------|-------|----------|----------------|-------------|
| RuntimeException | ✅ Yes | ✅ Yes | ❌ No | Re-throw as-is |
| Checked Exception | ❌ No | ❌ No | ❌ N/A | N/A (none thrown) |
| Error | ❌ No | ❌ No | ❌ N/A | Uncaught propagation |
| Throwable | ❌ No | ❌ No | ❌ N/A | Uncaught propagation |

### Implementation

```java
catch (RuntimeException e) {
    // DECISION: Rollback and propagate
    jdo.rollback();
    throw e;  // No wrapping
}
```

**⚠️ Design Issue**: 
- No exception wrapping (loses context)
- Only catches RuntimeException
- No logging before re-throw

---

## Conditional Logic Patterns

### Pattern 1: Try-Catch Transaction Management

**Pattern**: Error-based branching for transaction control

```java
// Pattern structure
begin_transaction()
try {
    business_logic()
    commit_transaction()  // Success branch
} catch (RuntimeException) {
    rollback_transaction()  // Error branch
    throw
}
```

**Decision Points**: 
1. Success → Commit
2. Failure → Rollback

**Complexity**: Cyclomatic complexity = 2

---

### Pattern 2: Template-Based Query Construction

**Pattern**: Fixed template with parameter substitution

```java
// Pattern structure
template = "SELECT FROM {entity} WHERE {field} == '{value}'"
return fill_template(template, id)
```

**Decision Points**: None (deterministic, no branching)  
**Complexity**: Cyclomatic complexity = 1

---

## Business Rule Decisions

### BR-001: Customer Display Format Selection

**Decision**: How to format customer data for display

```
GIVEN Customer object
WHEN formatting for display
THEN use "id:name" format with colon separator
```

**Alternatives Not Implemented**:
- JSON format: `{"id": "...", "name": "..."}`
- XML format: `<customer id="..." name="..."/>`
- Custom format: Based on configuration
- Locale-specific format: Regional variations

**Current Decision**: Hard-coded colon-separated format

---

### BR-002: Query Comparison Operator Selection

**Decision**: How to match customer ID in queries

```
GIVEN customer ID
WHEN building query
THEN use exact equality comparison (==)
```

**Alternatives Not Implemented**:
- Pattern matching (LIKE)
- Case-insensitive (equalsIgnoreCase)
- Prefix matching (startsWith)
- Regular expression matching

**Current Decision**: Exact string equality only

---

## Decision Complexity Analysis

### Cyclomatic Complexity by Decision Point

| Decision Point | Location | Complexity | Branch Count |
|---------------|----------|------------|--------------|
| Transaction Outcome | CustomerService.formatDisplay() | 2 | 2 (success/error) |
| Query Construction | LegacyQueries.byCustomerId() | 1 | 0 (no branching) |
| Error Propagation | CustomerService catch block | 1 | 0 (always re-throw) |

**Overall Decision Complexity**: ✅ **VERY LOW** (Total CC: 4)

---

## Missing Decision Logic

### Validation Decisions (Not Implemented)

**Should Implement**:

```
IF customer is null THEN
    throw IllegalArgumentException
ELSE IF customer.id is null or empty THEN
    throw IllegalArgumentException
ELSE IF customer.name is null or empty THEN
    throw IllegalArgumentException
ELSE
    proceed with operation
END IF
```

### Input Sanitization Decisions (Critical - Not Implemented)

**Should Implement**:

```
IF id contains SQL special characters THEN
    sanitize or escape characters
    OR use parameterized query
ELSE
    use id directly
END IF
```

**🔴 Security Risk**: Missing input validation enables SQL injection

---

## Decision Flow Diagrams

### Complete Transaction Decision Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    formatDisplay(Customer c)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  BEGIN Trans  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Get ID & Name │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Concatenate   │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │               │
            ┌───────▼─────┐   ┌─────▼────────┐
            │   SUCCESS   │   │  EXCEPTION   │
            │  (no throw) │   │   (thrown)   │
            └───────┬─────┘   └─────┬────────┘
                    │               │
            ┌───────▼─────┐   ┌─────▼────────┐
            │   COMMIT    │   │  ROLLBACK    │
            └───────┬─────┘   └─────┬────────┘
                    │               │
            ┌───────▼─────┐   ┌─────▼────────┐
            │   RETURN    │   │  RE-THROW    │
            │   result    │   │  exception   │
            └───────┬─────┘   └─────┬────────┘
                    │               │
                    └───────┬───────┘
                            ▼
                        [ END ]
```

---

## Decision Logic Evolution Recommendations

### Phase 1: Add Input Validation Decisions

```java
public String formatDisplay(Customer c) {
    // NEW DECISION: Input validation
    if (c == null) {
        throw new IllegalArgumentException("Customer cannot be null");
    }
    if (c.getId() == null || c.getId().trim().isEmpty()) {
        throw new IllegalArgumentException("Customer ID is required");
    }
    if (c.getName() == null || c.getName().trim().isEmpty()) {
        throw new IllegalArgumentException("Customer name is required");
    }
    
    // Existing transaction logic
    jdo.begin();
    try {
        String out = c.getId() + ":" + c.getName();
        jdo.commit();
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();
        throw e;
    }
}
```

### Phase 2: Add Configurable Format Decisions

```java
public String formatDisplay(Customer c, DisplayFormat format) {
    jdo.begin();
    try {
        String out;
        
        // NEW DECISION: Format selection
        switch (format) {
            case COLON_SEPARATED:
                out = c.getId() + ":" + c.getName();
                break;
            case JSON:
                out = toJson(c);
                break;
            case XML:
                out = toXml(c);
                break;
            default:
                throw new IllegalArgumentException("Unknown format: " + format);
        }
        
        jdo.commit();
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();
        throw e;
    }
}
```

### Phase 3: Add Query Strategy Decisions

```java
public String buildFindQuery(String id, QueryStrategy strategy) {
    // NEW DECISION: Query strategy selection
    switch (strategy) {
        case EXACT_MATCH:
            return "SELECT FROM Customer WHERE id == :id";  // Parameterized
        case PREFIX_MATCH:
            return "SELECT FROM Customer WHERE id.startsWith(:id)";
        case CASE_INSENSITIVE:
            return "SELECT FROM Customer WHERE id.toLowerCase() == :id";
        default:
            throw new IllegalArgumentException("Unknown strategy: " + strategy);
    }
}
```

---

## Decision Logic Quality Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Validation Logic | 🔴 Missing | No input validation decisions |
| Error Handling | 🟡 Partial | Basic try-catch, but incomplete |
| Branching Clarity | ✅ Good | Clear success/failure paths |
| Decision Documentation | 🟡 Partial | No inline comments on decisions |
| Flexibility | 🔴 Low | Hard-coded decisions, no configuration |
| Security | 🔴 Critical | Missing sanitization decisions |

---

## Related Documentation

- [Business Logic](business-logic.md) - Business rules and calculations
- [Workflows](workflows.md) - Transaction lifecycles and processes
- [Error Handling](error-handling.md) - Exception patterns and recovery
- [Sequence Diagrams](../diagrams/behavioral/sequence-diagrams.md) - Visual interaction flows
- [Security Vulnerabilities](../technical-debt/security-vulnerabilities.md) - Security issues in decision logic

---

*Last Updated: January 2026*  
*Decision Points: 3*  
*Complexity: Very Low*  
*Validation Decisions: 0 (Missing)*
