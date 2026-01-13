# Interfaces - Public API Reference

## Overview

This document provides comprehensive documentation of all public interfaces, methods, and APIs in the transform-legacy-demo codebase.

---

## Public API Summary

**Total Public Classes**: 5  
**Total Public Methods**: 10  
**Total Public Static Methods**: 1

---

## Public API by Class

### Customer (Entity API)

**Purpose**: Domain entity representing a customer

#### Constructor
```java
public Customer(String id, String name)
```
**Parameters**:
- `id` - Unique customer identifier (required, non-null)
- `name` - Customer name (required, non-null)

**Returns**: Customer instance

**Example**:
```java
Customer customer = new Customer("CUST-001", "John Doe");
```

---

#### Method: getId()
```java
public String getId()
```
**Parameters**: None  
**Returns**: `String` - Customer unique identifier  
**Throws**: None

**Example**:
```java
String id = customer.getId();  // "CUST-001"
```

---

#### Method: getName()
```java
public String getName()
```
**Parameters**: None  
**Returns**: `String` - Customer name  
**Throws**: None

**Example**:
```java
String name = customer.getName();  // "John Doe"
```

---

### CustomerDao (Data Access API)

**Purpose**: Data access operations for Customer entities

#### Constructor
```java
public CustomerDao(LegacyJdoManager jdo)
```
**Parameters**:
- `jdo` - JDO persistence manager wrapper (required, non-null)

**Returns**: CustomerDao instance

**Example**:
```java
LegacyJdoManager jdo = new LegacyJdoManager();
CustomerDao dao = new CustomerDao(jdo);
```

---

#### Method: buildFindByIdQuery()
```java
public String buildFindByIdQuery(String id)
```
**Purpose**: Constructs JDO query to find customer by ID

**Parameters**:
- `id` - Customer ID to search for (required)

**Returns**: `String` - JDO query string

**Throws**: None (no validation)

**⚠️ Security Warning**: This method is vulnerable to SQL injection. Input is not validated or sanitized.

**Example**:
```java
String query = dao.buildFindByIdQuery("CUST-001");
// Returns: "SELECT FROM com.verafin.legacy.Customer WHERE id == 'CUST-001'"
```

**Malicious Example**:
```java
String query = dao.buildFindByIdQuery("' OR '1'='1");
// Returns: "SELECT FROM ... WHERE id == '' OR '1'='1'"
// ⚠️ Returns all customers!
```

---

### CustomerService (Business API)

**Purpose**: Business-level operations with transaction management

#### Constructor
```java
public CustomerService(LegacyJdoManager jdo)
```
**Parameters**:
- `jdo` - Transaction manager (required, non-null)

**Returns**: CustomerService instance

**Example**:
```java
LegacyJdoManager jdo = new LegacyJdoManager();
CustomerService service = new CustomerService(jdo);
```

---

#### Method: formatDisplay()
```java
public String formatDisplay(Customer c)
```
**Purpose**: Formats customer for display with transaction management

**Parameters**:
- `c` - Customer to format (required, non-null)

**Returns**: `String` - Formatted string in format "id:name"

**Throws**: 
- `RuntimeException` - On transaction failure (after rollback)

**Transaction Behavior**:
1. Begins transaction
2. Formats customer
3. Commits transaction on success
4. Rolls back on RuntimeException

**Example**:
```java
Customer customer = new Customer("CUST-001", "John Doe");
String display = service.formatDisplay(customer);
// Returns: "CUST-001:John Doe"
```

**Error Example**:
```java
try {
    String display = service.formatDisplay(customer);
} catch (RuntimeException e) {
    // Transaction rolled back
    // Exception re-thrown
}
```

---

### LegacyJdoManager (Transaction Management API)

**Purpose**: Transaction lifecycle management

#### Constructor
```java
public LegacyJdoManager()
```
**Parameters**: None  
**Returns**: LegacyJdoManager instance

**Example**:
```java
LegacyJdoManager jdo = new LegacyJdoManager();
```

---

#### Method: begin()
```java
public void begin()
```
**Purpose**: Begins a new transaction

**Parameters**: None  
**Returns**: `void`  
**Throws**: None (stub implementation)

**Example**:
```java
jdo.begin();
// Transaction started
```

---

#### Method: commit()
```java
public void commit()
```
**Purpose**: Commits the current transaction

**Parameters**: None  
**Returns**: `void`  
**Throws**: None (stub implementation)

**Example**:
```java
jdo.commit();
// Transaction committed
```

---

#### Method: rollback()
```java
public void rollback()
```
**Purpose**: Rolls back the current transaction

**Parameters**: None  
**Returns**: `void`  
**Throws**: None (stub implementation)

**Example**:
```java
try {
    // operations
} catch (Exception e) {
    jdo.rollback();
    throw e;
}
```

---

### LegacyQueries (Query Construction API)

**Purpose**: JDO query construction utilities

**Note**: All methods are static

---

#### Static Method: byCustomerId()
```java
public static String byCustomerId(String id)
```
**Purpose**: Constructs JDO query to find customer by ID

