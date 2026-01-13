# Error Handling - Behavioral Documentation

## Overview

This document describes error handling strategies and exception management in the transform-legacy-demo codebase.

---

## Error Handling Strategy

**Overall Approach**: Try-Catch-Rollback with Exception Propagation  
**Error Recovery**: Rollback transaction and re-throw  
**Error Logging**: ❌ None implemented

---

## Error Handling Pattern: Transaction Rollback

### Implementation Location

**Class**: `CustomerService`  
**Method**: `formatDisplay(Customer c)`  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerService.java`

### Pattern Structure

```java
public String formatDisplay(Customer c) {
    jdo.begin();
    try {
        // Business logic that may throw exceptions
        String out = c.getId() + ":" + c.getName();
        jdo.commit();
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();  // Cleanup on error
        throw e;          // Propagate to caller
    }
}
```

### Error Handling Flow

```
[Business Logic Executes]
         │
         │ Success?
         ├─ YES → Commit Transaction → Return Result
         │
         └─ NO  → Exception Thrown
                      │
                      ├─→ Catch RuntimeException
                      ├─→ Rollback Transaction
                      └─→ Re-throw Exception to Caller
```

---

## Exception Categories

### Caught Exceptions

**Exception Type**: `RuntimeException`  
**Handling**: Rollback and re-throw  
**Examples**:
- NullPointerException (if customer is null)
- IllegalStateException (from JDO)
- Any unchecked exception

### Uncaught Exceptions

**⚠️ Problem**: `Error` and checked exceptions not handled

**Example Scenario**:
```java
// If OutOfMemoryError occurs:
jdo.begin();
// OutOfMemoryError thrown here
// Transaction NOT rolled back!
// Resource leak!
```

**Recommendation**: Catch `Throwable` instead:
```java
} catch (Throwable t) {
    jdo.rollback();
    throw t;
}
```

---

## Error Scenarios

### Scenario 1: Null Customer

**Trigger**: `formatDisplay(null)`

**Exception Flow**:
```
1. jdo.begin() → Success
2. c.getId() → NullPointerException thrown
3. catch (RuntimeException e) → Caught
4. jdo.rollback() → Executed
5. throw e → NullPointerException propagated
```

**Result**: Transaction rolled back, exception thrown to caller

---

### Scenario 2: Null Customer ID

**Trigger**: `formatDisplay(new Customer(null, "Name"))`

**Exception Flow**:
```
1. jdo.begin() → Success
2. c.getId() → Returns null
3. null + ":" → NullPointerException thrown
4. catch (RuntimeException e) → Caught
5. jdo.rollback() → Executed
6. throw e → NullPointerException propagated
```

**Result**: Transaction rolled back, exception thrown

---

### Scenario 3: Commit Failure

**Trigger**: JDO commit fails (database error)

**Exception Flow**:
```
1. jdo.begin() → Success
2. Business logic → Success
3. jdo.commit() → Throws RuntimeException
4. catch (RuntimeException e) → Caught
5. jdo.rollback() → Executed (may be no-op if already failed)
6. throw e → Exception propagated
```

**Result**: Transaction rolled back (if possible), exception thrown

---

## Error Recovery

### Current Recovery Strategy

**Approach**: ❌ No Recovery  
**Action**: Rollback and propagate exception  
**Retry**: None  
**Fallback**: None

### Recommended Recovery Strategy

```java
public String formatDisplay(Customer c) {
    int retries = 3;
    while (retries > 0) {
        jdo.begin();
        try {
            String out = c.getId() + ":" + c.getName();
            jdo.commit();
            return out;
        } catch (TransientException e) {
            jdo.rollback();
            retries--;
            if (retries == 0) throw e;
            // Wait and retry
        } catch (RuntimeException e) {
            jdo.rollback();
            throw e;  // Don't retry non-transient errors
        }
    }
}
```

---

## Error Logging

### Current State: ❌ No Logging

**Missing**:
- No exception logging
- No transaction failure logging
- No rollback logging
- No audit trail

### Recommended Logging

```java
private static final Logger logger = LoggerFactory.getLogger(CustomerService.class);

