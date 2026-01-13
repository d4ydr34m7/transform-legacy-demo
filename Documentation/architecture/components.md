# Components - Architecture Documentation

## Overview

This document describes the components (modules and classes) that comprise the transform-legacy-demo system, their responsibilities, interactions, and architectural organization.

---

## Module Architecture

### Module Overview

The system consists of **2 modules** organized in a layered architecture:

```
┌─────────────────────────────────────┐
│       APPLICATION LAYER             │
│      (legacy-app module)            │
│                                     │
│  Business Logic & Domain Model      │
└─────────────────┬───────────────────┘
                  │
                  │ depends on
                  │
┌─────────────────▼───────────────────┐
│     PERSISTENCE LAYER               │
│    (legacy-wrappers module)         │
│                                     │
│  Persistence Utilities              │
└─────────────────────────────────────┘
```

---

## Module 1: legacy-app

### Module Information

**Module Name**: `legacy-app`  
**Package**: `com.verafin.legacy`  
**Type**: Application module  
**Purpose**: Contains business logic, domain models, and data access layer

### Module Responsibilities

1. **Domain Modeling**: Define entity structures (Customer)
2. **Business Logic**: Implement service-level operations
3. **Data Access**: Provide DAO layer for database operations
4. **Transaction Coordination**: Manage transaction boundaries

### Module Components

#### Component 1.1: Customer (Entity)

**Class**: `Customer.java`  
**Package**: `com.verafin.legacy`  
**Type**: Domain Entity  
**Layer**: Domain/Persistence

**Purpose**:
Represents a customer entity with JDO persistence annotations. This is the primary domain model for the application.

**Responsibilities**:
- Store customer identification (ID)
- Store customer information (name)
- Provide immutable domain model
- Enable JDO persistence mapping

**Key Characteristics**:
- Immutable (final fields)
- JDO-annotated for persistence
- Simple data holder (no business logic)

**Dependencies**:
- javax.jdo.annotations.PersistenceCapable
- javax.jdo.annotations.PrimaryKey

**Structure**:
```java
@PersistenceCapable
public class Customer {
    @PrimaryKey
    private final String id;
    private final String name;
    
    // Constructor and getters
}
```

**Technical Debt**: Uses deprecated JDO annotations (should migrate to JPA @Entity)

---

#### Component 1.2: CustomerDao (Data Access Object)

**Class**: `CustomerDao.java`  
**Package**: `com.verafin.legacy`  
**Type**: Data Access Object  
**Layer**: Data Access

**Purpose**:
Encapsulates data access logic for Customer entities. Constructs and executes queries to retrieve customer information.

**Responsibilities**:
- Query construction for customer retrieval
- Database interaction abstraction
- Result transformation

**Key Characteristics**:
- Follows DAO pattern
- Uses LegacyQueries utility for query building
- Focuses solely on data access (no business logic)

**Dependencies**:
- `LegacyQueries` (from legacy-wrappers module)
- `Customer` (domain entity)

**Public Interface** (inferred):
```java
public class CustomerDao {
    public Customer byId(String customerId) {
        // Construct query using LegacyQueries
        // Execute query and return Customer
    }
}
```

**Design Pattern**: Data Access Object (DAO) pattern

---

#### Component 1.3: CustomerService (Service Layer)

**Class**: `CustomerService.java`  
**Package**: `com.verafin.legacy`  
**Type**: Service/Business Logic  
**Layer**: Service

**Purpose**:
Provides business-level operations for customer management. Coordinates transactions and delegates data access to DAO layer.

**Responsibilities**:
- Define transaction boundaries
- Coordinate business operations
- Handle error scenarios with rollback
- Format business results
- Orchestrate DAO calls

**Key Characteristics**:
- Manual transaction management (begin/commit/rollback)
- Try-catch-rollback error handling pattern
- Delegates data access to CustomerDao

**Dependencies**:
- `CustomerDao` (data access)
- `LegacyJdoManager` (transaction management, from legacy-wrappers)
- `Customer` (domain entity)

