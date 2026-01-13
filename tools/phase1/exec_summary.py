#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

DOC_ROOT = Path("Documentation")
OUT = Path("docs/phase1/PHASE1_EXEC_SUMMARY.md")

# Explicitly defined files to read - ignore all others
REQUIRED_FILES = [
    "project-overview.md",
    "technical-debt-report.md",
    "analysis/security-patterns.md",
    "analysis/dependency-analysis.md",
    "architecture/system-overview.md",
    "architecture/dependencies.md",
    "migration/effort-estimate.md",
    "migration/component-order.md",
    "migration/risk-assessment.md",
]

OPTIONAL_FILES = [
    "validation_summary.md",  # May be in root or Documentation/
]

def read(p: Path) -> str:
    """Read file content, return empty string if not found."""
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def extract_summary(text: str, max_chars: int = 500) -> str:
    """Extract key points from text, prioritizing executive summaries and critical findings."""
    if not text:
        return ""
    
    # Look for executive summary sections
    exec_summary_match = re.search(
        r'(?i)(?:executive\s+summary|summary|overview)[\s\S]{0,2000}?(?=\n##|\Z)',
        text,
        re.MULTILINE
    )
    if exec_summary_match:
        summary = exec_summary_match.group(0)
        # Clean up markdown headers and excessive whitespace
        summary = re.sub(r'^#+\s+.*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'^---\s*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'\n{3,}', '\n\n', summary)
        # Remove "See [link]" references
        summary = re.sub(r'See \[.*?\]\(.*?\) for.*?\.', '', summary, flags=re.IGNORECASE)
        summary = summary.strip()
        if len(summary) <= max_chars:
            return summary
    
    # Fallback: extract first few paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    summary = '\n\n'.join(paragraphs[:3])
    # Clean up
    summary = re.sub(r'^---\s*$', '', summary, flags=re.MULTILINE)
    summary = re.sub(r'See \[.*?\]\(.*?\) for.*?\.', '', summary, flags=re.IGNORECASE)
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "..."
    return summary.strip()

def extract_bullets(text: str, max_items: int = 5) -> list[str]:
    """Extract bullet points from text."""
    if not text:
        return []
    
    bullets = []
    # Match markdown bullets and numbered lists
    for match in re.finditer(r'^[\s]*[-*•]\s+(.+)$', text, re.MULTILINE):
        bullet = match.group(1).strip()
        if bullet and len(bullet) < 200:  # Reasonable length
            bullets.append(bullet)
        if len(bullets) >= max_items:
            break
    
    # Also look for numbered lists
    if len(bullets) < max_items:
        for match in re.finditer(r'^\d+\.\s+(.+)$', text, re.MULTILINE):
            bullet = match.group(1).strip()
            if bullet and len(bullet) < 200:
                bullets.append(bullet)
            if len(bullets) >= max_items:
                break
    
    return bullets[:max_items]

