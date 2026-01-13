# Dependency Graph - Structural Diagrams

## Overview

This document provides text-based visual representations of the dependency structure in the transform-legacy-demo system, including module dependencies, external library dependencies, and component relationships.

---

## Module Dependency Graph

### High-Level Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                     ROOT PROJECT                        │
│              (transform-legacy-demo)                    │
│                                                         │
│  Configuration:                                         │
│  • Gradle 8.5                                          │
│  • Java 11 toolchain                                   │
│  • Maven Central repository                            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ contains
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
┌─────────────────┐  ┌─────────────────┐
│   legacy-app    │  │ legacy-wrappers │
│                 │  │                 │
│  Application    │  │  Infrastructure │
│  Layer          │  │  Layer          │
└────────┬────────┘  └─────────────────┘
         │                   ▲
         │                   │
         │  implementation   │
         │   dependency      │
         └───────────────────┘
```

### Detailed Module Dependency Flow

```
Direction: Top (Dependent) → Bottom (Dependency)

┌──────────────────────────────────────────┐
│           legacy-app module              │
│                                          │
│  Package: com.verafin.legacy             │
│  Classes: Customer, CustomerDao,         │
│           CustomerService                │
│  Tests: CustomerDaoTest,                 │
│         CustomerServiceTest              │
└──────────────────┬───────────────────────┘
                   │
                   │ Runtime: Uses classes from legacy-wrappers
                   │ Build: Compiles against legacy-wrappers
                   │
                   ▼
┌──────────────────────────────────────────┐
│       legacy-wrappers module             │
│                                          │
│  Package: com.verafin.commons.jdo        │
│  Classes: LegacyJdoManager,              │
│           LegacyQueries                  │
│  Tests: (if any)                         │
└──────────────────────────────────────────┘
                   │
                   │ No further module dependencies
                   │
                   ▼
              (Terminal Node)
```

---

## External Dependency Graph

### Complete External Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                  ROOT PROJECT                           │
│           (All Subprojects Inherit)                     │
│                                                         │
│  Repository: Maven Central                              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ configured for all subprojects
                        │
        ┌───────────────┴──────────────┐
        │                              │
        ▼                              ▼
┌────────────────────┐      ┌────────────────────┐
│    legacy-app      │      │  legacy-wrappers   │
└────────┬───────────┘      └─────────┬──────────┘
         │                             │
         │                             │
         ├─────────────────────────────┤
         │                             │
         │     testImplementation      │
         │    (both modules share)     │
         │                             │
         ▼                             ▼
┌──────────────────────────────────────────────┐
│      org.junit.jupiter:junit-jupiter         │
│               Version: 5.10.2                │
│                                              │
│  Transitive Dependencies:                   │
│  ├─ junit-jupiter-api:5.10.2               │
│  ├─ junit-jupiter-engine:5.10.2            │
│  ├─ junit-jupiter-params:5.10.2            │
│  └─ junit-platform-* (various)             │
└──────────────────────────────────────────────┘

         │ (legacy-app only)
         │ implementation
         ▼
┌──────────────────────────────────────────────┐
│         javax.jdo:jdo-api                    │
│            Version: 3.1                      │
│          Released: 2013                      │
│                                              │
│  ⚠️  DEPRECATED TECHNOLOGY                   │
│                                              │
│  Minimal Transitive Dependencies:           │
│  └─ (API-only JAR, few dependencies)        │
└──────────────────────────────────────────────┘
```

---

## Component-Level Dependency Graph

### Class Dependencies

```
┌────────────────────────────────────────────────────────┐
│                  EXTERNAL LIBRARIES                    │
│                                                        │
│  ┌──────────────────┐      ┌──────────────────┐      │
│  │ javax.jdo.*      │      │ org.junit.*      │      │
│  │ annotations      │      │ (test scope)     │      │
│  └────────┬─────────┘      └────────┬─────────┘      │
└───────────┼──────────────────────────┼────────────────┘
            │                          │
            │ annotates                │ tests
            │                          │
┌───────────▼──────────────────────────▼────────────────┐
│              legacy-app MODULE                        │
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │           Customer (Entity)                 │    │
│  │  @PersistenceCapable, @PrimaryKey          │    │
│  └──────────────────┬──────────────────────────┘    │
│                     │                                │
│                     │ used by                        │
│                     │                                │
│  ┌──────────────────▼──────────────────────────┐    │
│  │         CustomerDao                         │    │
│  │    (Data Access Object)                     │    │
│  └──────────────────┬──────────────────────────┘    │
│                     │                                │
│                     │ used by                        │
│                     │                                │
│  ┌──────────────────▼──────────────────────────┐    │
│  │      CustomerService                        │    │
│  │    (Service Layer)                          │    │
│  └──────────────────┬──────────────────────────┘    │
│                     │                                │
└─────────────────────┼────────────────────────────────┘
                      │
                      │ uses utilities from
                      │
┌─────────────────────▼────────────────────────────────┐
│           legacy-wrappers MODULE                     │
│                                                      │
│  ┌───────────────────────┐  ┌──────────────────┐   │
│  │  LegacyJdoManager     │  │  LegacyQueries   │   │
│  │  (Transaction Mgmt)   │  │  (Query Builder) │   │
│  └───────────────────────┘  └──────────────────┘   │
│            ▲                         ▲              │
│            │                         │              │
│            │ used by                 │ used by      │
│            │                         │              │
│      CustomerService          CustomerDao           │
└──────────────────────────────────────────────────────┘
```

