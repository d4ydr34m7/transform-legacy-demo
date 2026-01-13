# Component Migration Order

## Overview

This document defines the recommended order for migrating components from the legacy JDO-based architecture to a modern JPA-based architecture.

---

## Migration Strategy: Bottom-Up Approach

**Rationale**: Migrate foundation layers first to avoid breaking dependencies

**Order**: Infrastructure → Data Access → Service → Application

---

## Phase 1: Infrastructure Layer (legacy-wrappers module)

### Priority: 🔴 CRITICAL  
### Duration: 2-3 weeks  
### Effort: 24-36 hours

#### Components to Migrate

1. **LegacyJdoManager** → **Spring @Transactional**
   - Remove manual transaction management
   - Configure Spring transaction management
   - Set up EntityManager
   - **Effort**: 8-12 hours

2. **LegacyQueries** → **JPA Criteria API / JPQL**
   - Replace string concatenation with parameterized queries
   - Implement type-safe query construction
   - Fix SQL injection vulnerability
   - **Effort**: 8-12 hours

3. **Module Configuration**
   - Add JPA dependencies
   - Remove JDO dependencies
   - Configure persistence.xml or Spring Data JPA
   - **Effort**: 4-6 hours

4. **Testing**
   - Unit test new transaction management
   - Verify query construction
   - **Effort**: 4-6 hours

### Dependencies

**Prerequisites**: None (foundation layer)  
**Blocks**: Phase 2 (data access layer depends on this)

---

## Phase 2: Domain & Data Access Layer (legacy-app module - Part 1)

### Priority: 🔴 CRITICAL  
### Duration: 2-3 weeks  
### Effort: 20-30 hours

#### Components to Migrate

1. **Customer Entity** → **JPA Entity**
   - Replace `@PersistenceCapable` with `@Entity`
   - Replace `@PrimaryKey` with `@Id`
   - Add `@Column` annotations
   - Add validation annotations
   - **Effort**: 2-4 hours

2. **CustomerDao** → **CustomerRepository (Spring Data JPA)**
   - Replace DAO with Repository interface
   - Remove manual query construction
   - Leverage Spring Data JPA auto-implementation
   - **Effort**: 4-6 hours

3. **Add Missing Methods**
   - Implement equals() and hashCode()
   - Implement toString()
   - **Effort**: 2-3 hours

4. **Testing**
   - Update unit tests for JPA
   - Integration tests with JPA
   - **Effort**: 8-12 hours

5. **Documentation**
   - Update code comments
   - Update API docs
   - **Effort**: 2-3 hours

### Dependencies

**Prerequisites**: Phase 1 complete (JPA infrastructure ready)  
**Blocks**: Phase 3 (service layer depends on data access)

---

## Phase 3: Service Layer (legacy-app module - Part 2)

### Priority: 🟡 MEDIUM  
### Duration: 1-2 weeks  
### Effort: 12-18 hours

#### Components to Migrate

1. **CustomerService** → **@Transactional Service**
   - Remove manual transaction management
   - Add `@Transactional` annotation
   - Update to use CustomerRepository
   - Add input validation
   - **Effort**: 4-6 hours

2. **Error Handling**
   - Implement custom exception hierarchy
   - Add proper logging
   - **Effort**: 4-6 hours

3. **Testing**
   - Update CustomerServiceTest
   - Add integration tests
   - **Effort**: 4-6 hours

### Dependencies

**Prerequisites**: Phase 2 complete (repository layer ready)  
**Blocks**: None (top of dependency chain)

---

## Phase 4: Cleanup and Optimization

### Priority: 🟢 LOW  
### Duration: 1 week  
### Effort: 8-12 hours

#### Activities

1. **Remove Legacy Code**
   - Delete LegacyJdoManager
   - Delete LegacyQueries
   - Remove JDO dependencies
   - **Effort**: 2-3 hours

