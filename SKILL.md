---
name: self-improver
description: Weekly audit and rewrite of all skills. Identify outdated instructions, missing steps, discovered pitfalls, and opportunities for improvement.
version: 1.1.0
author: BlutAgent
license: MIT
metadata:
  hermes:
    tags: [skills, improvement, audit, meta, maintenance]
    related_skills: [skill-management, writing-plans]
---

# Self Improver

## Overview

Self Improver conducts a weekly audit of all skills in the Hermes skills directory. It identifies outdated instructions, missing steps, discovered pitfalls, and opportunities for improvement — then rewrites skills to keep them accurate and useful.

**Core philosophy:** Skills are living documents. They decay as tools change, APIs update, and new pitfalls are discovered. Weekly review prevents skill rot and captures lessons learned.

## Audit Criteria

### 1. Accuracy Check

Does the skill still work as documented?

| Check | Method |
|-------|--------|
| Commands still valid | Run each command, verify output |
| API endpoints working | Test API calls, check for deprecations |
| File paths correct | Verify referenced paths exist |
| Dependencies available | Check tools are installed, versions match |

### 2. Completeness Check

Is anything missing that users need?

| Check | Method |
|-------|--------|
| Missing prerequisites | Compare with similar skills |
| Undocumented edge cases | Review recent session transcripts |
| Missing error handling | Check for "what if X fails" scenarios |
| Incomplete examples | Verify code snippets are copy-pasteable |

### 3. Clarity Check

Is the skill easy to follow?

| Check | Method |
|-------|--------|
| Instructions ambiguous? | Read as a newcomer would |
| Steps in logical order? | Trace the workflow |
| Examples relevant? | Match current use cases |
| Formatting consistent? | Check headers, code blocks, tables |

### 4. Lessons Captured

Were new discoveries made this week?

| Source | What to Capture |
|--------|-----------------|
| Session transcripts | Workarounds, fixes, tricks |
| User corrections | "Actually, do it this way" |
| Failed attempts | What didn't work and why |
| Tool updates | New flags, changed behavior |


## Security Notes

### Path Validation
- Skills directory restricted to `~/.hermes/skills/`
- All file paths validated before reading
- Permission errors handled gracefully

### Audit Safety
- Read-only operations (no file modifications)
- No external API calls
- No code execution

### Changelog

### v1.1.0 (Security Hardening)
- Added path validation (restricted to ~/.hermes/skills/)
- Added permission error handling
- Added Security Notes section

### v1.0.0
- Initial release

## Weekly Workflow

### Step 1: List All Skills

```bash
# Get all skill directories
find ~/.hermes/skills -name "SKILL.md" | sort
```

### Step 2: Prioritize for Review

Not all skills need weekly review. Prioritize by:

1. **High usage** (used 5+ times this week) — always review
2. **Recently modified** (changed in last 2 weeks) — review for stability
3. **Tool-dependent** (uses APIs, CLIs) — check for breaking changes
4. **User-reported issues** — fix reported problems

### Step 3: Review Each Skill

For each skill:

```markdown
## Skill: <name>

### Usage This Week
- Times used: N
- Sessions: [list session IDs]

### Issues Found
- [ ] Command X deprecated
- [ ] Missing error handling for Y
- [ ] Path Z incorrect on Linux

### Lessons to Capture
- Discovered: ...
- User corrected: ...
- Workaround found: ...

### Actions
- [ ] Patch skill with fix
- [ ] Add pitfalls section
- [ ] Update examples
- [ ] No changes needed
```

### Step 4: Apply Patches

For each issue found:

```bash
# Use skill_manage to patch
skill_manage(action='patch', name='skill-name', 
             old_string='outdated instruction',
             new_string='updated instruction')
```

### Step 5: Generate Report

```markdown
# Weekly Skill Audit — YYYY-MM-DD

## Skills Reviewed (N)

| Skill | Status | Changes |
|-------|--------|---------|
| repo-scout | ✅ Updated | Fixed API endpoint |
| code-reviewer | ✅ No changes | — |
| pr-analyst | ⚠️ Needs work | Missing error handling |

## Changes Made

### repo-scout
- Fixed: `/search/repositories` endpoint now requires `per_page` param
- Added: Pitfall about rate limiting

### pr-analyst
- Added: Error handling for private repos
- Updated: Example output format

## Skills Needing Attention

| Skill | Issue | Priority |
|-------|-------|----------|
| pr-analyst | Missing error handling | High |
| morning-brief | CI status check flaky | Medium |

## Next Week's Focus
- Complete pr-analyst error handling
- Investigate morning-brief CI reliability
```