### Detailed Component Interaction

```
CustomerService
    │
    ├─→ depends on: LegacyJdoManager
    │   │
    │   └─→ calls: begin(), commit(), rollback()
    │
    ├─→ depends on: CustomerDao
    │   │
    │   └─→ calls: byId(String)
    │
    └─→ depends on: Customer (domain model)


CustomerDao
    │
    ├─→ depends on: LegacyQueries
    │   │
    │   └─→ calls: byCustomerId(String)
    │
    └─→ returns: Customer instance


Customer (Entity)
    │
    ├─→ annotated by: @PersistenceCapable (javax.jdo)
    │
    └─→ annotated by: @PrimaryKey (javax.jdo)


LegacyJdoManager
    │
    └─→ provides: Transaction management primitives


LegacyQueries
    │
    └─→ provides: Query string construction utilities
```

---

## Dependency Layers

### Layered Dependency View

```
┌────────────────────────────────────────────────────┐
│  Layer 4: TEST FRAMEWORK                           │
│  ┌──────────────────────────────────────────────┐ │
│  │  JUnit Jupiter 5.10.2                        │ │
│  │  (Test scope only)                           │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
                         │ tests
                         │
┌────────────────────────▼───────────────────────────┐
│  Layer 3: APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────┐ │
│  │  legacy-app module                           │ │
│  │  • Customer                                  │ │
│  │  • CustomerDao                               │ │
│  │  • CustomerService                           │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────┘
                         │ depends on
                         │
┌────────────────────────▼───────────────────────────┐
│  Layer 2: INFRASTRUCTURE LAYER                     │
│  ┌──────────────────────────────────────────────┐ │
│  │  legacy-wrappers module                      │ │
│  │  • LegacyJdoManager                          │ │
│  │  • LegacyQueries                             │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────┘
                         │ depends on
                         │
┌────────────────────────▼───────────────────────────┐
│  Layer 1: EXTERNAL LIBRARIES                       │
│  ┌──────────────────────────────────────────────┐ │
│  │  JDO API 3.1 (javax.jdo:jdo-api)            │ │
│  │  ⚠️  Deprecated/Legacy                       │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────┘
                         │ requires runtime
                         │
┌────────────────────────▼───────────────────────────┐
│  Layer 0: RUNTIME PLATFORM                         │
│  ┌──────────────────────────────────────────────┐ │
│  │  Java 11 Runtime (JVM)                       │ │
│  │  JDO Implementation (not declared)           │ │
│  │  Database (not declared)                     │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

---

## Build Dependency Graph

### Gradle Build Dependencies

```
Root build.gradle
    │
    ├─→ Configures: allprojects { repositories { mavenCentral() } }
    │
    └─→ Configures: subprojects {
            java plugin
            java.toolchain { languageVersion = 11 }
            testImplementation: junit-jupiter:5.10.2
        }
        │
        ├────────────────────────────┐
        │                            │
        ▼                            ▼
legacy-app/build.gradle    legacy-wrappers/build.gradle
    │                            │
    ├─→ implementation: project(":legacy-wrappers")
    │                            │
    ├─→ implementation: javax.jdo:jdo-api:3.1
    │                            │
    └─→ inherits: JUnit from parent
                                 │
                                 └─→ dependencies { }
                                     (intentionally empty)
```

---

## Dependency Risk Matrix

### Module Dependency Risk

```
┌──────────────────┬─────────────┬──────────┬──────────┐
│ From Module      │ To Module   │ Type     │ Risk     │
├──────────────────┼─────────────┼──────────┼──────────┤
│ legacy-app       │ legacy-     │ Inter-   │ Low      │
│                  │ wrappers    │ module   │          │
│                  │             │          │          │
│ Rationale: Clean module boundary, can be replaced   │
└──────────────────────────────────────────────────────┘
```

### External Dependency Risk

```
┌─────────────────┬───────┬────────┬──────────────┐
│ Dependency      │ Ver   │ Age    │ Risk         │
├─────────────────┼───────┼────────┼──────────────┤
│ JDO API         │ 3.1   │ ~11y   │ 🔴 CRITICAL  │
│ JUnit Jupiter   │ 5.10  │ <1y    │ ✅ LOW       │
│ Gradle          │ 8.5   │ <1y    │ ✅ LOW       │
│ Java            │ 11    │ ~6y    │ 🟡 MEDIUM    │
└─────────────────┴───────┴────────┴──────────────┘

