# JDO Technology-Specific Documentation

## Overview

This document consolidates Java Data Objects (JDO) technology-specific patterns, usage, and considerations found in the transform-legacy-demo codebase.

---

## JDO Technology Summary

**Technology**: Java Data Objects (JDO) 3.1  
**Status**: ⚠️ Deprecated (since 2013)  
**Usage in Codebase**: Transaction management and query construction  
**Recommendation**: Migrate to JPA

---

## JDO Components in Codebase

### 1. LegacyJdoManager

**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyJdoManager.java`  
**Purpose**: Transaction lifecycle management

**JDO Methods Used**:
- `begin()` - Start transaction
- `commit()` - Commit transaction
- `rollback()` - Rollback transaction

**Implementation Pattern**: Stub implementation (no actual JDO PersistenceManager)

```java
public class LegacyJdoManager {
    public void begin() {
        // Stub - no actual JDO implementation
    }
    
    public void commit() {
        // Stub - no actual JDO implementation
    }
    
    public void rollback() {
        // Stub - no actual JDO implementation
    }
}
```

---

### 2. LegacyQueries

**File**: `legacy-wrappers/src/main/java/com/verafin/commons/jdo/LegacyQueries.java`  
**Purpose**: JDO query string construction

**JDO Query Language (JDOQL)**:
```java
"SELECT FROM com.verafin.legacy.Customer WHERE id == '{value}'"
```

**Pattern**: String concatenation (🔴 Security vulnerability)

---

## JDO Transaction Pattern

### Manual Transaction Management

The codebase uses explicit transaction boundaries:

```java
public String formatDisplay(Customer c) {
    jdo.begin();           // Start transaction
    try {
        // Business logic
        String out = c.getId() + ":" + c.getName();
        jdo.commit();      // Commit on success
        return out;
    } catch (RuntimeException e) {
        jdo.rollback();    // Rollback on error
        throw e;
    }
}
```

**Pattern**: Try-Catch-Rollback  
**Pros**: Explicit control  
**Cons**: Verbose, error-prone

---

## JDO Query Construction

### Current Approach: String Concatenation

```java
public static String byCustomerId(String id) {
    return "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";
}
```

**Issues**:
- 🔴 SQL injection vulnerability (CWE-89, CVSS 9.8)
- 🔴 No input validation
- 🔴 No parameterization

### Recommended Approach: Parameterized Queries

```java
// JDO parameterized query (secure)
public static Query byCustomerId(PersistenceManager pm, String id) {
    Query query = pm.newQuery(Customer.class);
    query.setFilter("id == :idParam");
    query.declareParameters("String idParam");
    return query;
}

// Usage
Query query = LegacyQueries.byCustomerId(pm, customerId);
List<Customer> results = (List<Customer>) query.execute(customerId);
```

---

## JDO Entity Annotations

### Current State: No JDO Annotations

The Customer entity has NO JDO annotations:

```java
public class Customer {
    private String id;
    private String name;
    // No @PersistenceCapable
    // No @PrimaryKey
    // No @Persistent
}
```

**Implication**: Entity not configured for actual JDO persistence

### Expected JDO Configuration

```java
import javax.jdo.annotations.*;

@PersistenceCapable(table="CUSTOMERS")
public class Customer {
    @PrimaryKey
    @Column(name="CUSTOMER_ID")
    private String id;
    
    @Persistent
    @Column(name="CUSTOMER_NAME")
    private String name;
    
    // Constructor, getters, setters
}
```

---

## JDO Configuration Requirements

### Required Configuration (Not Present)

**jdoconfig.xml**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jdoconfig xmlns="http://java.sun.com/xml/ns/jdo/jdoconfig">
    <persistence-manager-factory name="MyPMF">
        <property name="javax.jdo.PersistenceManagerFactoryClass" 
                  value="org.datanucleus.api.jdo.JDOPersistenceManagerFactory"/>
        <property name="javax.jdo.option.ConnectionURL" 
                  value="jdbc:h2:mem:testdb"/>
        <property name="javax.jdo.option.ConnectionDriverName" 
                  value="org.h2.Driver"/>
    </persistence-manager-factory>
</jdoconfig>
```