public String formatDisplay(Customer c) {
    logger.debug("Formatting display for customer: {}", c);
    jdo.begin();
    try {
        String out = c.getId() + ":" + c.getName();
        jdo.commit();
        logger.debug("Successfully formatted: {}", out);
        return out;
    } catch (RuntimeException e) {
        logger.error("Error formatting customer display", e);
        jdo.rollback();
        logger.debug("Transaction rolled back");
        throw e;
    }
}
```

---

## Exception Hierarchy (Not Implemented)

### Recommended Custom Exceptions

```java
// Base exception
public class CustomerException extends RuntimeException {
    public CustomerException(String message) {
        super(message);
    }
}

// Specific exceptions
public class CustomerNotFoundException extends CustomerException {
    public CustomerNotFoundException(String id) {
        super("Customer not found: " + id);
    }
}

public class CustomerValidationException extends CustomerException {
    public CustomerValidationException(String message) {
        super(message);
    }
}

public class TransactionException extends CustomerException {
    public TransactionException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## Error Messages

### Current State: ❌ No Custom Error Messages

**Problem**: Generic JVM exception messages

**Example**:
```java
java.lang.NullPointerException
    at CustomerService.formatDisplay(CustomerService.java:15)
```

**Not Helpful**: Doesn't explain business context

### Recommended Error Messages

```java
public String formatDisplay(Customer c) {
    Objects.requireNonNull(c, "Customer cannot be null");
    Objects.requireNonNull(c.getId(), "Customer ID cannot be null");
    Objects.requireNonNull(c.getName(), "Customer name cannot be null");
    
    jdo.begin();
    try {
        String out = c.getId() + ":" + c.getName();
        jdo.commit();
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();
        throw new TransactionException(
            "Failed to format customer display for ID: " + c.getId(), e);
    }
}
```

---

## Error Handling in DAO Layer

### Current State: ❌ No Error Handling

**CustomerDao.buildFindByIdQuery()**:
```java
public String buildFindByIdQuery(String id) {
    return LegacyQueries.byCustomerId(id);  // No error handling
}
```

**Problems**:
- No null check
- No validation
- Propagates SQL injection vulnerability

### Recommended Error Handling

```java
public String buildFindByIdQuery(String id) {
    Objects.requireNonNull(id, "Customer ID cannot be null");
    
    if (id.trim().isEmpty()) {
        throw new CustomerValidationException("Customer ID cannot be empty");
    }
    
    if (!id.matches("^[a-zA-Z0-9-]{1,50}$")) {
        throw new CustomerValidationException(
            "Invalid customer ID format: " + id);
    }
    
    try {
        return LegacyQueries.byCustomerId(id);
    } catch (Exception e) {
        throw new CustomerException("Failed to build query for ID: " + id, e);
    }
}
```

---

## Error Handling Quality Assessment

| Aspect | Current | Rating | Recommended |
|--------|---------|--------|-------------|
| Exception Catching | RuntimeException only | 🔴 Poor | Catch Throwable |
| Transaction Rollback | ✅ Implemented | ✅ Good | Add logging |
| Error Logging | ❌ None | 🔴 Poor | Add comprehensive logging |
| Error Messages | ❌ Generic | 🔴 Poor | Add contextual messages |
| Custom Exceptions | ❌ None | 🔴 Poor | Implement hierarchy |
| Input Validation | ❌ None | 🔴 Poor | Add validation |
| Recovery Strategy | ❌ None | 🔴 Poor | Add retry logic |

**Overall**: 🔴 **POOR** - Basic rollback implemented but missing critical error handling

---

## Error Handling Best Practices

### Practice 1: Fail Fast

**Current**: ⚠️ Partial (fails on null but no validation)

**Recommendation**: Validate inputs immediately:
```java
public String formatDisplay(Customer c) {
    // Fail fast with validation
    validate(c);
    
    // Then proceed with business logic
    jdo.begin();
    // ...
}
```

---

### Practice 2: Provide Context

**Current**: ❌ No context in exceptions

**Recommendation**: Add business context:
```java
throw new TransactionException(
    "Failed to format display for customer ID: " + c.getId() + 
    ", operation: formatDisplay", e);
```

---

### Practice 3: Log All Errors

**Current**: ❌ No logging

**Recommendation**: Log at appropriate levels:
```java
logger.error("Transaction failed for customer {}", c.getId(), e);
```

---

## Related Documentation

- [Business Logic](business-logic.md) - Business rules that may fail
- [Workflows](workflows.md) - Transaction lifecycles
- [Security Vulnerabilities](../technical-debt/security-vulnerabilities.md) - Error-related security issues

---

*Last Updated: January 2026*  
*Error Handling: Basic rollback only*  
*Quality: Poor (needs significant improvement)*
