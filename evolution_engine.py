#!/usr/bin/env python3
"""
SovereignEvolution — Permanent Autonomous Evolution Engine
Version: 1.0

Role: Daily / Weekly / Monthly evolution driver for the MFR ecosystem.

Ecosystem targets:
  - MFR-Cognition   → Cognitive Core
  - AetherMind      → Intelligence / Reasoning Layer
  - HelixMind       → Telemetry / Anomaly Intelligence Layer
"""

import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# ==================== CONFIG ====================
MEMORY_FILE = "evolution_memory.json"
DAILY_REPORT = "daily_report.md"
WEEKLY_REPORT = "weekly_report.md"
STATUS_FILE = "evolution_status.json"
LOG_FILE = "evolution.log"

ECOSYSTEM = [
    {
        "name": "MFR-Cognition",
        "role": "Cognitive Core",
        "repo": "mfathialrahman-crypto/MFR-Cognition",
        "main_file": "brain.py"
    },
    {
        "name": "AetherMind",
        "role": "Intelligence / Reasoning Layer",
        "repo": "mfathialrahman-crypto/AetherMind",
        "main_file": "core.py"
    },
    {
        "name": "HelixMind",
        "role": "Telemetry / Anomaly Intelligence Layer",
        "repo": "mfathialrahman-crypto/HelixMind",
        "main_file": "helix_core.py"
    }
]

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def log(msg: str, level: str = "INFO"):
    ts = utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] [{level}] {msg}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def load_json(path: str, default: Any) -> Any:
    p = Path(path)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log(f"Failed to load {path}: {e}", "ERROR")
    return default

def save_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

