# Gradle Build System Documentation

## Overview

This document provides Gradle build system specific information for the transform-legacy-demo project.

---

## Build System Summary

**Build Tool**: Gradle  
**Gradle Version**: 7.x (inferred from build files)  
**Java Version**: 11  
**Build Structure**: Multi-module project

---

## Project Structure

```
transform-legacy-demo/
├── build.gradle           (root build configuration)
├── settings.gradle        (project settings)
├── legacy-app/
│   └── build.gradle       (application module)
└── legacy-wrappers/
    └── build.gradle       (wrapper module)
```

---

## Root Build Configuration

### Project Configuration

```gradle
// Root build.gradle
plugins {
    id 'java'
}

allprojects {
    group = 'com.verafin'
    version = '1.0-SNAPSHOT'
}

subprojects {
    apply plugin: 'java'
    
    sourceCompatibility = 11
    targetCompatibility = 11
    
    repositories {
        mavenCentral()
    }
}
```

---

## Module: legacy-app

### Build Configuration

**Module Path**: `legacy-app/build.gradle`

**Dependencies**:
```gradle
dependencies {
    // Internal dependency
    implementation project(':legacy-wrappers')
    
    // Persistence API
    implementation 'javax.jdo:jdo-api:3.1'
    
    // Testing
    testImplementation 'org.junit.jupiter:junit-jupiter:5.8.1'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.8.1'
}

test {
    useJUnitPlatform()
}
```

### Build Tasks

**Compile**:
```bash
./gradlew :legacy-app:compileJava
```

**Test**:
```bash
./gradlew :legacy-app:test
```

**Build**:
```bash
./gradlew :legacy-app:build
```

---

## Module: legacy-wrappers

### Build Configuration

**Module Path**: `legacy-wrappers/build.gradle`

**Dependencies**:
```gradle
dependencies {
    // Persistence API (only dependency)
    implementation 'javax.jdo:jdo-api:3.1'
}
```

**Note**: No internal dependencies, no tests

---

## Multi-Module Build

### Settings Configuration

**File**: `settings.gradle`

```gradle
rootProject.name = 'transform-legacy-demo'

include 'legacy-app'
include 'legacy-wrappers'
```

### Build Order

Gradle automatically resolves build order based on dependencies:

1. **legacy-wrappers** (no dependencies)
2. **legacy-app** (depends on legacy-wrappers)

---

## Common Gradle Commands

### Build All Modules

```bash
./gradlew build
```

### Clean Build

```bash
./gradlew clean build
```

### Run Tests

```bash
# All tests
./gradlew test

# Specific module
./gradlew :legacy-app:test
```

### Compile Only

```bash
./gradlew compileJava
```

### Dependency Tree

```bash
./gradlew dependencies
```

### List All Tasks

```bash
./gradlew tasks --all
```

---

## Dependency Management

### Dependency Configuration Types

| Configuration | Scope | Transitivity |
|--------------|-------|--------------|
| `implementation` | Compile + Runtime | Not exposed to consumers |
| `api` | Compile + Runtime | Exposed to consumers |
| `compileOnly` | Compile only | Not included at runtime |
| `runtimeOnly` | Runtime only | Not available at compile time |
| `testImplementation` | Test compile + runtime | Test scope only |

### Current Usage

**legacy-app**:
- `implementation project(':legacy-wrappers')` - Internal module
- `implementation 'javax.jdo:jdo-api:3.1'` - JDO API
- `testImplementation` - JUnit 5

**legacy-wrappers**:
- `implementation 'javax.jdo:jdo-api:3.1'` - JDO API only

---

## Build Output Structure

```
legacy-app/
└── build/
    ├── classes/
    │   └── java/
    │       ├── main/          (compiled production classes)
    │       └── test/          (compiled test classes)
    ├── libs/
    │   └── legacy-app-1.0-SNAPSHOT.jar
    ├── reports/
    │   └── tests/             (test reports HTML)
    └── test-results/
        └── test/              (test results XML)

legacy-wrappers/
└── build/
    ├── classes/
    │   └── java/
    │       └── main/          (compiled production classes)
    └── libs/
        └── legacy-wrappers-1.0-SNAPSHOT.jar
```

---

## Gradle Wrapper

### Wrapper Files

```
transform-legacy-demo/
├── gradlew           (Unix/Mac wrapper script)
├── gradlew.bat       (Windows wrapper script)
└── gradle/
    └── wrapper/
        ├── gradle-wrapper.jar
        └── gradle-wrapper.properties
```