2. **Code Quality**
   - Add dependency injection
   - Improve error messages
   - Add comprehensive logging
   - **Effort**: 4-6 hours

3. **Final Testing**
   - Full regression test suite
   - Performance testing
   - **Effort**: 2-3 hours

---

## Detailed Migration Sequence

### Step-by-Step Order

```
1. Setup JPA infrastructure
   └─→ Add dependencies, configure persistence

2. Migrate LegacyQueries → JPA Criteria API
   └─→ Fix SQL injection vulnerability

3. Setup Spring transaction management
   └─→ Replace LegacyJdoManager

4. Migrate Customer entity
   └─→ JDO annotations → JPA annotations

5. Migrate CustomerDao → CustomerRepository
   └─→ Use Spring Data JPA

6. Migrate CustomerService
   └─→ Remove manual transactions, add @Transactional

7. Update tests
   └─→ Adapt to JPA/Spring

8. Remove legacy code
   └─→ Delete JDO-specific classes

9. Final validation
   └─→ Comprehensive testing
```

---

## Module Migration Dependencies

```
┌─────────────────────────┐
│  legacy-wrappers        │  ← Migrate FIRST
│  (Infrastructure)       │
└───────────┬─────────────┘
            │
            │ Phase 1 Complete
            │
            ▼
┌─────────────────────────┐
│  legacy-app (Part 1)    │  ← Migrate SECOND
│  (Domain & DAO)         │
└───────────┬─────────────┘
            │
            │ Phase 2 Complete
            │
            ▼
┌─────────────────────────┐
│  legacy-app (Part 2)    │  ← Migrate THIRD
│  (Service Layer)        │
└─────────────────────────┘
```

---

## Risk Mitigation by Phase

### Phase 1 Risks

| Risk | Mitigation |
|------|------------|
| Transaction behavior changes | Thorough testing, behavior validation |
| Configuration errors | Use proven Spring Boot starters |
| Query performance | Benchmark before and after |

### Phase 2 Risks

| Risk | Mitigation |
|------|------------|
| Entity mapping differences | Review JPA vs JDO mapping carefully |
| Data loss | Backup before migration, test on copy |
| Query result differences | Compare results with legacy system |

### Phase 3 Risks

| Risk | Mitigation |
|------|------------|
| Service behavior changes | Comprehensive integration tests |
| Transaction scope issues | Review @Transactional propagation |

---

## Rollback Strategy by Phase

**Phase 1**: Keep JDO code in separate branch, can revert infrastructure  
**Phase 2**: Can revert entity changes, restore DAO layer  
**Phase 3**: Can revert to manual transactions if needed

---

## Success Criteria by Phase

### Phase 1
- ✅ JPA infrastructure operational
- ✅ Queries execute without SQL injection
- ✅ Transactions commit/rollback correctly

### Phase 2
- ✅ All entities mapped to JPA
- ✅ Repository methods work correctly
- ✅ No behavioral differences

### Phase 3
- ✅ Services use declarative transactions
- ✅ All tests pass
- ✅ Performance acceptable

---

## Timeline

```
Month 1:         Month 2:         Month 3:
├─────────────┼─────────────┼─────────────┤
│ Phase 1     │ Phase 2     │ Phase 3     │
│ Infrastructure│ Data Access │ Service     │
│ (2-3 weeks) │ (2-3 weeks) │ (1-2 weeks) │
└─────────────┴─────────────┴─────────────┘
                                    │
                                    └─→ Cleanup (1 week)
```

**Total Duration**: 2-3 months  
**Total Effort**: 64-96 hours

---

## Related Documentation

- [Modernization Options](modernization-options.md)
- [Effort Estimate](effort-estimate.md)
- [Risk Assessment](risk-assessment.md)
- [Remediation Plan](../technical-debt/remediation-plan.md)

---

*Last Updated: January 2026*  
*Migration Approach: Bottom-up*  
*Total Phases: 4*  
*Critical Path: Phase 1 → Phase 2 → Phase 3*
