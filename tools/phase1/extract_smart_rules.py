#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

DOC_ROOT = Path("Documentation")
OUTPUT_FILE = Path("tools/phase1/impact_tokens.json")

# Files to scan
FILES_TO_SCAN = [
    "technical-debt/outdated-components.md",
    "technical-debt/security-vulnerabilities.md",
    "migration/risk-assessment.md",
    "analysis/dependency-analysis.md",
]

# Severity keyword patterns
CRITICAL_KEYWORDS = [
    r'\bsecurity\b',
    r'\bvulnerability\b',
    r'\bcritical\b',
    r'\bblocker\b',
    r'\burgent\b',
    r'\bsql\s+injection\b',
    r'\bcve\b',
    r'\bexploit\b',
]

HIGH_KEYWORDS = [
    r'\blegacy\b',
    r'\bdeprecated\b',
    r'\bunsupported\b',
    r'\bend\s+of\s+life\b',
    r'\beol\b',
    r'\babandoned\b',
    r'\bobsolete\b',
    r'\boutdated\b',
]

MEDIUM_KEYWORDS = [
    r'\bcomplexity\b',
    r'\bmaintainability\b',
    r'\brefactor\b',
    r'\bslow\b',
    r'\bperformance\b',
    r'\bmedium\b',
]

def read_file(file_path: Path) -> str:
    """Read file content, return empty string if not found."""
    return file_path.read_text(encoding="utf-8", errors="ignore") if file_path.exists() else ""

def extract_component_names(text: str) -> list[tuple[str, str]]:
    """
    Extract component/technology names from text.
    Returns list of (name, context) tuples where context is the text around the name.
    """
    components = []
    
    # Pattern 1: Headers like "## Component 1: JDO" or "## Component 1: JDO (Java Data Objects)"
    header_pattern = r'^##+\s+Component\s+\d+[:]\s+([^(\n]+?)(?:\s*\(|$)'
    for match in re.finditer(header_pattern, text, re.MULTILINE):
        name = match.group(1).strip()
        if name and 2 <= len(name) <= 80:
            # Get context (next 500 chars after the header)
            start_pos = match.end()
            context = text[start_pos:start_pos + 500]
            components.append((name, context))
    
    # Pattern 2: Bold items like "**Technology**: Java" or "**Dependency**: javax.jdo:jdo-api"
    bold_pattern = r'\*\*([^*]+?)\*\*[:]\s*([^\n]+)'
    for match in re.finditer(bold_pattern, text):
        label = match.group(1).strip().lower()
        value = match.group(2).strip()
        
        # Only extract from specific labels
        tech_labels = ['technology', 'component', 'dependency', 'api', 'version', 'library', 'framework']
        if any(term in label for term in tech_labels):
            if value and 2 <= len(value) <= 80:
                # Get context around this bold item
                start_pos = match.start()
                context = text[max(0, start_pos - 200):start_pos + 500]
                components.append((value, context))
    
    # Pattern 3: Maven/Gradle dependency coordinates: "javax.jdo:jdo-api:3.1"
    dep_coord_pattern = r'([a-z][a-z0-9._-]+:[a-z][a-z0-9._-]+(?::[0-9.]+)?)'
    for match in re.finditer(dep_coord_pattern, text, re.IGNORECASE):
        dep_name = match.group(1).strip()
        if 5 <= len(dep_name) <= 100:
            start_pos = match.start()
            context = text[max(0, start_pos - 200):start_pos + 500]
            components.append((dep_name, context))
    
    # Pattern 4: Technology names in tables (first column often has tech names)
    # Look for table rows with technology indicators
    table_row_pattern = r'\|[^|]*?([A-Z][a-zA-Z0-9\s]+(?:API|Framework|Library)?)[^|]*\|'
    for match in re.finditer(table_row_pattern, text):
        potential_name = match.group(1).strip()
        # Filter out common table headers
        skip_words = ['dependency', 'version', 'module', 'scope', 'status', 'risk', 'probability', 
                      'impact', 'severity', 'action', 'required', 'component', 'technology']
        if (3 <= len(potential_name) <= 50 and 
            potential_name.lower() not in skip_words and
            not potential_name.isdigit()):
            start_pos = match.start()
            context = text[max(0, start_pos - 200):start_pos + 500]
            components.append((potential_name, context))
    
    # Pattern 5: Technology names with version: "JDO 3.1", "Java 11", "JPA 3.1"
    tech_version_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+(\d+\.?\d*)\b'
    for match in re.finditer(tech_version_pattern, text):
        tech_name = match.group(1).strip()
        version = match.group(2).strip()
        full_name = f"{tech_name} {version}"
        if 3 <= len(tech_name) <= 30:
            start_pos = match.start()
            context = text[max(0, start_pos - 200):start_pos + 500]
            components.append((full_name, context))
            # Also add just the tech name
            components.append((tech_name, context))
    
    return components

