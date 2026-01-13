# System Overview - Architecture

## Introduction

This document provides a high-level architectural overview of the transform-legacy-demo system, describing the system's structure, design principles, and key architectural decisions.

---

## System Context

### Purpose
The transform-legacy-demo system demonstrates a legacy Java persistence pattern using Java Data Objects (JDO). The system provides customer data management with basic CRUD operations through a layered architecture.

### System Boundaries
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         transform-legacy-demo System                │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │         Application Layer                   │   │
│  │        (legacy-app module)                  │   │
│  │                                             │   │
│  │  • Customer entity (domain model)          │   │
│  │  • CustomerService (business logic)        │   │
│  │  • CustomerDao (data access)               │   │
│  └───────────────┬─────────────────────────────┘   │
│                  │                                  │
│                  │ depends on                       │
│                  │                                  │
│  ┌───────────────▼─────────────────────────────┐   │
│  │      Persistence Wrapper Layer             │   │
│  │       (legacy-wrappers module)             │   │
│  │                                             │   │
│  │  • LegacyJdoManager (transaction mgmt)     │   │
│  │  • LegacyQueries (query utilities)         │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         │ JDO API
                         ▼
                  [JDO Implementation]
                         │
                         ▼
                    [Database]
```

### External Dependencies
- **JDO API (javax.jdo:jdo-api:3.1)**: Java Data Objects persistence interface
- **JUnit Jupiter 5.10.2**: Testing framework
- **Maven Central**: Dependency repository

---

## Architectural Style

### Layered Architecture

The system follows a **3-tier layered architecture** pattern with clear separation between presentation (service), business logic (dao), and data access (persistence wrappers).

#### Layer Definitions

**Layer 1: Service Layer**
- **Component**: CustomerService
- **Responsibilities**: 
  - Transaction lifecycle management
  - Business logic coordination
  - Error handling and rollback
- **Dependencies**: CustomerDao, LegacyJdoManager

**Layer 2: Data Access Layer**
- **Component**: CustomerDao
- **Responsibilities**: 
  - Query construction
  - Data retrieval operations
  - Result formatting
- **Dependencies**: LegacyQueries

**Layer 3: Persistence Wrapper Layer**
- **Components**: LegacyJdoManager, LegacyQueries
- **Responsibilities**: 
  - Transaction management primitives
  - Query string construction utilities
  - JDO API abstraction
- **Dependencies**: None (intentionally dependency-free)

---

## Module Architecture

### Module Structure

The system is organized into two Gradle modules with unidirectional dependency:

```
legacy-app (Application Module)
    │
    │ implementation dependency
    │
    └──→ legacy-wrappers (Wrapper Module)
```

### Module Responsibilities

#### Module: `legacy-app`
**Purpose**: Contains application-level business logic and domain models

**Components**:
- `Customer.java` - JDO-annotated entity representing customer domain model
- `CustomerDao.java` - Data access object for customer operations
- `CustomerService.java` - Service layer orchestrating business operations

**Dependencies**:
- Project dependency: `:legacy-wrappers`
- External: `javax.jdo:jdo-api:3.1`

**Package**: `com.verafin.legacy`

#### Module: `legacy-wrappers`
**Purpose**: Provides reusable persistence utilities abstracting JDO complexity

**Components**:
- `LegacyJdoManager.java` - Transaction management utilities
- `LegacyQueries.java` - Query construction helpers

**Dependencies**:
- None (intentionally kept clean)

**Package**: `com.verafin.commons.jdo`

### Architectural Decision: Module Separation

**Rationale**: The separation of persistence utilities into a dedicated wrapper module follows the **Separation of Concerns** principle:

1. **Isolation of JDO Dependencies**: Centralizes JDO-specific code in one module
2. **Reusability**: Wrapper utilities can be shared across multiple application modules
3. **Migration Flexibility**: Allows replacing persistence layer without modifying application logic
4. **Dependency Management**: Keeps application module focused on business logic

**Trade-offs**:
- Adds complexity with additional module
- Increases build dependencies
- Benefits significant only in larger systems (marginal for 2-module system)

---

## Design Principles

### 1. Separation of Concerns
Each layer has distinct responsibilities:
- **Service layer**: Transaction boundaries and business coordination
- **DAO layer**: Data access and query construction
- **Persistence layer**: Low-level persistence operations

### 2. Dependency Inversion
Higher layers depend on lower layers through interfaces (conceptually):
- CustomerService depends on CustomerDao abstraction
- CustomerDao depends on LegacyQueries utilities

### 3. Single Responsibility
Each class has a focused purpose:
- `Customer`: Domain entity representation
- `CustomerDao`: Data access operations
- `CustomerService`: Transaction and business logic
- `LegacyJdoManager`: Transaction lifecycle
- `LegacyQueries`: Query construction

### 4. Explicit Transaction Management
Transactions are manually controlled with visible begin/commit/rollback, providing explicit control over transaction boundaries (contrasts with modern declarative transaction management).

---

## Key Architectural Patterns

### 1. Data Access Object (DAO) Pattern
**Implementation**: `CustomerDao` class

**Purpose**: Abstracts data access operations from business logic

**Benefits**:
- Centralized data access logic
- Easier testing (can mock DAO)
- Clear separation between business and data layers

### 2. Service Layer Pattern
**Implementation**: `CustomerService` class

**Purpose**: Defines application's boundary and provides transaction management

**Benefits**:
- Transaction boundary definition
- Coordination of multiple DAOs (if needed)
- Centralized business logic

### 3. Transaction Script Pattern
**Implementation**: Manual transaction management in CustomerService

**Pattern**: Explicit begin/commit/rollback in service methods

**Code Example**:
```java
public String formatDisplay(String customerId) {
    manager.begin();
    try {
        // business logic
        manager.commit();
        return result;
    } catch (RuntimeException e) {
        manager.rollback();
        throw e;
    }
}
```

**Characteristics**:
- Simple, procedural approach
- Explicit error handling
- Manual resource management

---

## Component Interaction Flow

### High-Level Interaction

```
[Client/Test]
     │
     │ calls
     ▼