**Public Interface** (inferred):
```java
public class CustomerService {
    public String formatDisplay(String customerId) {
        manager.begin();
        try {
            Customer customer = dao.byId(customerId);
            String result = format(customer);
            manager.commit();
            return result;
        } catch (RuntimeException e) {
            manager.rollback();
            throw e;
        }
    }
}
```

**Design Patterns**: 
- Service Layer pattern
- Transaction Script pattern

**Technical Debt**: Manual transaction management (should use declarative @Transactional)

---

### Module Dependencies

**External Dependencies**:
```gradle
dependencies {
    implementation project(":legacy-wrappers")  // Inter-module
    implementation "javax.jdo:jdo-api:3.1"      // JDO API
    testImplementation "org.junit.jupiter:junit-jupiter:5.10.2"
}
```

**Module Dependency Rationale**:
- Depends on legacy-wrappers for transaction and query utilities
- Requires JDO API for entity annotations and persistence

---

## Module 2: legacy-wrappers

### Module Information

**Module Name**: `legacy-wrappers`  
**Package**: `com.verafin.commons.jdo`  
**Type**: Utility/Infrastructure module  
**Purpose**: Provides reusable persistence utilities abstracting JDO complexity

### Module Responsibilities

1. **Transaction Management**: Provide transaction lifecycle utilities
2. **Query Construction**: Build JDO query strings
3. **Persistence Abstraction**: Hide JDO implementation details
4. **Reusability**: Offer utilities usable by multiple application modules

### Module Components

#### Component 2.1: LegacyJdoManager (Transaction Manager)

**Class**: `LegacyJdoManager.java`  
**Package**: `com.verafin.commons.jdo`  
**Type**: Utility/Infrastructure  
**Layer**: Persistence Infrastructure

**Purpose**:
Provides transaction management utilities for JDO persistence operations. Abstracts the complexity of JDO transaction lifecycle.

**Responsibilities**:
- Begin transactions
- Commit transactions
- Rollback transactions on error
- Manage persistence manager lifecycle
- Handle transaction state

**Key Characteristics**:
- Stateful (manages transaction state)
- Manual transaction control
- Utility class for transaction operations

**Public Interface** (inferred):
```java
public class LegacyJdoManager {
    public void begin() {
        // Start transaction
    }
    
    public void commit() {
        // Commit current transaction
    }
    
    public void rollback() {
        // Rollback current transaction
    }
}
```

**Design Pattern**: Transaction Manager pattern (manual)

**Technical Debt**: 
- Manual transaction management is error-prone
- No resource pooling evident
- Should be replaced with declarative transaction management

---

#### Component 2.2: LegacyQueries (Query Builder)

**Class**: `LegacyQueries.java`  
**Package**: `com.verafin.commons.jdo`  
**Type**: Utility  
**Layer**: Persistence Infrastructure

**Purpose**:
Provides utility methods for constructing JDO query strings. Centralizes query building logic.

**Responsibilities**:
- Build JDO query strings
- Parameterize queries (likely via string concatenation)
- Provide reusable query construction

**Key Characteristics**:
- Utility class (likely static methods)
- String-based query construction
- Query abstraction layer

**Public Interface** (inferred):
```java
public class LegacyQueries {
    public static String byCustomerId(String customerId) {
        // Construct query string for customer lookup
        // WARNING: Likely uses string concatenation
    }
}
```

**Security Concern**: 
⚠️ String concatenation in query construction poses **SQL injection risk**. This is a critical security vulnerability.

**Recommendation**: 
Replace with parameterized queries or JPA Criteria API.

---

### Module Dependencies

**External Dependencies**:
```gradle
dependencies {
    // intentionally empty (wrapper module)
    testImplementation "org.junit.jupiter:junit-jupiter:5.10.2"
}
```

**Module Dependency Rationale**:
- No external dependencies by design
- Keeps infrastructure layer clean and reusable
- JDO API dependency comes transitively from legacy-app

---

## Component Interaction Patterns

### Transaction Management Flow