**Status**: ❌ Not configured (stub implementation only)

---

## JDO vs JPA Comparison

| Feature | JDO (Current) | JPA (Recommended) |
|---------|---------------|-------------------|
| Status | Deprecated (2013) | Active, industry standard |
| Community | Small, declining | Large, active |
| Documentation | Limited | Extensive |
| Framework Support | Minimal | Spring, Jakarta EE |
| Query Language | JDOQL | JPQL |
| Adoption | Very low | Very high |
| Security Tools | Limited | Many scanners support |

**Recommendation**: Migrate to JPA

---

## Migration Path: JDO → JPA

### Step 1: Update Entity Annotations

```java
// FROM: Plain Java class (no annotations)
public class Customer {
    private String id;
    private String name;
}

// TO: JPA entity
import javax.persistence.*;

@Entity
@Table(name = "customers")
public class Customer {
    @Id
    @Column(name = "id")
    private String id;
    
    @Column(name = "name")
    private String name;
}
```

### Step 2: Replace Transaction Manager

```java
// FROM: LegacyJdoManager
jdo.begin();
try {
    // work
    jdo.commit();
} catch (RuntimeException e) {
    jdo.rollback();
    throw e;
}

// TO: JPA EntityManager
EntityManager em = emf.createEntityManager();
EntityTransaction tx = em.getTransaction();
tx.begin();
try {
    // work
    tx.commit();
} catch (RuntimeException e) {
    tx.rollback();
    throw e;
} finally {
    em.close();
}
```

### Step 3: Convert Queries

```java
// FROM: JDO string queries
String query = "SELECT FROM com.verafin.legacy.Customer WHERE id == '" + id + "'";

// TO: JPA parameterized queries
TypedQuery<Customer> query = em.createQuery(
    "SELECT c FROM Customer c WHERE c.id = :id", 
    Customer.class
);
query.setParameter("id", id);
List<Customer> results = query.getResultList();
```

---

## JDO Technical Debt

### Critical Issues

1. **Deprecated Technology**: JDO deprecated since 2013
2. **Security Vulnerability**: String concatenation in queries (SQL injection)
3. **No Configuration**: Missing JDO config files
4. **Stub Implementation**: No actual persistence functionality

### Remediation Priority

1. 🔴 **Critical**: Fix SQL injection (immediate)
2. 🟡 **High**: Migrate to JPA (60-100 hours)
3. 🟢 **Medium**: Add proper configuration

---

## JDO Dependencies

**Current Dependency**:
```gradle
implementation 'javax.jdo:jdo-api:3.1'
```

**Last Updated**: 2013  
**Status**: No longer maintained  
**Vulnerabilities**: Check CVE databases

**Replacement** (JPA):
```gradle
implementation 'javax.persistence:javax.persistence-api:2.2'
implementation 'org.hibernate:hibernate-core:5.6.15.Final'
```

---

## JDO Resources

### Documentation
- [JDO Specification 3.1](https://db.apache.org/jdo/) (archived)
- [DataNucleus JDO Guide](https://www.datanucleus.org/products/accessplatform_6_0/jdo/)

### Migration Guides
- [JDO to JPA Migration Guide](https://www.datanucleus.org/products/accessplatform/jdo/jdo_to_jpa.html)

---

## Related Documentation

- **[Modernization Options](../migration/modernization-options.md)** - Migration strategies
- **[Outdated Components](../technical-debt/outdated-components.md)** - Technology debt analysis
- **[Security Vulnerabilities](../technical-debt/security-vulnerabilities.md)** - SQL injection details
- **[Program Structure](../reference/program-structure.md)** - Code organization
- **[Workflows](../behavior/workflows.md)** - Transaction patterns

---

*Last Updated: January 2026*  
*JDO Version: 3.1*  
*Status: Deprecated*  
*Recommendation: Migrate to JPA*
