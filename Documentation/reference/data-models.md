# Data Models - Entity Documentation

## Overview

This document provides comprehensive documentation of all data models and entities in the transform-legacy-demo codebase.

---

## Entity Inventory

**Total Entities**: 1  
**Entity Type**: JDO-annotated domain model

---

## Entity: Customer

### Entity Overview

**Class Name**: `Customer`  
**Package**: `com.verafin.legacy`  
**File**: `legacy-app/src/main/java/com/verafin/legacy/Customer.java`  
**Purpose**: Represents a customer in the system  
**Persistence**: JDO (Java Data Objects)  
**Immutable**: ✅ Yes

### Entity Annotations

```java
@PersistenceCapable
public class Customer {
    @PrimaryKey
    private final String id;
    private final String name;
}
```

**JDO Annotations**:
- `@PersistenceCapable` - Marks class as persistable entity
- `@PrimaryKey` - Marks id field as primary key

**⚠️ Technical Debt**: JDO annotations are deprecated (should migrate to JPA @Entity)

---

### Entity Schema

#### Table Information

**Logical Table Name**: `Customer` (inferred from class name)  
**Primary Key**: `id` (String)

#### Field Mapping

| Field | Java Type | Database Type | Nullable | Key | Default |
|-------|-----------|---------------|----------|-----|---------|
| id | String | VARCHAR | ❌ No | Primary | None |
| name | String | VARCHAR | ⚠️ Likely No | - | None |

**Note**: Exact database schema depends on JDO implementation and configuration

---

### Entity Fields

#### Field 1: id

**Name**: `id`  
**Type**: `String`  
**Visibility**: `private`  
**Modifiers**: `final` (immutable)  
**Annotations**: `@PrimaryKey`

**Purpose**: Unique identifier for the customer

**Characteristics**:
- Primary key
- Immutable (cannot be changed after creation)
- No validation (accepts any string)

**Constraints**:
- ⚠️ No length constraint
- ⚠️ No format validation
- ⚠️ No null check

**Recommended Constraints**:
```java
@Id
@NotNull
@Size(min = 1, max = 50)
@Pattern(regexp = "^[a-zA-Z0-9-]+$")
private final String id;
```

---

#### Field 2: name

**Name**: `name`  
**Type**: `String`  
**Visibility**: `private`  
**Modifiers**: `final` (immutable)  
**Annotations**: None

**Purpose**: Customer's name

**Characteristics**:
- Immutable
- No validation
- Nullable (no constraint)

**Constraints**:
- ⚠️ No length constraint
- ⚠️ No null check
- ⚠️ No format validation

**Recommended Constraints**:
```java
@Column(nullable = false, length = 100)
@NotNull
@NotEmpty
@Size(max = 100)
private final String name;
```

---

### Entity Constructor

```java
public Customer(String id, String name)
```

**Parameters**:
- `id` - Customer unique identifier (required, but not validated)
- `name` - Customer name (required, but not validated)

**Validation**: ❌ None

**Example**:
```java
Customer customer = new Customer("CUST-001", "John Doe");
```

**Problem Example** (no validation prevents these):
```java
// No validation - all accepted:
new Customer(null, "John");          // id is null
new Customer("", "John");            // id is empty
new Customer("CUST-001", null);      // name is null
new Customer("CUST-001", "");        // name is empty
```

---

### Entity Methods

#### Method: getId()

```java
public String getId()
```

**Purpose**: Returns customer's unique identifier

**Returns**: `String` - Customer ID  
**Throws**: None

---

#### Method: getName()

```java
public String getName()
```

**Purpose**: Returns customer's name

**Returns**: `String` - Customer name  
**Throws**: None

---

### Entity Characteristics

#### Immutability

✅ **Fully Immutable**:
- All fields are `final`
- No setters
- Constructor is only way to set values
- Thread-safe

**Benefits**:
- Safe to share across threads
- Prevents accidental modification
- Simpler to reason about

---

#### Identity

**Identity Field**: `id` (String)  
**Identity Type**: Natural key (business key)

**⚠️ Missing**: `equals()` and `hashCode()` methods

**Recommendation**: Add identity methods:
```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Customer)) return false;
    Customer customer = (Customer) o;
    return Objects.equals(id, customer.id);
}

@Override
public int hashCode() {
    return Objects.hash(id);
}
```

---

#### String Representation

**⚠️ Missing**: `toString()` method

**Current behavior**: Uses default `Object.toString()`
```java
Customer@1a2b3c4d  // Not helpful
```

**Recommendation**: Add toString():
```java
@Override
public String toString() {
    return "Customer{id='" + id + "', name='" + name + "'}";
}
```

---

### Entity Relationships

**Current**: None  
**Potential Future Relationships**:
- `@OneToMany` - Customer has many Orders
- `@ManyToOne` - Customer belongs to Organization
- `@ManyToMany` - Customer has many Roles

---

### Entity Lifecycle