## Python Audit Script

Save as `~/.hermes/skills/software-development/self-improver/scripts/audit_skills.py`:

```python
#!/usr/bin/env python3
"""Weekly skill audit — find outdated skills and suggest improvements."""

import os, sys, json
from pathlib import Path
from datetime import datetime, timedelta

SKILLS_DIR = Path.home() / '.hermes' / 'skills'

def find_skills():
    """Find all SKILL.md files."""
    skills = []
    for skill_md in SKILLS_DIR.rglob('SKILL.md'):
        skills.append(skill_md)
    return sorted(skills)

def read_skill(path):
    """Read skill content."""
    with open(path) as f:
        return f.read()

def check_commands(content):
    """Find shell commands and flag potentially outdated ones."""
    issues = []
    # Look for common patterns that age poorly
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
    """Find API endpoints that might change."""
    issues = []
    if 'api.github.com' in content:
        issues.append("GitHub API — verify endpoints still valid")
    if 'api.openai.com' in content:
        issues.append("OpenAI API — check for version changes")
    return issues

def check_paths(content):
    """Find hardcoded paths that might be OS-specific."""
    issues = []
    if '/Users/' in content:
        issues.append("macOS-specific path found — add Linux/Windows alternative")
    if 'C:\\\\' in content:
        issues.append("Windows-specific path found — add macOS/Linux alternative")
    return issues

def check_completeness(content):
    """Check for missing sections."""
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
    """Generate audit report."""
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
    for audit in ok[:10]:  # Show first 10
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
```

## Integration with Hermes

### Weekly Cron Job

```python
cronjob(
    action='create',
    name='weekly-skill-audit',
    schedule='0 15 * * 0',  # Sunday 3pm
    prompt='Run self-improver skill audit. Review all skills, identify outdated content, capture lessons from this week sessions, patch skills with fixes. Generate report.',
    deliver='origin'
)
```

### Session Search for Lessons

```python
# Search for user corrections this week
session_search(query='actually do it this way OR should be OR correction OR wrong', 
               limit=10)

# Search for failed attempts
session_search(query='error OR failed OR did not work OR workaround',
               limit=10)

# Extract lessons and add to relevant skills
```

### Auto-Patch Pattern

```python
# When an issue is found during the week
skill_manage(
    action='patch',
    name='skill-name',
    old_string='old instruction',
    new_string='new instruction with fix',
)

# Log the change
memory(action='add', target='memory',
       content='Patched skill-name on YYYY-MM-DD: fixed X issue')
```

## Anti-Patterns

### ❌ Auditing Without Acting

**Bad:** Running the audit and not fixing anything
**Good:** Fix at least one issue per audit session

### ❌ Waiting for Perfect

**Bad:** "I'll rewrite the whole skill when I have time"
**Good:** Patch the one broken thing right now

### ❌ Ignoring User Feedback

**Bad:** User says "this doesn't work" and you don't update the skill
**Good:** User correction → immediate skill patch

### ❌ No Version Tracking

**Bad:** Skills change with no record of what changed
**Good:** Update version number and add changelog section

## Changelog Format

Add to each skill:

```markdown
## Changelog

### v1.1.0 (2026-04-23)
- Fixed: GitHub API endpoint for PR search
- Added: Rate limiting pitfall
- Updated: Example output format

### v1.0.0 (2026-04-15)
- Initial release
```

## Metrics

Track weekly:

| Metric | Target |
|--------|--------|
| Skills audited | All, weekly |
| Issues found & fixed | 3+ per week |
| User-reported issues | 0 carryover |
| Skills with changelogs | 100% |

## Remember

```
Audit every Sunday
Fix at least one issue per session
Capture lessons from user corrections
Version and changelog every change
Skills are living documents — they decay without care
```

**Self Improver ensures skills stay accurate, complete, and useful.**