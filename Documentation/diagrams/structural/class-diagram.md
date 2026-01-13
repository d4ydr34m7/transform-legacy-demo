# Class Diagram - Structural Documentation

## Overview

This document provides text-based UML-style class diagrams showing the relationships between all classes in the transform-legacy-demo codebase.

---

## Complete Class Diagram

### All Classes and Relationships

```
┌────────────────────────────────────────────────────────────────┐
│                        CLASS DIAGRAM                            │
│                   transform-legacy-demo                         │
└────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                     <<Entity>>                                   │
│                     Customer                                     │
│  Package: com.verafin.legacy                                     │
├──────────────────────────────────────────────────────────────────┤
│  Fields:                                                         │
│  - id: String (final, @PrimaryKey)                              │
│  - name: String (final)                                         │
├──────────────────────────────────────────────────────────────────┤
│  Methods:                                                        │
│  + Customer(id: String, name: String)                           │
│  + getId(): String                                              │
│  + getName(): String                                            │
└──────────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ uses
                            │
┌──────────────────────────────────────────────────────────────────┐
│                     CustomerService                               │
│  Package: com.verafin.legacy                                     │
├──────────────────────────────────────────────────────────────────┤
│  Fields:                                                         │
│  - jdo: LegacyJdoManager (final)                                │
├──────────────────────────────────────────────────────────────────┤
│  Methods:                                                        │
│  + CustomerService(jdo: LegacyJdoManager)                       │
│  + formatDisplay(c: Customer): String                           │
└──────────────────────────────────────────────────────────────────┘
                            │
                            │ uses
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     CustomerDao                                   │
│  Package: com.verafin.legacy                                     │
├──────────────────────────────────────────────────────────────────┤
│  Fields:                                                         │
│  - jdo: LegacyJdoManager (final)                                │
├──────────────────────────────────────────────────────────────────┤
│  Methods:                                                        │
│  + CustomerDao(jdo: LegacyJdoManager)                           │
│  + buildFindByIdQuery(id: String): String                       │
└──────────────────────────────────────────────────────────────────┘
                            │
                            │ uses
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                  <<Utility>>                                     │
│                  LegacyQueries                                   │
│  Package: com.verafin.commons.jdo                               │
├──────────────────────────────────────────────────────────────────┤
│  Methods:                                                        │
│  + byCustomerId(id: String): String <<static>>                  │
│                                                                  │
│  ⚠️  SQL INJECTION VULNERABILITY                                 │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  <<Utility>>                                     │
│               LegacyJdoManager                                   │
│  Package: com.verafin.commons.jdo                               │
├──────────────────────────────────────────────────────────────────┤
│  Methods:                                                        │
│  + begin(): void                                                │
│  + commit(): void                                               │
│  + rollback(): void                                             │
│                                                                  │
│  Note: Current implementation is stub/mock                      │
└──────────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            │ uses
                            │
        ┌───────────────────┴────────────────────┐
        │                                        │
┌───────┴─────────┐                   ┌──────────┴────────┐
│ CustomerService │                   │   CustomerDao      │
└─────────────────┘                   └───────────────────┘
```

---

## Detailed Class Relationships

### Relationship Matrix

| From Class | Relationship | To Class | Type | Multiplicity |
|-----------|--------------|----------|------|--------------|
| CustomerService | uses | LegacyJdoManager | Association | 1:1 |
| CustomerService | uses | Customer | Association | 1:* |
| CustomerDao | uses | LegacyJdoManager | Association | 1:1 |
| CustomerDao | uses | LegacyQueries | Dependency | * |
| CustomerDaoTest | tests | CustomerDao | Dependency | 1:1 |
| CustomerServiceTest | tests | CustomerService | Dependency | 1:1 |

---

## Layered Class Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                      TEST LAYER                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────┐         ┌──────────────────────┐        │
│  │ CustomerDaoTest  │         │ CustomerServiceTest  │        │
│  └────────┬─────────┘         └──────────┬───────────┘        │
│           │ tests                         │ tests              │
└───────────┼───────────────────────────────┼────────────────────┘
            │                               │
            │                               │
┌───────────▼───────────────────────────────▼────────────────────┐
│                    SERVICE LAYER                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              CustomerService                              │ │
│  │  + formatDisplay(Customer): String                       │ │
│  │  - Manages transactions                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                               │                                │
│                               │ uses                           │
└───────────────────────────────┼────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────┐
│                  DATA ACCESS LAYER                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              CustomerDao                                  │ │
│  │  + buildFindByIdQuery(String): String                    │ │
│  │  - Constructs queries                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                               │                                │
│                               │ uses                           │
└───────────────────────────────┼────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────┐
│                    DOMAIN LAYER                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Customer                                     │ │
│  │  - id: String                                            │ │
│  │  - name: String                                          │ │
│  │  + getId(): String                                       │ │
│  │  + getName(): String                                     │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│            INFRASTRUCTURE LAYER (cross-cutting)                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌───────────────────┐         ┌───────────────────────┐      │
│  │ LegacyJdoManager  │         │  LegacyQueries        │      │
│  │ + begin()         │         │  + byCustomerId()     │      │
│  │ + commit()        │         │    <<static>>         │      │
│  │ + rollback()      │         │  ⚠️  SQL Injection     │      │
│  └───────────────────┘         └───────────────────────┘      │
│          ▲                              ▲                      │
│          │                              │                      │
│          └──────────────┬───────────────┘                      │
│                         │                                      │
│                    Used by all                                 │
│                service/DAO layers                              │
└────────────────────────────────────────────────────────────────┘
```

---

## Package Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                     Package Structure                          │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  Module: legacy-app                                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Package: com.verafin.legacy                              │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  Customer              <<Entity>>                   │  │ │
│  │  │  CustomerDao           <<DAO>>                      │  │ │
│  │  │  CustomerService       <<Service>>                  │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
│         │                                                      │
│         │ depends on                                           │
│         ▼                                                      │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  Module: legacy-wrappers                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Package: com.verafin.commons.jdo                         │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  LegacyJdoManager      <<Utility>>                  │  │ │
│  │  │  LegacyQueries         <<Utility>>                  │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## Dependency Flow Diagram

```
Direction of Dependencies: Top → Bottom