def calculate_severity_score(context: str) -> int:
    """
    Calculate impact score based on keywords in context.
    Returns: 10 (CRITICAL), 8 (HIGH), 5 (MEDIUM), or 2 (LOW)
    """
    context_lower = context.lower()
    
    # Check for CRITICAL keywords (score 10)
    for pattern in CRITICAL_KEYWORDS:
        if re.search(pattern, context_lower, re.IGNORECASE):
            return 10
    
    # Check for HIGH keywords (score 8)
    for pattern in HIGH_KEYWORDS:
        if re.search(pattern, context_lower, re.IGNORECASE):
            return 8
    
    # Check for MEDIUM keywords (score 5)
    for pattern in MEDIUM_KEYWORDS:
        if re.search(pattern, context_lower, re.IGNORECASE):
            return 5
    
    # Default to LOW (score 2)
    return 2

def clean_component_name(name: str) -> str:
    """Clean and normalize component name."""
    # Remove markdown formatting
    name = re.sub(r'\*\*', '', name)
    name = re.sub(r'`', '', name)
    # Remove leading dashes/bullets
    name = re.sub(r'^[-•*]\s+', '', name)
    # Remove parenthetical notes (but keep version in format "Tech 3.1")
    if not re.search(r'\d+\.\d+', name):
        name = re.sub(r'\s*\([^)]+\)', '', name)
    # Remove trailing colons, dashes, etc.
    name = re.sub(r'[:;,\-]+$', '', name)
    # Clean whitespace
    name = ' '.join(name.split())
    return name.strip()