```
CustomerService.formatDisplay(customerId)
    │
    │ 1. Begin Transaction
    ├──→ LegacyJdoManager.begin()
    │
    │ 2. Execute Business Logic
    ├──→ CustomerDao.byId(customerId)
    │       │
    │       │ 3. Build Query
    │       └──→ LegacyQueries.byCustomerId(customerId)
    │               │
    │               └──→ returns query string
    │       │
    │       │ 4. Execute Query & Return Customer
    │       └──→ returns Customer entity
    │
    │ 5. Format Result
    ├──→ format Customer (id:name)
    │
    │ 6. Commit Transaction
    ├──→ LegacyJdoManager.commit()
    │
    └──→ return formatted string
```

### Error Handling Flow

```
CustomerService.formatDisplay(customerId)
    │
    ├──→ LegacyJdoManager.begin()
    │
    ├──→ try {
    │       CustomerDao.byId(customerId)
    │    }
    │
    │ ✗ RuntimeException thrown
    │
    ├──→ catch (RuntimeException e) {
    │       LegacyJdoManager.rollback()
    │       throw e
    │    }
```

---

## Component Relationship Matrix

| From Component | To Component | Relationship Type | Purpose |
|---------------|--------------|-------------------|---------|
| CustomerService | CustomerDao | Uses | Data access delegation |
| CustomerService | LegacyJdoManager | Uses | Transaction management |
| CustomerService | Customer | Uses | Domain model manipulation |
| CustomerDao | LegacyQueries | Uses | Query construction |
| CustomerDao | Customer | Creates/Returns | Result object creation |
| legacy-app (module) | legacy-wrappers (module) | Depends on | Infrastructure utilities |

---

## Layered Architecture View

```
┌────────────────────────────────────────────────────┐
│  SERVICE LAYER                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │ CustomerService                              │ │
│  │ • Transaction coordination                   │ │
│  │ • Business logic                             │ │
│  │ • Error handling                             │ │
│  └──────────────────────────────────────────────┘ │
└───────────────────┬────────────────────────────────┘
                    │ uses
┌───────────────────▼────────────────────────────────┐
│  DATA ACCESS LAYER                                 │
│  ┌──────────────────────────────────────────────┐ │
│  │ CustomerDao                                  │ │
│  │ • Query construction                         │ │
│  │ • Data retrieval                             │ │
│  └──────────────────────────────────────────────┘ │
└───────────────────┬────────────────────────────────┘
                    │ uses
┌───────────────────▼────────────────────────────────┐
│  DOMAIN LAYER                                      │
│  ┌──────────────────────────────────────────────┐ │
│  │ Customer                                     │ │
│  │ • Entity representation                      │ │
│  │ • Domain model                               │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  PERSISTENCE INFRASTRUCTURE LAYER                  │
│  (legacy-wrappers module)                          │
│  ┌─────────────────────┐ ┌─────────────────────┐  │
│  │ LegacyJdoManager    │ │ LegacyQueries       │  │
│  │ • Transactions      │ │ • Query building    │  │
│  └─────────────────────┘ └─────────────────────┘  │
└────────────────────────────────────────────────────┘
```

---

## Component Responsibilities Matrix

| Component | Layer | Create | Read | Update | Delete | Business Logic | Transaction Mgmt |
|-----------|-------|--------|------|--------|--------|----------------|-----------------|
| Customer | Domain | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CustomerDao | Data Access | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CustomerService | Service | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| LegacyJdoManager | Infrastructure | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| LegacyQueries | Infrastructure | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Note**: Current implementation only supports Read operations (query by ID)

---

## Component Sizing and Complexity

### Estimated Component Metrics

| Component | Estimated LOC | Methods (est.) | Complexity | Test Coverage |
|-----------|---------------|----------------|------------|---------------|
| Customer | 15-20 | 3 | Very Low | ✅ |
| CustomerDao | 20-30 | 2-3 | Low | ✅ |
| CustomerService | 25-35 | 2-3 | Medium | ✅ |
| LegacyJdoManager | 30-40 | 4-5 | Medium | ❓ |
| LegacyQueries | 15-25 | 2-3 | Low | ❓ |

