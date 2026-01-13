# Sequence Diagrams - Behavioral Documentation

## Overview

Text-based sequence diagrams showing component interactions for key operations in the transform-legacy-demo system.

---

## Sequence Diagram 1: Customer Display Formatting

### Operation: formatDisplay(Customer)

```
Actor: Test/Client
Objects: CustomerService, LegacyJdoManager, Customer

Test/Client    CustomerService    LegacyJdoManager    Customer
     │                │                  │                │
     │ formatDisplay()│                  │                │
     ├───────────────>│                  │                │
     │                │                  │                │
     │                │ begin()          │                │
     │                ├─────────────────>│                │
     │                │                  │                │
     │                │ getId()          │                │
     │                ├──────────────────────────────────>│
     │                │<───────────────────────────────────┤
     │                │ "1"              │                │
     │                │                  │                │
     │                │ getName()        │                │
     │                ├──────────────────────────────────>│
     │                │<───────────────────────────────────┤
     │                │ "Shreya"         │                │
     │                │                  │                │
     │                │ [Format: "1:Shreya"]              │
     │                │                  │                │
     │                │ commit()         │                │
     │                ├─────────────────>│                │
     │                │                  │                │
     │<───────────────┤                  │                │
     │ "1:Shreya"     │                  │                │
```

**Duration**: < 1ms  
**Transaction**: Yes (begin → commit)  
**Error Handling**: Rollback on exception

---

## Sequence Diagram 2: Query Construction

### Operation: buildFindByIdQuery(String)

```
Test/Client    CustomerDao    LegacyQueries
     │              │               │
     │ buildFindByIdQuery("123")    │
     ├─────────────>│               │
     │              │               │
     │              │ byCustomerId("123")
     │              ├──────────────>│
     │              │               │
     │              │               │ [Construct Query]
     │              │               │ "SELECT FROM ... WHERE id == '123'"
     │              │<──────────────┤
     │              │ query string  │
     │<─────────────┤               │
     │ query string │               │
```

**Duration**: < 1ms  
**Transaction**: No  
**Error Handling**: None

---

## Sequence Diagram 3: Error Scenario - Null Customer

### Operation: formatDisplay(null)

```
Test/Client    CustomerService    LegacyJdoManager
     │                │                  │
     │ formatDisplay(null)               │
     ├───────────────>│                  │
     │                │                  │
     │                │ begin()          │
     │                ├─────────────────>│
     │                │                  │
     │                │ getId()          │
     │                │ on null          │
     │                ├──X               │
     │                │ NullPointerException
     │                │                  │
     │                │ rollback()       │
     │                ├─────────────────>│
     │                │                  │
     │<───────X───────┤                  │
     │ NullPointerException              │
```

**Result**: Transaction rolled back, exception propagated

---

## Sequence Diagram 4: Complete Test Scenario

### Test: CustomerServiceTest.formatsDisplay()

```
JUnit          CustomerServiceTest    CustomerService    LegacyJdoManager    Customer
  │                     │                   │                  │                │
  │ @Test formatsDisplay()                  │                  │                │
  ├────────────────────>│                   │                  │                │
  │                     │                   │                  │                │
  │                     │ new LegacyJdoManager()               │                │
  │                     ├──────────────────────────────────────>│                │
  │                     │<────────────────────────────────────┤                 │
  │                     │                   │                  │                │
  │                     │ new CustomerService(jdo)             │                │
  │                     ├──────────────────>│                  │                │
  │                     │<─────────────────┤                   │                │
  │                     │                   │                  │                │
  │                     │ new Customer("1", "Shreya")          │                │
  │                     ├──────────────────────────────────────────────────────>│
  │                     │<────────────────────────────────────────────────────┤ │
  │                     │                   │                  │                │
  │                     │ formatDisplay(customer)              │                │
  │                     ├──────────────────>│                  │                │
  │                     │                   │ begin()          │                │
  │                     │                   ├─────────────────>│                │
  │                     │                   │ getId()          │                │
  │                     │                   ├──────────────────────────────────>│
  │                     │                   │<───────────────────────────────────┤
  │                     │                   │ getName()        │                │
  │                     │                   ├──────────────────────────────────>│
  │                     │                   │<───────────────────────────────────┤
  │                     │                   │ commit()         │                │
  │                     │                   ├─────────────────>│                │
  │                     │<─────────────────┤                   │                │
  │                     │ "1:Shreya"        │                  │                │
  │                     │                   │                  │                │
  │                     │ assertEquals("1:Shreya", result)     │                │
  │<────────────────────┤                   │                  │                │
  │ Test PASSED         │                   │                  │                │
```

---

## Timing Diagram

```
Time →

t=0ms    CustomerService.formatDisplay() called
         │
t=0.1ms  └─→ jdo.begin()
             │
t=0.2ms      └─→ c.getId()
                 │
t=0.3ms          └─→ c.getName()
                     │
t=0.4ms              └─→ Format string
                         │
t=0.5ms                  └─→ jdo.commit()
                             │
t=0.6ms                      └─→ return result

Total: ~0.6ms (stub implementation, no actual database)
```

---

## Interaction Patterns

### Pattern 1: Transaction Wrapper

```
Service
  ├─→ Begin Transaction
  ├─→ Execute Business Logic
  │   └─→ Call Domain Objects
  ├─→ Commit Transaction
  └─→ Return Result

On Error:
  ├─→ Rollback Transaction
  └─→ Throw Exception
```

### Pattern 2: Query Delegation

```
DAO
  └─→ Delegate to Query Utility
      └─→ Return Query String
```

---

## Related Documentation

- [Business Logic](../behavior/business-logic.md)
- [Workflows](../behavior/workflows.md)
- [Error Handling](../behavior/error-handling.md)
- [Transaction Flow](../diagrams/data-flow/transaction-flow.md)

---

*Last Updated: January 2026*  
*Diagram Format: Text-based ASCII*  
*Sequence Diagrams: 4*