def signature(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def load_memory() -> Dict:
    return load_json(MEMORY_FILE, {
        "created_at": utc_now().isoformat(),
        "version": "1.0",
        "cycles": [],
        "known_capabilities": [],
        "known_gaps": [],
        "project_ideas": [],
        "last_daily": None,
        "last_weekly": None,
        "last_monthly": None,
        "total_cycles": 0
    })

def record_cycle(memory: Dict, cycle_type: str, changes: List[str],
                 capabilities: List[str], discoveries: List[str],
                 next_target: str, notes: str = "") -> Dict:
    entry = {
        "id": signature({"ts": utc_now().isoformat(), "type": cycle_type}),
        "timestamp": utc_now().isoformat(),
        "type": cycle_type,          # daily | weekly | monthly
        "changes": changes,
        "new_capabilities": capabilities,
        "discoveries": discoveries,
        "next_target": next_target,
        "notes": notes
    }
    memory["cycles"].append(entry)
    # Keep last 90 cycles
    if len(memory["cycles"]) > 90:
        memory["cycles"] = memory["cycles"][-90:]
    memory["total_cycles"] = memory.get("total_cycles", 0) + 1
    memory["last_" + cycle_type] = utc_now().isoformat()
    return memory

def analyze_ecosystem() -> Dict:
    """
    Static analysis of known ecosystem state.
    In a full autonomous setting this would pull live repo data.
    Here we maintain a truthful snapshot of current known strengths/gaps.
    """
    analysis = {
        "timestamp": utc_now().isoformat(),
        "projects": {},
        "system_gaps": [],
        "high_value_opportunities": []
    }

    # Known current state (updated as evolution progresses)
    analysis["projects"]["HelixMind"] = {
        "maturity": "high",
        "strengths": [
            "Multi-layer anomaly detection",
            "Correlated multi-signal events",
            "Explainable health score",
            "Structured events + insights"
        ],
        "gaps": [
            "No unit tests",
            "No external event consumption yet",
            "Limited long-term trend models"
        ]
    }

    analysis["projects"]["MFR-Cognition"] = {
        "maturity": "medium-high",
        "strengths": [
            "Structured decision pipeline",
            "Evidence + confidence scoring",
            "Decision trace persistence"
        ],
        "gaps": [
            "No unit tests",
            "Still largely metric-driven",
            "Limited memory abstraction"
        ]
    }

    analysis["projects"]["AetherMind"] = {
        "maturity": "medium",
        "strengths": [
            "Cleaner structure than original",
            "Logging present",
            "Basic statistical detection"
        ],
        "gaps": [
            "Still too similar to monitoring scripts",
            "No real reasoning / hypothesis layer",
            "No consumption of Helix or MFR outputs",
            "No unit tests"
        ]
    }

    analysis["system_gaps"] = [
        "No shared event/schema contracts between projects",
        "No automated tests in any repository",
        "No cross-project data flow yet",
        "AetherMind not yet acting as Intelligence Layer",
        "No Project Factory operationalization",
        "No long-term trend / baseline learning across days"
    ]

    analysis["high_value_opportunities"] = [
        {
            "id": "aether-reasoning-upgrade",
            "title": "Upgrade AetherMind to real Intelligence Layer",
            "impact": 9,
            "feasibility": 8,
            "strategic": 9,
            "reusability": 7,
            "score": 9*8*9*7,
            "description": "Add hypothesis generation, evidence weighing, and recommendation with confidence."
        },
        {
            "id": "shared-contracts",
            "title": "Create shared event/schema contracts",
            "impact": 8,
            "feasibility": 7,
            "strategic": 9,
            "reusability": 10,
            "score": 8*7*9*10,
            "description": "Define common event and decision schemas so projects can interoperate cleanly."
        },
        {
            "id": "test-foundation",
            "title": "Add real unit + workflow tests",
            "impact": 8,
            "feasibility": 8,
            "strategic": 8,
            "reusability": 9,
            "score": 8*8*8*9,
            "description": "Introduce pytest-based tests for core logic in all three projects."
        },
        {
            "id": "baseline-learning",
            "title": "Long-term baseline learning in HelixMind",
            "impact": 7,
            "feasibility": 7,
            "strategic": 7,
            "reusability": 8,
            "score": 7*7*7*8,
            "description": "Learn normal ranges over days/weeks instead of only short windows."
        }
    ]

    # Sort opportunities by score
    analysis["high_value_opportunities"].sort(key=lambda x: x["score"], reverse=True)
    return analysis

def choose_next_target(analysis: Dict, memory: Dict) -> Dict:
    """Select the highest value target that has not been recently completed."""
    opportunities = analysis.get("high_value_opportunities", [])
    recent_changes = []
    for c in memory.get("cycles", [])[-10:]:
        recent_changes.extend(c.get("changes", []))

    for opp in opportunities:
        # Simple avoidance of repeating the exact same target too soon
        if opp["id"] not in str(recent_changes):
            return opp

    # Fallback
    return opportunities[0] if opportunities else {
        "id": "maintain",
        "title": "Maintain and observe",
        "description": "No high-value safe change identified today."
    }

def generate_daily_report(memory: Dict, analysis: Dict, target: Dict) -> str:
    now = utc_now()
    lines = [
        f"# Daily Evolution Report",
        f"",
        f"**Date:** {now.strftime('%Y-%m-%d %H:%M:%S')} UTC",
        f"**Engine Version:** 1.0",
        f"**Total Cycles:** {memory.get('total_cycles', 0)}",
        f"",
        f"## Ecosystem Snapshot",
        f"",
    ]

    for name, info in analysis.get("projects", {}).items():
        lines.append(f"### {name} ({info.get('maturity')})")
        lines.append(f"- Strengths: {', '.join(info.get('strengths', []))}")
        lines.append(f"- Gaps: {', '.join(info.get('gaps', []))}")
        lines.append("")

    lines.append("## System Gaps")
    for g in analysis.get("system_gaps", []):
        lines.append(f"- {g}")
    lines.append("")

    lines.append("## Next Best Development Target")
    lines.append(f"- **ID:** `{target.get('id')}`")
    lines.append(f"- **Title:** {target.get('title')}")
    lines.append(f"- **Description:** {target.get('description')}")
    if "score" in target:
        lines.append(f"- **Priority Score:** {target.get('score')}")
    lines.append("")

    lines.append("## Rule")
    lines.append("Only real, high-value, safe changes are executed. If no such change exists, the cycle records analysis and waits for the next opportunity.")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by SovereignEvolution Engine*")
    return "\n".join(lines)

def main():
    log("=== SovereignEvolution Daily Cycle Started ===")

    memory = load_memory()
    analysis = analyze_ecosystem()
    target = choose_next_target(analysis, memory)

    log(f"Selected next target: {target.get('id')} — {target.get('title')}")

    # In this version the engine records the analysis and target.
    # Actual cross-repo code changes are performed by the human/AI operator
    # or future enhanced actions that have proper write tokens.
    changes = [
        "Recorded full ecosystem analysis",
        f"Selected next target: {target.get('id')}"
    ]
    capabilities = []
    discoveries = analysis.get("system_gaps", [])[:5]

    memory = record_cycle(
        memory,
        cycle_type="daily",
        changes=changes,
        capabilities=capabilities,
        discoveries=discoveries,
        next_target=target.get("id", "unknown"),
        notes=target.get("description", "")
    )

    save_json(MEMORY_FILE, memory)

    report = generate_daily_report(memory, analysis, target)
    with open(DAILY_REPORT, "w", encoding="utf-8") as f:
        f.write(report)

    status = {
        "last_run": utc_now().isoformat(),
        "engine_version": "1.0",
        "total_cycles": memory.get("total_cycles", 0),
        "next_target": target,
        "ecosystem": [p["name"] for p in ECOSYSTEM]
    }
    save_json(STATUS_FILE, status)

    print(report)
    log("=== SovereignEvolution Daily Cycle Completed ===")

if __name__ == "__main__":
    main()