### Wrapper Configuration

**File**: `gradle/wrapper/gradle-wrapper.properties`

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

**Benefits**:
- ✅ Consistent Gradle version across team
- ✅ No need to install Gradle globally
- ✅ Version controlled

---

## Source Sets

### Default Source Sets

**legacy-app**:
```
src/
├── main/
│   └── java/              (production code)
└── test/
    └── java/              (test code)
```

**legacy-wrappers**:
```
src/
└── main/
    └── java/              (production code)
```

### Source Set Configuration

```gradle
sourceSets {
    main {
        java {
            srcDirs = ['src/main/java']
        }
    }
    test {
        java {
            srcDirs = ['src/test/java']
        }
    }
}
```

---

## Build Performance

### Current Build Characteristics

**Build Speed**: Fast (small codebase)
- Total source files: ~7 files
- Total LOC: ~92 lines
- Build time: < 5 seconds

### Performance Optimization

**Current**:
- ✅ Gradle daemon (default enabled)
- ✅ Incremental compilation

**Recommendations**:
```gradle
// build.gradle
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
```

---

## Testing Configuration

### JUnit 5 Setup

**legacy-app/build.gradle**:
```gradle
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.8.1'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.8.1'
}

test {
    useJUnitPlatform()
    
    testLogging {
        events "passed", "skipped", "failed"
    }
}
```

### Test Execution

```bash
# Run all tests
./gradlew test

# Run with detailed output
./gradlew test --info

# Run specific test class
./gradlew test --tests CustomerServiceTest

# Run tests with coverage (if jacoco plugin added)
./gradlew test jacocoTestReport
```

---

## Build Lifecycle

### Standard Build Lifecycle

```
compileJava → processResources → classes → jar → assemble → test → check → build
```

### Custom Tasks

None currently defined. Could add:

```gradle
task printDependencies {
    doLast {
        configurations.runtimeClasspath.each { println it }
    }
}
```

---

## Dependency Versions

### Current Versions

| Dependency | Version | Status |
|-----------|---------|--------|
| JDO API | 3.1 | ⚠️ Deprecated (2013) |
| JUnit Jupiter | 5.8.1 | ⚠️ Outdated (current: 5.10+) |
| Java | 11 | 🟡 Legacy (LTS ended) |

### Recommended Updates

```gradle
dependencies {
    // Replace JDO with JPA
    implementation 'javax.persistence:javax.persistence-api:2.2'
    implementation 'org.hibernate:hibernate-core:5.6.15.Final'
    
    // Update JUnit
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.1'
    
    // Consider Spring Boot for simplified setup
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa:2.7.18'
}
```

---

## Build Scripts Best Practices

### Current State: ✅ Good Structure

**Strengths**:
- Multi-module organization
- Clear dependency separation
- Gradle wrapper included

**Areas for Improvement**:
- ⚠️ Update outdated dependencies
- ⚠️ Add code quality plugins (Checkstyle, SpotBugs)
- ⚠️ Add test coverage plugin (JaCoCo)
- ⚠️ Consider Spring Boot Gradle plugin

---

## Gradle Plugins

### Current Plugins

- `java` - Core Java compilation

### Recommended Plugins

```gradle
plugins {
    id 'java'
    id 'checkstyle'                          // Code style
    id 'pmd'                                 // Static analysis
    id 'com.github.spotbugs' version '5.0.13' // Bug detection
    id 'jacoco'                              // Test coverage
}

checkstyle {
    toolVersion = '10.3.4'
    configFile = file("${rootDir}/config/checkstyle/checkstyle.xml")
}

jacoco {
    toolVersion = '0.8.8'
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }
}
```

---

## Build Troubleshooting

### Common Issues

**Issue 1: Dependency Resolution Failure**
```bash
./gradlew build --refresh-dependencies
```

**Issue 2: Clean Build Needed**
```bash
./gradlew clean build
```

**Issue 3: Gradle Daemon Issues**
```bash
./gradlew --stop
./gradlew build
```

---

## Related Documentation

- **[Program Structure](../reference/program-structure.md)** - Module organization
- **[Dependencies](../architecture/dependencies.md)** - Dependency analysis
- **[Test Specifications](../migration/test-specifications.md)** - Testing strategy
- **[Modernization Options](../migration/modernization-options.md)** - Build modernization

---

*Last Updated: January 2026*  
*Build Tool: Gradle 7.x*  
*Modules: 2*  
*Build Time: < 5 seconds*
