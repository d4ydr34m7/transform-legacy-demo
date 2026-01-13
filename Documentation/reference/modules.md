# Modules - Program Structure Reference

## Overview

This document serves as the module-level documentation for the transform-legacy-demo codebase. For complete structural documentation including class-level details, please refer to [program-structure.md](program-structure.md).

---

## Quick Reference

**Primary Module Documentation**: [program-structure.md](program-structure.md)

---

## Module Architecture

The transform-legacy-demo project is organized into 2 primary modules:

```
transform-legacy-demo/
├── legacy-app/          [Application Module]
└── legacy-wrappers/     [Persistence Wrapper Module]
```

---

## Module 1: legacy-app

### Module Information

**Name**: legacy-app  
**Type**: Application Module  
**Purpose**: Core customer management application  
**Language**: Java 11

### Module Contents

**Packages**: 1  
- `com.verafin.legacy`

**Classes**: 3
- `Customer` - Domain entity
- `CustomerDao` - Data access layer
- `CustomerService` - Business service layer

**Test Classes**: 2
- `CustomerDaoTest`
- `CustomerServiceTest`

**Total LOC**: ~80 lines

### Module Dependencies

**Internal Dependencies**:
- `legacy-wrappers` (persistence utilities)

**External Dependencies**:
- JDO API 3.1
- JUnit 5 (testing)

### Module Responsibility

The legacy-app module provides:
- Customer entity definition
- Customer data access operations
- Customer business logic
- Customer service orchestration

---

## Module 2: legacy-wrappers

### Module Information

**Name**: legacy-wrappers  
**Type**: Persistence Wrapper Module  
**Purpose**: JDO persistence abstraction layer  
**Language**: Java 11

### Module Contents

**Packages**: 1
- `com.verafin.commons.jdo`

**Classes**: 2
- `LegacyJdoManager` - Transaction management
- `LegacyQueries` - Query construction utilities

**Test Classes**: 0

**Total LOC**: ~12 lines

### Module Dependencies

**Internal Dependencies**: None (foundation module)

**External Dependencies**:
- JDO API 3.1

### Module Responsibility

The legacy-wrappers module provides:
- Transaction lifecycle management
- JDO query construction utilities
- Persistence abstraction

---

## Inter-Module Dependencies

```
legacy-app
    │
    └─→ depends on
            │
            ▼
    legacy-wrappers
```

### Dependency Details

**legacy-app → legacy-wrappers**:
- `CustomerService` uses `LegacyJdoManager` for transaction management
- `CustomerDao` uses `LegacyQueries` for query construction

**Dependency Type**: Compile-time dependency  
**Coupling**: Medium (shared JDO abstractions)

---

## Module Dependency Graph

```
┌─────────────────────┐
│    legacy-app       │
│                     │
│  - Customer         │
│  - CustomerDao      │
│  - CustomerService  │
└──────────┬──────────┘
           │ uses
           │
           ▼
┌─────────────────────┐
│  legacy-wrappers    │
│                     │
│  - LegacyJdoManager │
│  - LegacyQueries    │
└─────────────────────┘
           │ uses
           │
           ▼
   ┌───────────────┐
   │   JDO API     │
   │   (External)  │
   └───────────────┘
```

---

## Module Build Configuration

### Module: legacy-app

**Build Tool**: Gradle  
**Source Path**: `src/main/java`  
**Test Path**: `src/test/java`

**Dependencies**:
```gradle
dependencies {
    implementation project(':legacy-wrappers')
    implementation 'javax.jdo:jdo-api:3.1'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.8.1'
}
```

### Module: legacy-wrappers

**Build Tool**: Gradle  
**Source Path**: `src/main/java`  
**Test Path**: None

**Dependencies**:
```gradle
dependencies {
    implementation 'javax.jdo:jdo-api:3.1'
}
```

---

## Module Metrics

| Module | Classes | LOC | Test Coverage | Complexity |
|--------|---------|-----|---------------|------------|
| legacy-app | 3 | ~80 | High (2 test classes) | Low |
| legacy-wrappers | 2 | ~12 | None | Very Low |
| **Total** | **5** | **~92** | **Partial** | **Low** |

---

## Module Evolution Recommendations

### Phase 1: Decouple Modules

**Goal**: Reduce coupling between legacy-app and legacy-wrappers

**Actions**:
- Define interface-based contracts
- Remove direct class dependencies
- Use dependency injection

### Phase 2: Modernize Persistence Module

**Goal**: Replace legacy-wrappers with modern persistence

**Actions**:
- Migrate from JDO to JPA
- Create new persistence module
- Gradually migrate legacy-app

### Phase 3: Microservices Architecture

**Goal**: Split monolith into services

**Actions**:
- Extract customer service as REST API
- Separate persistence layer
- Add service discovery

---

## Module Testing Strategy

### legacy-app Testing

**Test Classes**: 2  
**Test Coverage**: ~80%  
**Test Types**: Unit tests

**Test Execution**:
```bash
./gradlew :legacy-app:test
```

### legacy-wrappers Testing

**Test Classes**: 0  
**Test Coverage**: 0%  
**Recommendation**: Add unit tests for transaction and query utilities

**Suggested Tests**:
- Transaction lifecycle tests
- Query construction validation
- Error handling tests

---

## Module Migration Order

Based on dependency analysis, recommended migration order:

1. **Phase 1**: legacy-wrappers (foundation)
   - Migrate JDO to JPA
   - No upstream dependencies

2. **Phase 2**: legacy-app (dependent)
   - Update to use new persistence layer
   - Depends on Phase 1 completion

---

## Complete Module Documentation

For detailed module documentation including:
- Complete class inventories
- Line-by-line code structure
- Method implementations
- Inheritance hierarchies
- Package organization
- File locations

**See**: [program-structure.md](program-structure.md)

---

## Related Documentation

- **[program-structure.md](program-structure.md)** - Complete structural documentation
- **[dependencies.md](../architecture/dependencies.md)** - Dependency analysis
- **[Component Order](../migration/component-order.md)** - Migration sequence
- **[Class Diagram](../diagrams/structural/class-diagram.md)** - Visual structure

---

*Last Updated: January 2026*  
*Modules: 2*  
*This document provides module overview - see program-structure.md for complete details*