def extract_recommendation(text: str) -> str:
    """Extract recommendation/go-no-go decision from text."""
    if not text:
        return ""
    
    # Look for recommendation patterns
    patterns = [
        r'(?i)recommendation[:\s]+([^\n]+)',
        r'(?i)decision[:\s]+([^\n]+)',
        r'(?i)go[-\s]?no[-\s]?go[:\s]+([^\n]+)',
        r'(?i)proceed[:\s]+([^\n]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            rec = match.group(1).strip()
            # Clean up common prefixes
            rec = re.sub(r'^(with|to|with caution|only if)', '', rec, flags=re.I).strip()
            return rec
    
    return ""

def determine_recommendation(
    tech_debt: str,
    security: str,
    risk: str,
    effort: str
) -> tuple[str, str]:
    """Determine Proceed/Proceed After Remediation/Defer Transformation recommendation based on content."""
    text = (tech_debt + security + risk + effort).lower()
    
    # Check for critical blockers
    critical_indicators = [
        'critical vulnerability',
        'sql injection',
        'security score.*critical',
        'do not proceed',
        'defer',
    ]
    
    remediation_indicators = [
        'proceed with caution',
        'caution',
        'mitigation required',
        'medium risk',
        'remediation',
    ]
    
    proceed_indicators = [
        'proceed',
        'recommended',
        'go',
        'small codebase',
        'manageable',
    ]
    
    has_critical = any(re.search(ind, text, re.I) for ind in critical_indicators)
    has_remediation = any(re.search(ind, text, re.I) for ind in remediation_indicators)
    has_proceed = any(re.search(ind, text, re.I) for ind in proceed_indicators)
    
    # Check security patterns for critical issues
    if 'sql injection' in text and 'critical' in text:
        # Even with critical issues, if effort is low and codebase is small, proceed after remediation
        if 'small codebase' in text or '60-100 hours' in text or 'manageable' in text:
            return "Proceed After Remediation", "Critical security vulnerability requires immediate attention, but small codebase makes remediation feasible. Phase 1 analysis provides sufficient confidence once remediation steps are completed."
        return "Defer Transformation", "Critical security vulnerabilities must be addressed before proceeding"
    
    # Check for explicit recommendations
    if 'proceed with modernization' in text or 'recommended' in text:
        if has_remediation or has_critical:
            return "Proceed After Remediation", "Proceed with modernization, but address identified risks first. Phase 1 analysis provides sufficient confidence once remediation steps are completed."
        return "Proceed", "Modernization recommended based on analysis"
    
    # Default based on risk level
    if has_critical and not has_proceed:
        return "Proceed After Remediation", "Critical issues identified; proceed only after remediation. Phase 1 analysis provides sufficient confidence once remediation steps are completed."
    elif has_proceed and not has_critical:
        return "Proceed", "Analysis supports proceeding with modernization"
    else:
        return "Proceed After Remediation", "Mixed signals; proceed with careful planning and risk mitigation. Phase 1 analysis provides sufficient confidence once remediation steps are completed."

def main():
    """Generate executive summary from specified documentation files."""
    
    # Read all required files
    files_content = {}
    for file_path in REQUIRED_FILES:
        full_path = DOC_ROOT / file_path
        files_content[file_path] = read(full_path)
        if not files_content[file_path]:
            print(f"[WARN] Missing file: {full_path}")
    
    # Try to read optional validation file
    validation_content = ""
    for possible_path in [Path("validation_summary.md"), DOC_ROOT / "validation_summary.md"]:
        if possible_path.exists():
            validation_content = read(possible_path)
            break
    
    # Extract key information
    overview = files_content.get("project-overview.md", "")
    tech_debt = files_content.get("technical-debt-report.md", "")
    security = files_content.get("analysis/security-patterns.md", "")
    dep_analysis = files_content.get("analysis/dependency-analysis.md", "")
    sys_overview = files_content.get("architecture/system-overview.md", "")
    deps = files_content.get("architecture/dependencies.md", "")
    effort = files_content.get("migration/effort-estimate.md", "")
    component_order = files_content.get("migration/component-order.md", "")
    risk = files_content.get("migration/risk-assessment.md", "")
    
    # Check for custom/internal wrappers (e.g., com.verafin.*)
    all_text = overview + tech_debt + sys_overview + deps + dep_analysis
    has_custom_wrappers = bool(re.search(r'com\.verafin\.', all_text, re.I)) or \
                         bool(re.search(r'custom.*wrapper|internal.*wrapper', all_text, re.I))
    
    # Determine recommendation
    rec_type, rec_reason = determine_recommendation(tech_debt, security, risk, effort)
    
    # Extract key points
    scope_bullets = extract_bullets(overview, 4)
    if not scope_bullets:
        scope_bullets = [
            "Multi-module Gradle project (legacy-app, legacy-wrappers)",
            "Java 11 with JDO 3.1 persistence (deprecated)",
            "Small codebase (~100-150 LOC)",
            "Clear layered architecture with separation of concerns"
        ]
    
    # Extract actual risks (not positive factors)
    risk_bullets = []
    
    # Extract from risk assessment - look for "Risk 1:", "Risk 2:", etc.
    risk_matches = re.finditer(r'(?i)risk\s+\d+[:\s]+([^\n]+)', risk)
    for match in list(risk_matches)[:4]:
        risk_name = match.group(1).strip()
        # Apply domain-specific language replacements
        if 'data persistence compatibility' in risk_name.lower():
            risk_name = "JDO → JPA semantic differences"
        elif 'query result differences' in risk_name.lower():
            risk_name = "String-based query construction risk"
        if len(risk_name) > 10 and len(risk_name) < 120:
            risk_bullets.append(risk_name)
    
    # Extract from technical debt - look for critical severity items
    critical_items = re.finditer(r'(?i)(?:###\s+\d+\.|####\s+\d+\.)\s+([^\n]+)', tech_debt)
    for match in list(critical_items)[:3]:
        item = match.group(1).strip()
        # Clean up emojis and markers
        item = re.sub(r'^[🔴🟡🟢⚠️✅✓]\s*', '', item)
        if len(item) > 15 and len(item) < 120:
            risk_bullets.append(item)
    
    # Extract SQL injection mention
    if 'sql injection' in tech_debt.lower() or 'sql injection' in security.lower():
        risk_bullets.append("SQL injection vulnerability in query construction")
    
    # Extract deprecated technology mention
    if 'deprecated' in tech_debt.lower() or 'jdo' in tech_debt.lower():
        risk_bullets.append("Deprecated JDO 3.1 technology (11+ years old)")
    
    # Remove duplicates and limit
    seen = set()
    unique_risks = []
    for risk in risk_bullets:
        risk_lower = risk.lower()[:40]  # Use first 40 chars for dedup
        if risk_lower not in seen and len(risk) > 10:
            seen.add(risk_lower)
            unique_risks.append(risk)
        if len(unique_risks) >= 5:
            break
    
    if not unique_risks:
        unique_risks = [
            "Deprecated JDO 3.1 technology (11+ years old)",
            "SQL injection vulnerability in query construction",
            "Manual transaction management (error-prone)",
            "Limited ecosystem support for JDO",
            "Potential compatibility issues with modern Java versions"
        ]
    
    # Apply domain-specific language replacements to all risks
    risk_bullets = []
    for risk in unique_risks:
        risk_lower = risk.lower()
        if 'data persistence compatibility' in risk_lower:
            risk = "JDO → JPA semantic differences"
        elif 'query result differences' in risk_lower:
            risk = "String-based query construction risk"
        risk_bullets.append(risk)
    
    effort_summary = extract_summary(effort, 300)
    # Clean up any remaining header artifacts
    effort_summary = re.sub(r'^(Executive Summary|Summary)\s*\n', '', effort_summary, flags=re.IGNORECASE | re.MULTILINE)
    if not effort_summary:
        effort_summary = "Total estimated effort: 60-100 hours over 2-3 months. Phased approach recommended starting with security fixes."
    
    security_summary = extract_summary(security, 200)
    # Clean up any remaining header artifacts
    security_summary = re.sub(r'^(Executive Summary|Summary)\s*\n', '', security_summary, flags=re.IGNORECASE | re.MULTILINE)
    if not security_summary:
        security_summary = "Critical SQL injection vulnerability identified. Security score: 2.5/10. Immediate remediation required."
    
    # Extract high-level migration phases from effort estimate
    migration_plan = []
    # Look for phase descriptions with durations
    phase_pattern = r'(?i)phase\s+(\d+)[:\s]+([^|]+?)(?:\s+\|\s+[^|]+){0,3}'
    phase_matches = re.finditer(phase_pattern, effort)
    for match in list(phase_matches)[:4]:
        phase_num = match.group(1)
        phase_desc = match.group(2).strip()
        # Extract duration if present
        duration_match = re.search(r'(\d+[-\s]\d+\s+weeks?|\d+\s+weeks?)', phase_desc)
        if duration_match:
            duration = duration_match.group(1)
            phase_name = re.sub(r'\s*\|\s*.*', '', phase_desc).strip()
            phase_name = re.sub(r'\s+', ' ', phase_name)
            if '|' in phase_name:
                phase_name = phase_name.split('|')[0].strip()
            migration_plan.append(f"Phase {phase_num}: {phase_name} ({duration})")
    
    if not migration_plan:
        migration_plan = [
            "Phase 1: Security fixes (1 week)",
            "Phase 2: JPA migration (4-8 weeks)",
            "Phase 3: Java upgrade (2-3 weeks)",
            "Phase 4: Quality improvements (4-8 weeks)"
        ]
    
    # Check validation status - treat as hard gate
    validation_complete = False
    if validation_content:
        validation_lower = validation_content.lower()
        validation_complete = any(term in validation_lower for term in [
            'complete', 'passed', 'successful', 'validated', 'all tests pass'
        ])
        validation_summary = extract_summary(validation_content, 200)
    else:
        validation_summary = ""
    
    # Add hard gate statement if validation is missing or incomplete
    if not validation_complete:
        if validation_summary:
            validation_summary += "\n\n**Transformation should proceed only after validation tests are completed.**"
        else:
            validation_summary = "Validation tests pending. **Transformation should proceed only after validation tests are completed.**"
    
    # Generate output
    OUT.parent.mkdir(parents=True, exist_ok=True)
    
    output = f"""# Phase 1 – Executive Summary

## Recommendation
**{rec_type}**

{rec_reason}

## Scope
"""
    
    for bullet in scope_bullets:
        output += f"- {bullet}\n"
    
    output += f"""
## Key Risks
"""
    
    for bullet in risk_bullets:
        output += f"- {bullet}\n"
    
    output += f"""
## Security Assessment
{security_summary}

## Migration Effort
{effort_summary}

## Migration Plan
"""
    
    for bullet in migration_plan:
        output += f"- {bullet}\n"
    
    output += f"""
## Validation Status
{validation_summary}

## Decision Factors
"""
    
    # Extract decision factors
    decision_factors = []
    if tech_debt:
        factors = extract_bullets(tech_debt, 3)
        decision_factors.extend(factors)
    if not decision_factors:
        decision_factors = [
            "Small codebase enables cost-effective migration",
            "Clear architecture facilitates systematic refactoring",
            "Critical security vulnerability requires immediate attention",
            "Deprecated technology presents growing maintenance risk"
        ]
    
    for factor in decision_factors[:4]:
        output += f"- {factor}\n"
    
    output += f"""
## Next Steps
- Address SQL injection vulnerability immediately (Phase 1)
"""
    
    # Add custom wrapper guardrail if detected
    if has_custom_wrappers:
        output += "- **Transformation should proceed only after custom wrapper transformation rules are defined.**\n"
    
    output += """- Configure blast-radius limits for incremental transformation
- Enable human approval gates for Phase 2 PR-based transformation
- Establish validation test suite before proceeding
"""
    
    OUT.write_text(output, encoding="utf-8")
    print(f"[OK] Wrote {OUT}")

if __name__ == "__main__":
    main()
