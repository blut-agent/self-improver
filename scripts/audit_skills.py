#!/usr/bin/env python3
"""Weekly skill audit — find outdated skills and suggest improvements.

Security hardened v1.1.0:
- Path validation for skill files
- Restricted to ~/.hermes/skills/ directory
"""

import os, sys, json
from pathlib import Path
from datetime import datetime, timedelta

# Security: Restrict to skills directory
SKILLS_DIR = Path.home() / '.hermes' / 'skills'

def find_skills():
    """Find all SKILL.md files within allowed directory."""
    skills = []
    try:
        for skill_md in SKILLS_DIR.rglob('SKILL.md'):
            # Validate path is within allowed directory
            if str(skill_md.resolve()).startswith(str(SKILLS_DIR.resolve())):
                skills.append(skill_md)
    except PermissionError:
        pass
    return sorted(skills)

def read_skill(path):
    """Read skill content from validated path."""
    with open(path) as f:
        return f.read()

def check_commands(content):
    issues = []
    deprecated = [
        ('pip install', 'Consider: pipx install or uv pip install'),
        ('brew cask install', 'Deprecated: use brew install --cask'),
        ('docker-compose', 'Note: docker compose (v2) is now a docker subcommand'),
    ]
    for pattern, note in deprecated:
        if pattern in content:
            issues.append(f"Found '{pattern}' — {note}")
    return issues

def check_api_endpoints(content):
    issues = []
    if 'api.github.com' in content:
        issues.append("GitHub API — verify endpoints still valid")
    if 'api.openai.com' in content:
        issues.append("OpenAI API — check for version changes")
    return issues

def check_paths(content):
    issues = []
    if '/Users/' in content:
        issues.append("macOS-specific path found — add Linux/Windows alternative")
    if 'C:\\' in content:
        issues.append("Windows-specific path found — add macOS/Linux alternative")
    return issues

def check_completeness(content):
    issues = []
    required = ['When to Use', 'Workflow', 'Commands Required']
    for section in required:
        if section.lower() not in content.lower():
            issues.append(f"Missing section: {section}")
    return issues

def audit_skill(path):
    """Run full audit on a skill."""
    content = read_skill(path)
    issues = []
    
    issues.extend(check_commands(content))
    issues.extend(check_api_endpoints(content))
    issues.extend(check_paths(content))
    issues.extend(check_completeness(content))
    
    return {
        'path': str(path),
        'name': path.parent.name,
        'issues': issues,
        'size': len(content),
        'last_modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
    }

def generate_report(audits):
    print(f"# Weekly Skill Audit — {datetime.now().strftime('%Y-%m-%d')}\n")
    
    needs_work = [a for a in audits if a['issues']]
    ok = [a for a in audits if not a['issues']]
    
    print(f"## Summary\n")
    print(f"- Skills reviewed: {len(audits)}")
    print(f"- Need updates: {len(needs_work)}")
    print(f"- No changes: {len(ok)}\n")
    
    if needs_work:
        print(f"## Skills Needing Attention\n")
        for audit in needs_work:
            print(f"### {audit['name']}\n")
            print(f"**Path:** `{audit['path']}`\n")
            print("**Issues:**")
            for issue in audit['issues']:
                print(f"- {issue}")
            print()
    
    print(f"## Healthy Skills\n")
    for audit in ok[:10]:
        print(f"- {audit['name']}")
    if len(ok) > 10:
        print(f"- ... and {len(ok) - 10} more")

if __name__ == '__main__':
    skills = find_skills()
    print(f"Found {len(skills)} skills\n", file=sys.stderr)
    
    audits = []
    for skill_path in skills:
        print(f"Auditing {skill_path.parent.name}...", file=sys.stderr)
        audits.append(audit_skill(skill_path))
    
    generate_report(audits)