CustomerService.formatDisplay(customerId)
     │
     │ 1. manager.begin()
     │
     │ 2. calls
     ▼
CustomerDao.byId(customerId)
     │
     │ constructs query using
     ▼
LegacyQueries.byCustomerId(customerId)
     │
     │ returns query string
     │
     │ 3. executes query, returns Customer
     │
     │ 4. manager.commit()
     │
     │ 5. returns formatted string
     ▼
[Client/Test]
```

### Transaction Lifecycle

```
BEGIN TRANSACTION
    │
    ├─→ Execute Business Logic
    │       │
    │       ├─→ Call DAO
    │       │       │
    │       │       └─→ Execute Query
    │       │
    │       └─→ Process Result
    │
    ├─→ SUCCESS?
    │    ├─ YES → COMMIT TRANSACTION
    │    └─ NO  → ROLLBACK TRANSACTION
    │
END TRANSACTION
```

---

## Data Flow Architecture

### Information Flow

```
User Request
    │
    ▼
Service Layer (Transaction Boundary)
    │
    ▼
DAO Layer (Query Construction)
    │
    ▼
Persistence Wrappers (JDO Operations)
    │
    ▼
JDO Implementation
    │
    ▼
Database
```

### Data Transformation Pipeline

1. **Input**: Customer ID (String)
2. **Query Construction**: LegacyQueries builds query string
3. **Query Execution**: DAO executes query via JDO
4. **Entity Retrieval**: JDO returns Customer object
5. **Business Logic**: Service formats display string
6. **Output**: Formatted string "id:name"

---

## Architectural Constraints

### Technology Constraints
- **Java 11**: Language and runtime version
- **JDO 3.1**: Persistence API (deprecated)
- **Gradle 8.5**: Build system
- **JUnit 5**: Testing framework

### Design Constraints
- **Manual Transactions**: No declarative transaction support
- **No Dependency Injection**: Manual object instantiation
- **No ORM Features**: Basic JDO without advanced mapping
- **String-based Queries**: Query construction via string concatenation

### Operational Constraints
- **Single Module Dependency**: legacy-app can only depend on legacy-wrappers
- **Maven Central Only**: All dependencies must be from public Maven Central
- **Java Toolchain**: Must use Java 11 toolchain

---

## Architectural Quality Attributes

### Maintainability
**Rating**: ⚠️ Medium

**Strengths**:
- Clear module separation
- Small codebase size
- Well-defined layers

**Weaknesses**:
- Deprecated persistence technology
- Manual transaction management
- String-based query construction

### Scalability
**Rating**: Low (not designed for scale)

**Limitations**:
- No connection pooling evident
- No caching layer
- Manual transaction management overhead

### Testability
**Rating**: ✅ Good

**Strengths**:
- Unit tests present
- Clear layer separation enables mocking
- Simple, focused classes

### Security
**Rating**: ⚠️ Moderate Risk

**Concerns**:
- Potential SQL injection in query construction
- No input validation evident
- Manual transaction management error potential

### Modifiability
**Rating**: ✅ Good (for small changes), ⚠️ Poor (for technology migration)

**Analysis**:
- Adding business logic: Easy
- Changing persistence technology: Difficult (requires wrapper module rewrite)
- Replacing JDO: High effort due to deep integration

---

## Architectural Technical Debt

### Critical Issues

1. **Deprecated Persistence Technology (JDO)**
   - **Impact**: High maintenance risk, limited ecosystem support
   - **Priority**: HIGH

2. **Manual Transaction Management**
   - **Impact**: Error-prone, verbose, high maintenance burden
   - **Priority**: Medium

3. **String-based Query Construction**
   - **Impact**: SQL injection risk, no compile-time validation
   - **Priority**: High

### See Also
- [Technical Debt Report](../technical-debt-report.md) - Comprehensive technical debt analysis
- [Remediation Plan](../technical-debt/remediation-plan.md) - Prioritized action items

---

## Future Architecture Considerations

### Modernization Options

1. **Persistence Layer Migration**
   - Replace JDO with JPA/Hibernate
   - Implement Spring Data repositories
   - Add declarative transaction management

2. **Service Layer Enhancement**
   - Introduce dependency injection (Spring)
   - Add declarative transactions (@Transactional)
   - Implement proper exception hierarchy

3. **Security Improvements**
   - Parameterized queries
   - Input validation framework
   - Security annotations

### See Also
- [Modernization Options](../migration/modernization-options.md) - Detailed migration strategies
- [Component Order](../migration/component-order.md) - Recommended migration sequence

---

## References

### Internal Documentation
- [Project Overview](../project-overview.md)
- [Components](components.md)
- [Dependencies](dependencies.md)
- [Patterns](patterns.md)

### Related Diagrams
- [Dependency Graph](../diagrams/structural/dependency-graph.md)
- [Class Diagram](../diagrams/structural/class-diagram.md)

---

*Last Updated: January 2026*  
*Analysis Method: Static architecture analysis*  
*Coverage: Complete system architecture documented*
