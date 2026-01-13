# Program Structure - Reference Documentation

## Overview

This document provides complete structural documentation of all classes, interfaces, and code organization in the transform-legacy-demo codebase.

---

## Project Structure

```
transform-legacy-demo/
├── legacy-app/                           # Application module
│   ├── src/main/java/
│   │   └── com/verafin/legacy/
│   │       ├── Customer.java            [Entity] (20 LOC)
│   │       ├── CustomerDao.java         [DAO] (16 LOC)
│   │       └── CustomerService.java     [Service] (21 LOC)
│   └── src/test/java/
│       └── com/verafin/legacy/
│           ├── CustomerDaoTest.java     [Test] (12 LOC)
│           └── CustomerServiceTest.java [Test] (11 LOC)
│
└── legacy-wrappers/                      # Persistence wrapper module
    └── src/main/java/
        └── com/verafin/commons/jdo/
            ├── LegacyJdoManager.java    [Utility] (5 LOC)
            └── LegacyQueries.java       [Utility] (7 LOC)

Total LOC: ~92 lines of code
```

---

## Class Inventory

### Main Classes: 5
### Test Classes: 2
### Total Classes: 7

---

## Module 1: legacy-app

### Package: com.verafin.legacy

#### Class 1: Customer

**Type**: Entity / Domain Model  
**File**: `legacy-app/src/main/java/com/verafin/legacy/Customer.java`  
**Lines of Code**: ~20  
**Purpose**: Represents a customer domain entity with JDO persistence mapping

**Class Signature**:
```java
@PersistenceCapable
public class Customer
```

**Fields**:
```java
@PrimaryKey
private final String id;        // Customer unique identifier
private final String name;      // Customer name
```

**Constructor**:
```java
public Customer(String id, String name)
```

**Methods**:
- `String getId()` - Returns customer ID
- `String getName()` - Returns customer name

**Annotations**:
- `@PersistenceCapable` (JDO) - Marks class as persistable
- `@PrimaryKey` (JDO) - Marks id field as primary key

**Dependencies**:
- javax.jdo.annotations.PersistenceCapable
- javax.jdo.annotations.PrimaryKey

**Characteristics**:
- Immutable (all fields final)
- No business logic (pure data holder)
- JDO-annotated for persistence

**Design Pattern**: Entity Pattern  
**Technical Debt**: JDO annotations (deprecated, should migrate to JPA @Entity)

---

#### Class 2: CustomerDao

**Type**: Data Access Object  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerDao.java`  
**Lines of Code**: ~16  
**Purpose**: Provides data access operations for Customer entities

**Class Signature**:
```java
public class CustomerDao
```

**Fields**:
```java
private final LegacyJdoManager jdo;  // JDO persistence manager wrapper
```

**Constructor**:
```java
public CustomerDao(LegacyJdoManager jdo)
```

**Methods**:
- `String buildFindByIdQuery(String id)` - Constructs query to find customer by ID
  - **Parameters**: `String id` - Customer ID to search for
  - **Returns**: `String` - JDO query string
  - **Implementation**: Delegates to `LegacyQueries.byCustomerId(id)`

**Dependencies**:
- LegacyJdoManager (from legacy-wrappers)
- LegacyQueries (from legacy-wrappers)

**Collaborators**:
- LegacyQueries - for query construction
- LegacyJdoManager - for persistence management

**Design Pattern**: Data Access Object (DAO) Pattern  
**Technical Debt**: None specific to this class (issues in dependencies)

---

#### Class 3: CustomerService

**Type**: Service Layer / Business Logic  
**File**: `legacy-app/src/main/java/com/verafin/legacy/CustomerService.java`  
**Lines of Code**: ~21  
**Purpose**: Provides business-level operations with transaction management

**Class Signature**:
```java
public class CustomerService
```

**Fields**:
```java
private final LegacyJdoManager jdo;  // Transaction manager
```

**Constructor**:
```java
public CustomerService(LegacyJdoManager jdo)
```

**Methods**:
- `String formatDisplay(Customer c)` - Formats customer for display
  - **Parameters**: `Customer c` - Customer to format
  - **Returns**: `String` - Formatted string "id:name"
  - **Transaction**: Managed (begin/commit/rollback)
  - **Error Handling**: Try-catch with rollback on RuntimeException
  - **Implementation**:
    ```java
    jdo.begin();
    try {
        String out = c.getId() + ":" + c.getName();
        jdo.commit();
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();
        throw e;
    }
    ```

**Dependencies**:
- LegacyJdoManager (from legacy-wrappers)
- Customer (domain entity)

**Design Pattern**: Service Layer, Transaction Script  
**Technical Debt**: Manual transaction management (should use @Transactional)

---

### Test Classes

#### Test Class 1: CustomerDaoTest

**Type**: Unit Test  
**File**: `legacy-app/src/test/java/com/verafin/legacy/CustomerDaoTest.java`  
**Lines of Code**: ~12  
**Purpose**: Tests CustomerDao query construction

**Test Methods**:
- `void buildsLegacyQuery()` - Verifies query construction
  - Creates CustomerDao with LegacyJdoManager
  - Calls `buildFindByIdQuery("123")`
  - Asserts query contains "Customer" and "id =="

**Dependencies**:
- JUnit Jupiter 5.10.2
- CustomerDao
- LegacyJdoManager

---

#### Test Class 2: CustomerServiceTest

**Type**: Unit Test  
**File**: `legacy-app/src/test/java/com/verafin/legacy/CustomerServiceTest.java`  
**Lines of Code**: ~11  
**Purpose**: Tests CustomerService business logic

**Test Methods**:
- `void formatsDisplay()` - Verifies customer display formatting
  - Creates CustomerService with LegacyJdoManager
  - Calls `formatDisplay(new Customer("1", "Shreya"))`
  - Asserts result equals "1:Shreya"

**Dependencies**:
- JUnit Jupiter 5.10.2
- CustomerService
- LegacyJdoManager
- Customer

---

## Module 2: legacy-wrappers

### Package: com.verafin.commons.jdo

#### Class 4: LegacyJdoManager

**Type**: Utility / Transaction Manager  
**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyJdoManager.java`  
**Lines of Code**: ~5  
**Purpose**: Provides transaction management primitives for JDO