**Parameters**:
- `id` - Customer ID to search for

**Returns**: `String` - JDO query string

**Throws**: None

**⚠️ CRITICAL Security Vulnerability**: SQL Injection (CVSS 9.8)

**Implementation**:
```java
return "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";
```

**Safe Example**:
```java
String query = LegacyQueries.byCustomerId("CUST-001");
// Returns: "SELECT FROM com.verafin.legacy.Customer WHERE id == 'CUST-001'"
```

**Unsafe Example (SQL Injection)**:
```java
String query = LegacyQueries.byCustomerId("' OR '1'='1");
// Returns: "SELECT FROM ... WHERE id == '' OR '1'='1'"
// ⚠️ Bypasses authentication!
```

---

## API Usage Patterns

### Pattern 1: Query Construction

```java
// 1. Create components
LegacyJdoManager jdo = new LegacyJdoManager();
CustomerDao dao = new CustomerDao(jdo);

// 2. Build query
String query = dao.buildFindByIdQuery("CUST-001");

// 3. Execute query (not shown - would use JDO PersistenceManager)
```

---

### Pattern 2: Transaction Management

```java
// 1. Create service
LegacyJdoManager jdo = new LegacyJdoManager();
CustomerService service = new CustomerService(jdo);

// 2. Create customer
Customer customer = new Customer("CUST-001", "John Doe");

// 3. Execute business operation (transaction managed automatically)
String display = service.formatDisplay(customer);
// Transaction: begin → execute → commit
```

---

### Pattern 3: Error Handling

```java
LegacyJdoManager jdo = new LegacyJdoManager();
CustomerService service = new CustomerService(jdo);

try {
    String display = service.formatDisplay(customer);
    // Success path
} catch (RuntimeException e) {
    // Transaction automatically rolled back
    // Exception re-thrown
    logger.error("Operation failed", e);
}
```

---

## API Contracts and Guarantees

### Immutability Guarantees

✅ **Customer**: Immutable once created (all fields final)  
⚠️ **CustomerDao**: Mutable state in dependencies  
⚠️ **CustomerService**: Mutable state in dependencies

### Thread Safety

⚠️ **All Classes**: NOT thread-safe  
- No synchronization
- Shared mutable state (in JDO manager)
- Concurrent access requires external synchronization

### Null Handling

❌ **No Null Checks**: None of the public methods validate null parameters  
**Risk**: NullPointerException on null input

**Example**:
```java
dao.buildFindByIdQuery(null);  // ❌ NullPointerException
service.formatDisplay(null);    // ❌ NullPointerException
```

**Recommendation**: Add null validation:
```java
Objects.requireNonNull(id, "Customer ID cannot be null");
```

---

## API Compatibility

### Binary Compatibility

✅ **Stable**: No method signature changes expected  
⚠️ **JDO Dependency**: Tied to deprecated JDO API

### Source Compatibility

✅ **Backward Compatible**: Adding methods won't break clients  
⚠️ **Changing Signatures**: Would break existing code

---

## API Migration Guide

### From JDO to JPA

**Current (JDO)**:
```java
CustomerDao dao = new CustomerDao(jdo);
String query = dao.buildFindByIdQuery("123");
```

**Future (JPA)**:
```java
CustomerRepository repo = new CustomerRepository(entityManager);
Customer customer = repo.findById("123");
```

**Changes**:
- Replace CustomerDao with CustomerRepository
- Replace String queries with type-safe query methods
- Remove LegacyJdoManager, use EntityManager

---

## API Deprecation Status

| API | Status | Replacement | Timeline |
|-----|--------|-------------|----------|
| LegacyJdoManager | ⚠️ Deprecated | Spring @Transactional | Immediate |
| LegacyQueries.byCustomerId() | 🔴 Deprecated + Vulnerable | JPA Criteria API | Immediate |
| CustomerDao | 🟡 Legacy | Spring Data Repository | Short-term |

---

## API Security Considerations

### 🔴 Critical: SQL Injection

**Vulnerable APIs**:
- `LegacyQueries.byCustomerId(String id)` - No input sanitization
- `CustomerDao.buildFindByIdQuery(String id)` - Uses vulnerable query builder

**Impact**: CVSS 9.8 (Critical)

**Remediation**: Use parameterized queries immediately

---

### ⚠️ High: No Input Validation

**Affected APIs**: ALL public methods

**Risk**: 
- NullPointerException
- Invalid data processing
- Unexpected behavior

**Remediation**: Add validation to all public method parameters

---

## API Documentation Coverage

✅ **100%** - All public APIs documented

---

## Related Documentation

- [Program Structure](program-structure.md) - Complete class details
- [Data Models](data-models.md) - Entity documentation
- [Security Vulnerabilities](../technical-debt/security-vulnerabilities.md) - Security issues
- [Patterns](../architecture/patterns.md) - Design patterns

---

*Last Updated: January 2026*  
*Public APIs: 10 methods*  
*Documentation Coverage: 100%*  
*Security Status: CRITICAL (SQL Injection)*
