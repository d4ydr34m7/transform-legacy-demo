# Business Logic - Behavioral Documentation

## Overview

This document extracts and documents the business logic and business rules implemented in the transform-legacy-demo codebase.

---

## Business Logic Summary

**Total Business Rules**: 2  
**Complexity**: Low (simple formatting and query construction)  
**Domain**: Customer management

---

## Business Rule 1: Customer Display Formatting

### Rule Description

**Rule ID**: BR-001  
**Name**: Customer Display Format  
**Location**: `CustomerService.formatDisplay()`  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerService.java`

**Business Rule**:
> A customer's display representation is formatted as: `{customerId}:{customerName}`

### Rule Implementation

```java
public String formatDisplay(Customer c) {
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

### Rule Specification

**Input**: Customer object  
**Output**: String in format "id:name"  
**Delimiter**: Colon (:)

**Examples**:
- Customer("1", "Shreya") → "1:Shreya"
- Customer("CUST-001", "John Doe") → "CUST-001:John Doe"
- Customer("123", "Test User") → "123:Test User"

### Business Rationale

**Purpose**: Provides a standardized string representation of customer data for display purposes

**Use Cases**:
- UI display
- Logging
- Reports
- Debug output

### Rule Constraints

**Constraints**:
- Input customer must not be null (no validation)
- Both ID and name must not be null (no validation)
- Separator is fixed (colon)

**⚠️ Issues**:
- No null handling
- No validation
- Fixed format (not configurable)
- Colon in name/ID would not be escaped

---

## Business Rule 2: Customer Query Construction

### Rule Description

**Rule ID**: BR-002  
**Name**: Customer Lookup by ID  
**Location**: `LegacyQueries.byCustomerId()`  
**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyQueries.java`

**Business Rule**:
> A customer can be queried by their unique identifier using an equality comparison

### Rule Implementation

```java
public static String byCustomerId(String id) {
    return "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";
}
```

### Rule Specification

**Input**: Customer ID (String)  
**Output**: JDO query string  
**Query Type**: SELECT with WHERE clause  
**Comparison**: Equality (==)

**Query Pattern**:
```
SELECT FROM {entity_class} WHERE {id_field} == '{id_value}'
```

### Business Rationale

**Purpose**: Enable retrieval of customer records by their unique identifier

**Use Cases**:
- Customer details lookup
- Customer verification
- Customer update operations
- Customer delete operations

### Rule Constraints

**Constraints**:
- ID must match exactly (case-sensitive)
- Only single customer lookup (not batch)
- Full entity returned (not projection)

**🔴 Critical Issue**: SQL injection vulnerability due to string concatenation

---

## Business Process Flows

### Process 1: Display Customer Information

```
START
  │
  ├─→ Receive Customer object
  │
  ├─→ BEGIN transaction
  │
  ├─→ Extract customer ID
  │
  ├─→ Extract customer name
  │
  ├─→ Format as "id:name"
  │
  ├─→ COMMIT transaction
  │
  └─→ Return formatted string
END
```

**Transactional**: Yes  
**Error Handling**: Rollback on exception  
**Duration**: < 1ms (no actual database operation in stub)

---

### Process 2: Query Customer by ID

```
START
  │
  ├─→ Receive customer ID
  │
  ├─→ Construct JDO query string
  │   └─→ Template: "SELECT FROM ... WHERE id == 'VALUE'"
  │
  ├─→ Return query string
  │
END
```

**Transactional**: No  
**Error Handling**: None  
**Duration**: < 1ms

---

## Business Calculations

### Calculation 1: Display String

**Formula**: `displayString = customerId + ":" + customerName`

**Components**:
- customerId: String identifier
- ":" : Fixed delimiter
- customerName: String name

**Result Type**: String  
**Example**: "CUST-001:John Doe"

---

## Business Validations

### Current State: ❌ No Business Validations

**Missing Validations**:
1. Customer ID validation (format, length, characters)
2. Customer name validation (non-empty, length, characters)
3. Duplicate customer prevention
4. Referential integrity checks

**Recommended Validations**:

```java
public String formatDisplay(Customer c) {
    // Validation
    Objects.requireNonNull(c, "Customer cannot be null");
    Objects.requireNonNull(c.getId(), "Customer ID cannot be null");
    Objects.requireNonNull(c.getName(), "Customer name cannot be null");
    
    if (c.getId().trim().isEmpty()) {
        throw new IllegalArgumentException("Customer ID cannot be empty");
    }
    
    if (c.getName().trim().isEmpty()) {
        throw new IllegalArgumentException("Customer name cannot be empty");
    }
    
    // Business logic
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

---

## Business Rules in Domain Model

### Customer Entity Rules

**Implicit Rules**:
1. Customer must have an ID (primary key)
2. Customer must have a name
3. ID uniquely identifies a customer
4. Customer is immutable once created

**⚠️ Not Enforced**:
- No validation in constructor
- No uniqueness constraint enforcement in code
- No format validation

---

## Business Logic Complexity

### Complexity Assessment

| Business Rule | Complexity | Cyclomatic Complexity |
|--------------|------------|----------------------|
| Display Formatting | ✅ Very Low | 2 |
| Query Construction | ✅ Very Low | 1 |

**Overall Business Logic Complexity**: ✅ **VERY LOW**

---

## Business Rules Documentation Quality

| Aspect | Rating | Notes |
|--------|--------|-------|
| Documentation | 🟡 Partial | No inline comments explaining business rules |
| Validation | 🔴 None | No business rule validation |
| Testing | ✅ Good | Unit tests cover business logic |
| Clarity | ✅ Good | Code is simple and understandable |

---

## Domain Knowledge

### Domain Concepts

**Domain**: Customer Management  
**Entities**: Customer  
**Operations**: Display, Query

**Domain Terminology**:
- **Customer**: Person or organization that uses the service
- **Customer ID**: Unique identifier for a customer
- **Customer Name**: Human-readable name of the customer
- **Display Format**: Standardized string representation

### Domain Rules (Inferred)

1. **Identity Rule**: Each customer has a unique identifier
2. **Naming Rule**: Each customer has a name
3. **Display Rule**: Customers are displayed in "id:name" format
4. **Lookup Rule**: Customers can be found by their ID

---

## Business Logic Evolution

### Current State

**Simplicity**: Very simple CRUD operations  
**Maturity**: Basic implementation  
**Completeness**: Minimal feature set

### Potential Evolution

**Phase 1**: Add validation
```java
- Validate customer ID format
- Validate customer name (non-empty, length)
- Add uniqueness checks
```

**Phase 2**: Add business logic
```java
- Customer status (active/inactive)
- Customer type categorization
- Customer creation date tracking
- Last modified tracking
```

**Phase 3**: Add complex rules
```java
- Customer credit limits
- Customer tier levels (gold, silver, bronze)
- Customer relationships (organizations, contacts)
- Business rule engine
```

---

## Related Documentation

- [Workflows](workflows.md) - Transaction lifecycles
- [Error Handling](error-handling.md) - Exception strategies
- [Sequence Diagrams](../diagrams/behavioral/sequence-diagrams.md) - Interaction flows
- [Program Structure](../reference/program-structure.md) - Code details

---

*Last Updated: January 2026*  
*Business Rules: 2*  
*Complexity: Very Low*  
*Validation: None*