```
┌─────────────┐
│   TRANSIENT │  (new Customer("id", "name"))
└──────┬──────┘
       │ persist()
       ▼
┌─────────────┐
│  PERSISTENT │  (managed by JDO)
└──────┬──────┘
       │ commit()
       ▼
┌─────────────┐
│  DETACHED   │  (after transaction close)
└─────────────┘
```

**Note**: Exact lifecycle depends on JDO PersistenceManager operations

---

### JDO vs JPA Annotation Comparison

#### Current (JDO)
```java
@PersistenceCapable
public class Customer {
    @PrimaryKey
    private final String id;
    private final String name;
}
```

#### Future (JPA)
```java
@Entity
@Table(name = "customer")
public class Customer {
    @Id
    private final String id;
    
    @Column(nullable = false, length = 100)
    private final String name;
}
```

**Changes Required**:
1. Replace `@PersistenceCapable` with `@Entity`
2. Replace `@PrimaryKey` with `@Id`
3. Add `@Table` annotation (optional)
4. Add `@Column` annotations for constraints

---

### Entity Validation Requirements

#### Current State: ❌ No Validation

#### Recommended Validation (Bean Validation / JSR 380)

```java
@Entity
public class Customer {
    @Id
    @NotNull(message = "Customer ID cannot be null")
    @Size(min = 1, max = 50, message = "Customer ID must be 1-50 characters")
    @Pattern(regexp = "^[a-zA-Z0-9-]+$", 
             message = "Customer ID must be alphanumeric")
    private final String id;
    
    @Column(nullable = false, length = 100)
    @NotNull(message = "Customer name cannot be null")
    @NotEmpty(message = "Customer name cannot be empty")
    @Size(max = 100, message = "Customer name must not exceed 100 characters")
    private final String name;
}
```

---

### Entity Usage Examples

#### Creating a Customer

```java
Customer customer = new Customer("CUST-001", "John Doe");
```

#### Persisting a Customer (JDO)

```java
PersistenceManager pm = pmf.getPersistenceManager();
Transaction tx = pm.currentTransaction();
try {
    tx.begin();
    Customer customer = new Customer("CUST-001", "John Doe");
    pm.makePersistent(customer);
    tx.commit();
} finally {
    if (tx.isActive()) {
        tx.rollback();
    }
    pm.close();
}
```

#### Querying for a Customer (JDO)

```java
String query = LegacyQueries.byCustomerId("CUST-001");
// Execute query via JDO PersistenceManager
```

---

### Entity Performance Considerations

#### Memory Footprint

**Estimated Size**: ~50-100 bytes per instance
- String id: ~40-80 bytes (depending on length)
- String name: ~40-80 bytes (depending on length)
- Object overhead: ~16 bytes

**Assessment**: ✅ Lightweight

---

#### Indexing Recommendations

**Primary Key**: `id` (automatically indexed)

**Additional Indexes** (if queries added):
- Index on `name` (for search by name)
- Composite index (if multi-field queries)

---

### Entity Security

#### Data Sensitivity

**id**: 🟡 Medium sensitivity (customer identifier)  
**name**: 🟢 Low-Medium sensitivity (PII)

**Compliance**:
- ⚠️ GDPR: Customer name is PII
- ⚠️ CCPA: Customer data subject to privacy regulations

**Recommendations**:
- Encrypt name field (at rest and in transit)
- Implement data retention policies
- Add audit logging for access
- Implement right to erasure (GDPR)

---

### Entity Migration Path

#### Phase 1: Add Validation
```java
// Add validation without breaking existing code
Objects.requireNonNull(id, "Customer ID cannot be null");
Objects.requireNonNull(name, "Customer name cannot be null");
```

#### Phase 2: Migrate to JPA
```java
// Replace JDO annotations with JPA
@Entity
@Table(name = "customer")
public class Customer {
    @Id
    private final String id;
    
    @Column(nullable = false, length = 100)
    private final String name;
}
```

#### Phase 3: Add Methods
```java
// Add equals, hashCode, toString
@Override
public boolean equals(Object o) { ... }

@Override
public int hashCode() { ... }

@Override
public String toString() { ... }
```

---

## Data Model Quality Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Immutability | ✅ Excellent | All fields final |
| Validation | 🔴 Poor | No validation |
| Identity | 🟡 Partial | Missing equals/hashCode |
| Documentation | 🟢 Good | Clear purpose |
| Security | 🟡 Moderate | No encryption, PII concerns |
| JPA Readiness | 🟡 Moderate | Needs annotation migration |

**Overall**: 🟡 **MODERATE** - Good foundation, needs improvements

---

## Related Documentation

- [Program Structure](program-structure.md) - Complete class details
- [Interfaces](interfaces.md) - Public API reference
- [Architecture Patterns](../architecture/patterns.md) - Entity pattern
- [Technical Debt](../technical-debt-report.md) - JDO deprecation

---

*Last Updated: January 2026*  
*Total Entities: 1*  
*Persistence Technology: JDO (deprecated)*  
*Immutability: Yes*  
*Validation: None*