**Class Signature**:
```java
public class LegacyJdoManager
```

**Fields**: None

**Constructor**: Default (implicit)

**Methods**:
- `void begin()` - Begins a transaction
  - **Implementation**: Empty (stub for demo)
- `void commit()` - Commits current transaction
  - **Implementation**: Empty (stub for demo)
- `void rollback()` - Rolls back current transaction
  - **Implementation**: Empty (stub for demo)

**Dependencies**: None

**Characteristics**:
- Stateless utility class
- Stub implementation (methods are empty)
- Would wrap JDO PersistenceManager in real implementation

**Design Pattern**: Transaction Manager (manual)  
**Technical Debt**: Manual transaction management

**Notes**: 
- Current implementation is a stub/mock
- Real implementation would manage JDO PersistenceManager
- Would handle transaction state and resource cleanup

---

#### Class 5: LegacyQueries

**Type**: Utility / Query Builder  
**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyQueries.java`  
**Lines of Code**: ~7  
**Purpose**: Provides JDO query construction utilities

**Class Signature**:
```java
public class LegacyQueries
```

**Fields**: None

**Constructor**: None (all methods static)

**Methods**:
- `static String byCustomerId(String id)` - Constructs JDO query by customer ID
  - **Parameters**: `String id` - Customer ID to search for
  - **Returns**: `String` - JDO query string
  - **Implementation**:
    ```java
    return "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";
    ```
  - **⚠️ Security Issue**: String concatenation enables SQL injection

**Dependencies**: None

**Design Pattern**: Query Builder (basic)  
**Technical Debt**: 🔴 SQL Injection vulnerability (CVSS 9.8)

**Security Vulnerability**:
- Line 4: String concatenation in query construction
- Risk: Allows malicious input to manipulate queries
- Example exploit: `id = "' OR '1'='1"` returns all customers
- **Priority**: CRITICAL - Fix immediately

---

## Class Relationships

### Dependency Graph

```
CustomerService
    │
    ├──[uses]──> LegacyJdoManager
    │
    └──[uses]──> Customer

CustomerDao
    │
    ├──[uses]──> LegacyJdoManager
    │
    └──[uses]──> LegacyQueries

CustomerDaoTest
    │
    ├──[tests]──> CustomerDao
    │
    └──[uses]──> LegacyJdoManager

CustomerServiceTest
    │
    ├──[tests]──> CustomerService
    │
    ├──[uses]──> LegacyJdoManager
    │
    └──[uses]──> Customer
```

### Layered View

```
┌─────────────────────────────────────┐
│  Test Layer                         │
│  CustomerDaoTest, CustomerServiceTest
└─────────────────┬───────────────────┘
                  │ tests