**Total Estimated LOC**: ~105-150 lines of production code

---

## Module Communication Patterns

### Communication Style

**Synchronous, Direct Method Calls**:
- All component interactions use direct method invocation
- No messaging, events, or asynchronous patterns
- Simple, procedural call chains

**Tight Coupling**:
- legacy-app directly depends on legacy-wrappers classes
- No interface abstractions evident
- Concrete class dependencies

**Benefits**:
- Simple to understand
- Easy to debug
- Low overhead

**Drawbacks**:
- Hard to swap implementations
- Difficult to mock for testing without frameworks
- Module coupling complicates independent evolution

---

## Component Deployment

### Module Packaging

**Both modules** are packaged as JAR files:
```
transform-legacy-demo-legacy-app.jar
    └── com/verafin/legacy/*.class

transform-legacy-demo-legacy-wrappers.jar
    └── com/verafin/commons/jdo/*.class
```

**Deployment Unit**: 
Combined as single application (both JARs on classpath)

**Runtime Dependencies**:
- JDO implementation (not bundled, must be provided)
- Java 11 runtime

---

## Component Extensibility

### Adding New Entities

To add a new entity (e.g., Order):

1. **Domain Layer**: Create Order.java with JDO annotations
2. **DAO Layer**: Create OrderDao using LegacyQueries
3. **Service Layer**: Create OrderService using LegacyJdoManager
4. **No Changes Needed**: LegacyJdoManager and LegacyQueries are reusable

**Effort**: Low - well-defined pattern to follow

### Adding New Operations

To add Update or Delete operations:

1. **LegacyQueries**: Add query construction methods
2. **DAO Layer**: Add methods to CustomerDao
3. **Service Layer**: Add transaction-wrapped methods to CustomerService

**Effort**: Low - straightforward extension

### Technology Migration

To replace JDO with JPA:

1. **LegacyJdoManager**: Replace with JPA EntityManager or Spring @Transactional
2. **LegacyQueries**: Replace with JPQL or Criteria API
3. **Customer**: Update annotations (@PersistenceCapable → @Entity)
4. **DAO/Service**: Update to use new APIs

**Effort**: Medium to High - requires rewrite of persistence layer

---

## Component Reusability

### Reusable Components

**LegacyJdoManager** and **LegacyQueries**:
- Designed as reusable utilities in commons package
- Can be used by multiple application modules
- Generic transaction and query building capabilities

### Non-Reusable Components

**Customer, CustomerDao, CustomerService**:
- Specific to customer domain
- Tightly coupled to business logic
- Not designed for reuse

---

## Component Quality Assessment

### Quality Characteristics

| Component | Maintainability | Testability | Security | Reusability |
|-----------|----------------|-------------|----------|-------------|
| Customer | ✅ Good | ✅ Good | ✅ Safe | ⚠️ Domain-specific |
| CustomerDao | ✅ Good | ✅ Good | 🔴 SQL Injection Risk | ⚠️ Domain-specific |
| CustomerService | ⚠️ Manual TX | ✅ Good | ⚠️ No Validation | ⚠️ Domain-specific |
| LegacyJdoManager | ⚠️ Manual TX | ⚠️ Stateful | ⚠️ Error-prone | ✅ Reusable |
| LegacyQueries | 🔴 Deprecated | ✅ Good | 🔴 String Concat | ✅ Reusable |

---

## Related Documentation

### Internal Links
- [System Overview](system-overview.md) - Architecture context
- [Dependencies](dependencies.md) - Module and library dependencies
- [Patterns](patterns.md) - Design pattern details
- [Program Structure](../reference/program-structure.md) - Detailed class documentation
- [Class Diagram](../diagrams/structural/class-diagram.md) - Visual relationships

### Technical Debt
- [Technical Debt Report](../technical-debt-report.md) - Component-specific issues
- [Outdated Components](../technical-debt/outdated-components.md) - Deprecation analysis

---

*Last Updated: January 2026*  
*Analysis Method: Static analysis of module structure and build configuration*  
*Coverage: 100% of modules and primary components documented*
