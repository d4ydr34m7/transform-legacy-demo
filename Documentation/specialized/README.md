# Specialized Documentation

## Overview

This directory contains technology-specific and domain-specific documentation for the transform-legacy-demo project. Specialized documentation provides deep-dive details on specific technologies, frameworks, and domain patterns used in the codebase.

---

## Directory Structure

```
specialized/
├── README.md               (this file)
├── jdo/                    [JDO Technology]
│   └── jdo-patterns.md
└── gradle/                 [Build System]
    └── build-system.md
```

---

## Technology-Specific Documentation

### 1. JDO (Java Data Objects)

**Directory**: [jdo/](jdo/)  
**Primary Document**: [jdo-patterns.md](jdo/jdo-patterns.md)

**Coverage**:
- JDO transaction patterns
- JDO query construction
- JDO entity configuration
- JDO to JPA migration guide
- Security vulnerabilities in JDO usage
- Technical debt assessment

**Key Findings**:
- 🔴 Deprecated technology (since 2013)
- 🔴 SQL injection vulnerability in query construction
- 🔴 Missing configuration and proper setup
- Recommended action: Migrate to JPA

---

### 2. Gradle Build System

**Directory**: [gradle/](gradle/)  
**Primary Document**: [build-system.md](gradle/build-system.md)

**Coverage**:
- Multi-module project structure
- Build configuration details
- Dependency management
- Build tasks and lifecycle
- Testing configuration with JUnit 5
- Build optimization recommendations

**Key Findings**:
- ✅ Well-structured multi-module build
- ⚠️ Outdated dependencies
- Recommended improvements: Add code quality plugins

---

## Domain-Specific Documentation

### Customer Management Domain

**Status**: Simple domain, covered in core documentation

**Related Documents**:
- [Business Logic](../behavior/business-logic.md) - Domain rules
- [Data Models](../reference/data-models.md) - Domain entities
- [Decision Logic](../behavior/decision-logic.md) - Domain decisions

**Domain Concepts**:
- Customer entity (ID, Name)
- Customer display formatting
- Customer lookup operations

**Assessment**: Domain is straightforward with minimal business complexity. Dedicated domain-specific documentation not required for this codebase size.

---

## Navigation Guide

### For Technology Migration

**If migrating from JDO**:
1. Read [JDO Patterns](jdo/jdo-patterns.md)
2. Review [Modernization Options](../migration/modernization-options.md)
3. Check [Security Vulnerabilities](../technical-debt/security-vulnerabilities.md)
4. Follow [Component Migration Order](../migration/component-order.md)

**If updating build system**:
1. Read [Gradle Build System](gradle/build-system.md)
2. Review [Dependencies](../architecture/dependencies.md)
3. Check [Test Specifications](../migration/test-specifications.md)

---

### For Understanding Technology Patterns

**JDO Transaction Management**:
- [JDO Patterns](jdo/jdo-patterns.md) → Transaction patterns section
- [Workflows](../behavior/workflows.md) → Transaction lifecycle
- [Error Handling](../behavior/error-handling.md) → Rollback patterns

**Gradle Build Process**:
- [Build System](gradle/build-system.md) → Build lifecycle
- [Program Structure](../reference/program-structure.md) → Module organization
- [Dependency Analysis](../analysis/dependency-analysis.md) → Dependency tree

---

## When to Add Specialized Documentation

Add new specialized documentation when:

1. **Technology Detection Threshold**:
   - Multiple files using the technology (5+ files)
   - Complex patterns specific to the technology
   - Migration guides needed
   - Security considerations specific to technology

2. **Domain Complexity Threshold**:
   - 10+ business rules in single domain
   - Complex domain calculations
   - Domain-specific workflows
   - Industry-specific patterns (e.g., financial, healthcare)

3. **Current State**:
   - JDO: ✅ Warranted (deprecated tech, migration needed)
   - Gradle: ✅ Warranted (multi-module, build guidance)
   - Customer Domain: ❌ Not warranted (simple CRUD)

---

## Specialized Documentation Standards

### Required Sections

Each technology-specific document should include:
1. **Overview** - Technology summary
2. **Usage in Codebase** - Where/how used
3. **Patterns** - Implementation patterns found
4. **Configuration** - Setup and config details
5. **Issues** - Problems, vulnerabilities, debt
6. **Recommendations** - Improvements and alternatives
7. **Migration Guide** - If applicable
8. **Related Documentation** - Cross-references

---

## Related Core Documentation

### Architecture
- [System Overview](../architecture/system-overview.md)
- [Components](../architecture/components.md)
- [Dependencies](../architecture/dependencies.md)

### Technical Debt
- [Outdated Components](../technical-debt/outdated-components.md)
- [Security Vulnerabilities](../technical-debt/security-vulnerabilities.md)
- [Technical Debt Report](../technical-debt-report.md)

### Migration
- [Modernization Options](../migration/modernization-options.md)
- [Component Order](../migration/component-order.md)
- [Effort Estimate](../migration/effort-estimate.md)

---

## Quick Reference

| Technology | Document | Status | Priority |
|-----------|----------|--------|----------|
| JDO 3.1 | [jdo-patterns.md](jdo/jdo-patterns.md) | 🔴 Deprecated | High - Migrate |
| Gradle 7.x | [build-system.md](gradle/build-system.md) | ✅ Active | Medium - Update deps |
| JUnit 5 | See [Test Specs](../migration/test-specifications.md) | ✅ Active | Low - Update version |

---

*Last Updated: January 2026*  
*Specialized Topics: 2*  
*Technology Coverage: JDO, Gradle*