┌─────────────────────┐
│  CustomerService    │
└──────────┬──────────┘
           │
           ├────────────┐
           │            │
           ▼            ▼
┌──────────────────┐ ┌──────────────┐
│  CustomerDao     │ │  Customer    │
└──────┬───────────┘ └──────────────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────────┐ ┌──────────────────┐
│LegacyQueries │ │LegacyJdoManager  │
└──────────────┘ └──────────────────┘
```

---

## Sequence Diagram: formatDisplay Operation

```
CustomerServiceTest  CustomerService  LegacyJdoManager  Customer
        │                  │                 │             │
        │ formatDisplay()  │                 │             │
        ├─────────────────>│                 │             │
        │                  │ begin()         │             │
        │                  ├────────────────>│             │
        │                  │                 │             │
        │                  │ getId()         │             │
        │                  ├────────────────────────────>  │
        │                  │<─────────────────────────────┤
        │                  │ "1"             │             │
        │                  │                 │             │
        │                  │ getName()       │             │
        │                  ├────────────────────────────>  │
        │                  │<─────────────────────────────┤
        │                  │ "Shreya"        │             │
        │                  │                 │             │
        │                  │ commit()        │             │
        │                  ├────────────────>│             │
        │                  │                 │             │
        │<─────────────────┤                 │             │
        │ "1:Shreya"       │                 │             │
```

---

## Object Diagram: Runtime Instance Example

```
┌─────────────────────────────┐
│  :CustomerServiceTest       │
│  (test instance)            │
└──────────┬──────────────────┘
           │ svc
           ▼
┌─────────────────────────────┐
│  svc:CustomerService        │
└──────────┬──────────────────┘
           │ jdo
           ▼
┌─────────────────────────────┐
│  jdo:LegacyJdoManager       │
└─────────────────────────────┘

           and

┌─────────────────────────────┐
│  :Customer                  │
│  id = "1"                   │
│  name = "Shreya"            │
└─────────────────────────────┘
```

---

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Interaction Patterns                       │
└──────────────────────────────────────────────────────────────┘

Pattern 1: Query Construction
┌──────────────┐         ┌─────────────┐         ┌──────────────┐
│ CustomerDao  │ uses    │LegacyQueries│ returns │ Query String │
│              ├────────>│             ├────────>│              │
└──────────────┘         └─────────────┘         └──────────────┘

Pattern 2: Transaction Management
┌──────────────┐         ┌──────────────────┐
│CustomerService│ uses   │LegacyJdoManager  │
│              ├────────>│ - begin()        │
│              │         │ - commit()       │
│              │         │ - rollback()     │
└──────────────┘         └──────────────────┘
```

---

## Class Stereotypes

```
<<Entity>>
  Customer
  - Represents domain model
  - Immutable
  - JDO-annotated

<<Service>>
  CustomerService
  - Business logic
  - Transaction coordination
  - Service layer

<<DAO>>
  CustomerDao
  - Data access operations
  - Query construction
  - Persistence abstraction

<<Utility>>
  LegacyJdoManager
  - Transaction primitives
  - Stateless
  - Infrastructure

<<Utility>>
  LegacyQueries
  - Query builders
  - Static methods
  - ⚠️ Security issue
```

---

## Class Complexity Analysis

```
Complexity Map (by lines of code and cyclomatic complexity):

       High Complexity
            │
            │
    Medium  │  CustomerService (21 LOC, CC=2)
            │
            │
    Low     │  Customer (20 LOC, CC=1)
            │  CustomerDao (16 LOC, CC=1)
            │
    Very Low│  LegacyQueries (7 LOC, CC=1)
            │  LegacyJdoManager (5 LOC, CC=1)
            │
            └──────────────────────────────────>
                        Lines of Code
```

---

## Class Modification History (Technical Debt Context)

```
Customer
  └─ Created: Initial version with JDO annotations
  └─ Status: ⚠️ Needs JPA migration

CustomerDao
  └─ Created: Initial version
  └─ Status: ⚠️ Uses vulnerable query construction

CustomerService
  └─ Created: Initial version with manual transactions
  └─ Status: ⚠️ Needs declarative transactions

LegacyJdoManager
  └─ Created: JDO wrapper (stub implementation)
  └─ Status: 🔴 To be removed (replace with Spring)

LegacyQueries
  └─ Created: Query utility
  └─ Status: 🔴 CRITICAL - SQL injection vulnerability
```

---

## Related Documentation

- [Program Structure](../reference/program-structure.md) - Detailed class documentation
- [Components](../architecture/components.md) - Component descriptions
- [Patterns](../architecture/patterns.md) - Design patterns
- [Dependencies](../architecture/dependencies.md) - Dependency details

---

*Last Updated: January 2026*  
*Total Classes: 7 (5 main + 2 test)*  
*Diagram Format: Text-based ASCII art*  
*Notation: UML-inspired*
