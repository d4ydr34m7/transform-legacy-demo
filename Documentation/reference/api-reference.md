# API Reference

## Overview

This document serves as the consolidated API reference for the transform-legacy-demo codebase. For detailed API documentation, please refer to [interfaces.md](interfaces.md) which provides comprehensive documentation of all public interfaces, methods, and APIs.

---

## Quick Reference

**Primary API Documentation**: [interfaces.md](interfaces.md)

---

## Public API Summary

**Total Public Classes**: 5  
**Total Public Methods**: 10  
**Total Public Static Methods**: 1

---

## API Categories

### 1. Entity API
- **Customer**: Domain entity representing a customer
  - Constructor: `Customer(String id, String name)`
  - Methods: `getId()`, `getName()`

### 2. Data Access API
- **CustomerDao**: Data access object for customer operations
  - Methods: `buildFindByIdQuery(String id)`

### 3. Service API
- **CustomerService**: Business service for customer operations
  - Constructor: `CustomerService(LegacyJdoManager jdo)`
  - Methods: `formatDisplay(Customer c)`

### 4. Persistence Management API
- **LegacyJdoManager**: Transaction and persistence manager
  - Methods: `begin()`, `commit()`, `rollback()`

### 5. Query Utility API
- **LegacyQueries**: Static query construction utilities
  - Static Methods: `byCustomerId(String id)`

---

## Complete API Documentation

For complete details including:
- Full method signatures
- Parameter descriptions
- Return types
- Usage examples
- Exceptions thrown
- Best practices
- Security considerations

**See**: [interfaces.md](interfaces.md)

---

## Related Documentation

- **[interfaces.md](interfaces.md)** - Complete public API documentation
- **[program-structure.md](program-structure.md)** - Class organization and structure
- **[data-models.md](data-models.md)** - Entity schemas and data types
- **[Sequence Diagrams](../diagrams/behavioral/sequence-diagrams.md)** - API interaction flows

---

*Last Updated: January 2026*  
*This document consolidates API reference - see interfaces.md for complete details*
