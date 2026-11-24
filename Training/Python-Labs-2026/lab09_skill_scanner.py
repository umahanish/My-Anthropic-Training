"""Lab 9b (Module 9): review a Skill or plugin before you install it.

A static scanner for the red flags covered in the Module 9 workshop. It reads SKILL.md and every
bundled file and reports findings by severity. It never runs the code it scans.

It is a first filter, not a verdict: a clean scan still needs a human review of the source,
the permissions requested and the network endpoints (and your organisation's own scanning, if enabled).

Run
    python lab09_skill_scanner.py samples/skills            # scans both sample skills
    python lab09_skill_scanner.py path/to/your/skill

Exercise: add a rule for a red flag the scanner misses (for example, a hard-coded IP address
or writing to a startup folder), then add a sample that triggers it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED_DOMAINS = {"api.anthropic.com", "docs.claude.com"}

# (severity, rule id, pattern, explanation)
RULES = [
    ("HIGH", "exfil-network", r"requests\.(post|put)|urllib\.request|httpx\.(post|put)|curl\s+-X?\s*POST|fetch\(", "Sends data to a network endpoint"),
    ("HIGH", "secrets-access", r"\.aws/credentials|\.ssh/|id_rsa|API_KEY|os\.environ\)|dict\(os\.environ\)", "Reads credentials or the whole environment"),
    ("HIGH", "shell-exec", r"subprocess\.|os\.system|shell=True|\beval\(|\bexec\(", "Executes shell commands or dynamic code"),
    ("HIGH", "prompt-injection", r"ignore (any |all |previous |prior )+instructions|disregard .*(rules|instructions)", "Instructions that try to override the user or system"),
    ("MEDIUM", "obfuscation", r"base64\.b64decode|codecs\.decode|\\x[0-9a-f]{2}\\x", "Hidden or encoded content"),
    ("MEDIUM", "broad-permissions", r"allowed-tools:.*(Bash\(\*\)|Write)", "Requests broad tool permissions"),
    ("LOW", "vague-description", r"description:.*(everything|improves .* over time|any task)", "Description does not state a narrow purpose"),
]
URL = re.compile(r"https?://([a-zA-Z0-9.-]+)")


def scan(skill_dir: Path) -> list[tuple[str, str, str, str]]:
    findings = []
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        text = path.read_text(errors="ignore")
        rel = str(path.relative_to(skill_dir))
        for severity, rule, pattern, why in RULES:
            for m in re.finditer(pattern, text, re.I):
                line = text[: m.start()].count("\n") + 1
                findings.append((severity, rule, f"{rel}:{line}", why))
        for m in URL.finditer(text):
            if m.group(1) not in ALLOWED_DOMAINS:
                line = text[: m.start()].count("\n") + 1
                findings.append(("MEDIUM", "unknown-domain", f"{rel}:{line}", f"Contacts unlisted domain {m.group(1)}"))
    return sorted(set(findings), key=lambda f: (f[2], f[1]))


def verdict(findings) -> str:
    severities = {f[0] for f in findings}
    if "HIGH" in severities:
        return "REJECT"
    if severities:
        return "NEEDS REVIEW"
    return "PASS SCAN (still review the source)"


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "samples/skills")
    skills = [p.parent for p in root.rglob("SKILL.md")]
    for skill in sorted(skills):
        findings = scan(skill)
        print(f"\n== {skill.name}: {verdict(findings)}")
        for severity, rule, where, why in sorted(findings, key=lambda f: ["HIGH", "MEDIUM", "LOW"].index(f[0])):
            print(f"  {severity:6} {rule:18} {where:28} {why}")