Legend:
🔴 CRITICAL - Requires immediate attention
🟡 MEDIUM   - Should plan upgrade
✅ LOW      - Acceptable, maintain updates
```

---

## Transitive Dependency Graph

### JUnit Jupiter Transitive Dependencies

```
org.junit.jupiter:junit-jupiter:5.10.2 (aggregate)
    │
    ├─→ org.junit.jupiter:junit-jupiter-api:5.10.2
    │       │
    │       └─→ org.opentest4j:opentest4j:1.3.0
    │       └─→ org.junit.platform:junit-platform-commons:1.10.2
    │
    ├─→ org.junit.jupiter:junit-jupiter-params:5.10.2
    │       │
    │       └─→ (depends on junit-jupiter-api)
    │
    └─→ org.junit.jupiter:junit-jupiter-engine:5.10.2
            │
            └─→ org.junit.platform:junit-platform-engine:1.10.2
                    │
                    └─→ org.junit.platform:junit-platform-commons:1.10.2
```

### JDO API Transitive Dependencies

```
javax.jdo:jdo-api:3.1
    │
    └─→ (minimal transitive dependencies - API specification only)
```

**Note**: A JDO implementation (e.g., DataNucleus) would be required at runtime but is not declared in the build.

---

## Package Dependency Graph

### Package-Level Dependencies

```
┌─────────────────────────────────────────────────────┐
│  com.verafin.legacy (legacy-app)                    │
│                                                     │
│  ┌──────────┐  ┌─────────────┐  ┌───────────────┐ │
│  │ Customer │  │ CustomerDao │  │ CustomerService│ │
│  └────┬─────┘  └──────┬──────┘  └───────┬────────┘ │
└───────┼────────────────┼──────────────────┼─────────┘
        │                │                  │
        │                │                  │
        │ imports        │ imports          │ imports
        │                │                  │
        ▼                ▼                  ▼
┌─────────────────────────────────────────────────────┐
│  com.verafin.commons.jdo (legacy-wrappers)          │
│                                                     │
│  ┌────────────────────┐  ┌──────────────────────┐  │
│  │ LegacyJdoManager   │  │ LegacyQueries        │  │
│  └────────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Circular Dependency Analysis

### Result: No Circular Dependencies Detected ✅

The dependency graph is **acyclic** (DAG - Directed Acyclic Graph):

```
Dependency Chain (all valid, no cycles):

legacy-app → legacy-wrappers → (none)

✅ No module depends on legacy-app
✅ legacy-wrappers has no dependencies
✅ Clean, unidirectional dependency flow
```

**Benefit**: 
- Easy to understand
- Safe to refactor
- Clear build order
- No complex dependency resolution

---

## Dependency Update Path

### Safe Update Sequence

To update dependencies without breaking changes:

```
1. Update Gradle wrapper (build tool)
   └─→ Test build

2. Update JUnit Jupiter (test framework)
   └─→ Run tests

3. Consider Java upgrade (11 → 17/21)
   └─→ Full regression testing

4. Plan JDO replacement (requires code changes)
   └─→ Major refactoring effort
```

---

## Dependency Isolation

### Module Dependency Isolation

```
┌────────────────────────────────────┐
│  Module: legacy-app                │
│                                    │
│  CAN access:                       │
│  ✅ All classes in legacy-wrappers │
│  ✅ JDO API classes                │
│  ✅ JUnit (test scope)             │
│                                    │
│  CANNOT access:                    │
│  ❌ Private classes in wrappers    │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  Module: legacy-wrappers           │
│                                    │
│  CAN access:                       │
│  ✅ JUnit (test scope)             │
│                                    │
│  CANNOT access:                    │
│  ❌ Any classes in legacy-app      │
│  ❌ JDO API (not declared)         │
└────────────────────────────────────┘
```

---

## Related Documentation

### Internal Links
- [Dependencies](../architecture/dependencies.md) - Detailed dependency analysis
- [Components](../architecture/components.md) - Component descriptions
- [System Overview](../architecture/system-overview.md) - Architecture context
- [Technical Debt - Outdated Components](../technical-debt/outdated-components.md) - Dependency risks

---

*Last Updated: January 2026*  
*Analysis Method: Static analysis of build.gradle files and import statements*  
*Diagram Format: Text-based ASCII diagrams for universal readability*