def is_valid_component_name(name: str) -> bool:
    """Check if a name looks like a valid technology/component name."""
    if not name or len(name) < 2 or len(name) > 80:
        return False
    
    name_lower = name.lower()
    
    # Skip common false positives
    skip_patterns = [
        r'^component\s+\d+$',
        r'^risk\s+\d+$',
        r'^phase\s+\d+$',
        r'^step\s+\d+$',
        r'^table\s+\d+$',
        r'^\d+$',
        r'^[a-z]$',
        r'^[A-Z]$',
        r'^action\s+required$',
        r'^see\s+',
        r'^last\s+updated',
        r'^overview$',
        r'^summary$',
        r'^details$',
        r'^age[:]',
        r'^active\s+(development|maintenance)$',
        r'^community\s+size$',
        r'^behavioral\s+differences$',
        r'^aging$',
        r'^cve\s+database',
        r'^direct[:]',
        r'^ep[ls]$',  # EPL, ECL
        r'^jsr$',  # Just "JSR" without number
    ]
    
    if any(re.match(pattern, name_lower) for pattern in skip_patterns):
        return False
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', name):
        return False
    
    # Skip common English words (unless they're part of tech names)
    common_words = {'the', 'and', 'or', 'for', 'with', 'from', 'this', 'that', 
                   'these', 'those', 'when', 'where', 'what', 'which', 'who',
                   'how', 'why', 'all', 'any', 'some', 'no', 'not', 'but',
                   'can', 'will', 'would', 'should', 'could', 'may', 'might',
                   'active', 'age', 'community', 'size', 'development', 'maintenance'}
    words = name_lower.split()
    if len(words) == 1 and words[0] in common_words:
        return False
    
    # Must look like a technology/component name:
    # - Maven/Gradle coordinates (contains colon, e.g., "javax.jdo:jdo-api")
    # - Technology with version (e.g., "Java 11", "JDO 3.1", "JPA 3.1")
    # - Known technology acronyms (JDO, JPA, API, etc.)
    # - Technology names from known list
    
    has_colon = ':' in name  # Maven coordinates are strong indicators
    has_version = bool(re.search(r'\d+\.?\d*', name))  # Version numbers indicate tech
    is_acronym = bool(re.match(r'^[A-Z]{2,5}$', name))  # Acronyms like JDO, JPA, API
    
    # Known technology names (case-insensitive)
    known_techs = {
        'java', 'jdo', 'jpa', 'hibernate', 'spring', 'gradle', 'maven',
        'junit', 'struts', 'log4j', 'apache', 'eclipse', 'netty',
        'jackson', 'gson', 'slf4j', 'logback', 'tomcat', 'jetty',
        'javax', 'jdk', 'jre', 'jvm', 'jdbc', 'jndi', 'jms', 'jta',
        'servlet', 'jsp', 'jsf', 'ejb', 'cdi', 'jax-rs', 'jax-ws'
    }
    
    # Check if it's a known tech name
    is_known_tech = name_lower in known_techs
    
    # Check if it starts with known tech prefix
    has_tech_prefix = any(name_lower.startswith(tech) for tech in ['java', 'jdo', 'jpa', 'junit', 'javax'])
    
    # Must have at least one strong technology indicator
    if not (has_colon or (has_version and is_known_tech) or is_acronym or is_known_tech or has_tech_prefix):
        return False
    
    return True

def main():
    """Extract anti-patterns from documentation files."""
    all_patterns = []
    seen_patterns = set()  # Track duplicates by (name, source)
    
    for file_path_str in FILES_TO_SCAN:
        file_path = DOC_ROOT / file_path_str
        if not file_path.exists():
            print(f"[WARN] File not found: {file_path}")
            continue
        
        print(f"[INFO] Processing: {file_path}")
        content = read_file(file_path)
        
        if not content:
            print(f"[WARN] Empty file: {file_path}")
            continue
        
        # Extract component names
        components = extract_component_names(content)
        
        # Get source filename for tracking
        source_name = file_path.name
        
        for name, context in components:
            # Clean the name
            cleaned_name = clean_component_name(name)
            
            # Validate the component name
            if not is_valid_component_name(cleaned_name):
                continue
            
            # Calculate severity
            score = calculate_severity_score(context)
            
            # Create unique key for deduplication
            pattern_key = (cleaned_name.lower(), source_name)
            
            # Only add if not seen, or if this occurrence has higher score
            if pattern_key not in seen_patterns:
                seen_patterns.add(pattern_key)
                all_patterns.append({
                    "token": cleaned_name,
                    "impact_score": score,
                    "source": source_name
                })
            else:
                # Update if this occurrence has higher score
                for pattern in all_patterns:
                    if (pattern["token"].lower() == cleaned_name.lower() and 
                        pattern["source"] == source_name):
                        if score > pattern["impact_score"]:
                            pattern["impact_score"] = score
                        break
    
    # Sort by impact score (descending), then by token name
    all_patterns.sort(key=lambda x: (-x["impact_score"], x["token"].lower()))
    
    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        json.dump(all_patterns, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Extracted {len(all_patterns)} anti-patterns")
    print(f"[OK] Wrote: {OUTPUT_FILE}")
    
    # Print summary
    score_counts = defaultdict(int)
    for pattern in all_patterns:
        score_counts[pattern["impact_score"]] += 1
    
    print("\nSummary by impact score:")
    for score in sorted(score_counts.keys(), reverse=True):
        severity = {10: "CRITICAL", 8: "HIGH", 5: "MEDIUM", 2: "LOW"}.get(score, "UNKNOWN")
        print(f"  {severity} (score {score}): {score_counts[score]} patterns")

if __name__ == "__main__":
    main()