┌─────────────────▼───────────────────┐
│  Service Layer                      │
│  CustomerService                    │
└─────────────────┬───────────────────┘
                  │ uses
┌─────────────────▼───────────────────┐
│  Data Access Layer                  │
│  CustomerDao                        │
└─────────────────┬───────────────────┘
                  │ uses
┌─────────────────▼───────────────────┐
│  Domain Layer                       │
│  Customer                           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Infrastructure Layer (cross-cutting)│
│  LegacyJdoManager, LegacyQueries    │
└─────────────────────────────────────┘
```

---

## Package Organization

### Package: com.verafin.legacy

**Purpose**: Application-level business logic and domain models  
**Module**: legacy-app  
**Classes**: Customer, CustomerDao, CustomerService

**Naming Convention**: "legacy" indicates outdated/deprecated status

---

### Package: com.verafin.commons.jdo

**Purpose**: Reusable JDO persistence utilities  
**Module**: legacy-wrappers  
**Classes**: LegacyJdoManager, LegacyQueries

**Naming Convention**: 
- "commons" suggests shared/reusable utilities
- "jdo" indicates JDO-specific functionality

---

## Code Metrics Summary

| Metric | Value |
|--------|-------|
| Total Classes | 7 (5 main + 2 test) |
| Total Lines of Code | ~92 LOC |
| Average Class Size | ~13 LOC |
| Largest Class | CustomerService (21 LOC) |
| Smallest Class | LegacyJdoManager (5 LOC) |
| Public Methods | ~10 |
| Test Classes | 2 |
| Test Methods | 2 |
| Packages | 2 |
| Modules | 2 |

---

## Complexity Analysis

**Overall Complexity**: ✅ **LOW**

| Class | Cyclomatic Complexity | Assessment |
|-------|----------------------|------------|
| Customer | 1 | ✅ Very Simple |
| CustomerDao | 1 | ✅ Very Simple |
| CustomerService | 2 | ✅ Simple |
| LegacyJdoManager | 1 | ✅ Very Simple |
| LegacyQueries | 1 | ✅ Very Simple |

**Note**: Low complexity indicates the codebase is easy to understand and maintain (aside from technical debt issues).

---

## Access Modifiers Analysis

| Class | Visibility | Fields | Methods |
|-------|-----------|--------|---------|
| Customer | public | private (2) | public (3) |
| CustomerDao | public | private (1) | public (1) |
| CustomerService | public | private (1) | public (1) |
| LegacyJdoManager | public | none | public (3) |
| LegacyQueries | public | none | public static (1) |

**Encapsulation**: ✅ Good - All fields are private, accessed via public methods

---

## Constructor Analysis

| Class | Constructor Parameters | Dependency Injection |
|-------|----------------------|----------------------|
| Customer | id, name | No (data) |
| CustomerDao | LegacyJdoManager | ✅ Yes (manual) |
| CustomerService | LegacyJdoManager | ✅ Yes (manual) |
| LegacyJdoManager | none | N/A |
| LegacyQueries | none (static) | N/A |

**Pattern**: Constructor injection (manual, not framework-based)

---

## Method Signature Reference

### Customer
```java
public Customer(String id, String name)
public String getId()
public String getName()
```

### CustomerDao
```java
public CustomerDao(LegacyJdoManager jdo)
public String buildFindByIdQuery(String id)
```

### CustomerService
```java
public CustomerService(LegacyJdoManager jdo)
public String formatDisplay(Customer c)
```

### LegacyJdoManager
```java
public void begin()
public void commit()
public void rollback()
```

### LegacyQueries
```java
public static String byCustomerId(String id)
```

---

## Immutability Analysis

| Class | Immutable | Reason |
|-------|-----------|--------|
| Customer | ✅ Yes | All fields final, no setters |
| CustomerDao | 🟡 Partially | Final field, but mutable operations |
| CustomerService | 🟡 Partially | Final field, but mutable operations |
| LegacyJdoManager | ✅ Yes | Stateless |
| LegacyQueries | ✅ Yes | Stateless, static methods |

---

## Related Documentation

- [Components](../architecture/components.md) - Component details and responsibilities
- [Patterns](../architecture/patterns.md) - Design patterns used
- [Data Models](data-models.md) - Entity documentation
- [Interfaces](interfaces.md) - Public API reference
- [Class Diagram](../diagrams/structural/class-diagram.md) - Visual relationships

---

*Last Updated: January 2026*  
*Total Classes: 7 (5 main + 2 test)*  
*Total LOC: ~92*  
*Complexity: LOW*  
*Documentation Coverage: 100%*
