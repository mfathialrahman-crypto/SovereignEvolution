#!/usr/bin/env python3
"""
SovereignEvolution — Permanent Autonomous Evolution Engine
Version: 1.1

Drives continuous improvement of the MFR Cognitive Ecosystem.
"""

import json
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any

MEMORY_FILE = "evolution_memory.json"
DAILY_REPORT = "daily_report.md"
STATUS_FILE = "evolution_status.json"
LOG_FILE = "evolution.log"

ECOSYSTEM = [
    {"name": "MFR-Cognition", "role": "Cognitive Core", "repo": "mfathialrahman-crypto/MFR-Cognition"},
    {"name": "AetherMind", "role": "Intelligence / Reasoning Layer", "repo": "mfathialrahman-crypto/AetherMind"},
    {"name": "HelixMind", "role": "Telemetry / Anomaly Intelligence Layer", "repo": "mfathialrahman-crypto/HelixMind"},
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
        "version": "1.1",
        "cycles": [],
        "known_capabilities": [
            "HelixMind multi-layer + correlation + explainable health",
            "MFR-Cognition decision pipeline with confidence",
            "AetherMind hypothesis + recommendation with evidence-first rule"
        ],
        "known_gaps": [
            "No unit tests in any project",
            "No shared event/schema contracts",
            "No cross-project data consumption yet",
            "Limited long-term baseline learning"
        ],
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
        "type": cycle_type,
        "changes": changes,
        "new_capabilities": capabilities,
        "discoveries": discoveries,
        "next_target": next_target,
        "notes": notes
    }
    memory.setdefault("cycles", []).append(entry)
    if len(memory["cycles"]) > 120:
        memory["cycles"] = memory["cycles"][-120:]
    memory["total_cycles"] = memory.get("total_cycles", 0) + 1
    memory["last_" + cycle_type] = utc_now().isoformat()
    # Update known capabilities
    for c in capabilities:
        if c not in memory.get("known_capabilities", []):
            memory.setdefault("known_capabilities", []).append(c)
    return memory

def analyze_ecosystem() -> Dict:
    analysis = {
        "timestamp": utc_now().isoformat(),
        "projects": {
            "HelixMind": {
                "maturity": "high",
                "version": "1.1",
                "strengths": [
                    "Multi-layer anomaly detection",
                    "Correlated multi-signal events",
                    "Explainable health score with components",
                    "Structured events + insights"
                ],
                "gaps": ["No unit tests", "No long-term baseline model"]
            },
            "MFR-Cognition": {
                "maturity": "high",
                "version": "4.1",
                "strengths": [
                    "Structured decision pipeline",
                    "Evidence + confidence scoring",
                    "Persistent decision traces"
                ],
                "gaps": ["No unit tests", "Still primarily metric-driven"]
            },
            "AetherMind": {
                "maturity": "medium-high",
                "version": "1.1",
                "strengths": [
                    "Hypothesis generation",
                    "Evidence-first recommendations",
                    "Confidence scoring",
                    "Reasoning trace"
                ],
                "gaps": ["No unit tests", "Does not yet consume Helix/MFR outputs"]
            }
        },
        "system_gaps": [
            "No shared event/schema contracts between projects",
            "No automated tests in any repository",
            "No cross-project data flow yet",
            "No long-term baseline learning across days",
            "No Project Factory operationalization beyond discovery"
        ],
        "high_value_opportunities": [
            {
                "id": "test-foundation",
                "title": "Add real unit tests across the ecosystem",
                "impact": 9, "feasibility": 8, "strategic": 9, "reusability": 10,
                "score": 9*8*9*10,
                "description": "Introduce pytest tests for core logic in HelixMind, MFR-Cognition and AetherMind."
            },
            {
                "id": "shared-contracts",
                "title": "Create shared event and decision schemas",
                "impact": 8, "feasibility": 7, "strategic": 9, "reusability": 10,
                "score": 8*7*9*10,
                "description": "Define common contracts so projects can interoperate cleanly without tight coupling."
            },
            {
                "id": "cross-project-flow",
                "title": "Enable Helix → MFR → Aether data flow",
                "impact": 9, "feasibility": 6, "strategic": 9, "reusability": 8,
                "score": 9*6*9*8,
                "description": "Allow AetherMind to optionally consume structured outputs from HelixMind and MFR-Cognition."
            },
            {
                "id": "baseline-learning",
                "title": "Long-term baseline learning in HelixMind",
                "impact": 7, "feasibility": 7, "strategic": 7, "reusability": 8,
                "score": 7*7*7*8,
                "description": "Learn normal ranges over longer windows instead of only short recent history."
            }
        ]
    }
    analysis["high_value_opportunities"].sort(key=lambda x: x["score"], reverse=True)
    return analysis

def choose_next_target(analysis: Dict, memory: Dict) -> Dict:
    opportunities = analysis.get("high_value_opportunities", [])
    recent = []
    for c in memory.get("cycles", [])[-8:]:
        recent.append(c.get("next_target", ""))
        recent.extend(c.get("changes", []))

    for opp in opportunities:
        if opp["id"] not in str(recent):
            return opp
    return opportunities[0] if opportunities else {
        "id": "maintain",
        "title": "Maintain and observe",
        "description": "No high-value safe change identified today."
    }

def detect_cycle_type(memory: Dict) -> str:
    """Simple heuristic for daily / weekly / monthly."""
    now = utc_now()
    last_weekly = memory.get("last_weekly")
    last_monthly = memory.get("last_monthly")

    if last_monthly:
        try:
            lm = datetime.fromisoformat(last_monthly.replace("Z", "+00:00"))
            if (now - lm) > timedelta(days=28):
                return "monthly"
        except Exception:
            pass
    if last_weekly:
        try:
            lw = datetime.fromisoformat(last_weekly.replace("Z", "+00:00"))
            if (now - lw) > timedelta(days=6):
                return "weekly"
        except Exception:
            pass
    return "daily"

def generate_daily_report(memory: Dict, analysis: Dict, target: Dict, cycle_type: str) -> str:
    now = utc_now()
    lines = [
        f"# {cycle_type.upper()} Evolution Report",
        f"",
        f"**Date:** {now.strftime('%Y-%m-%d %H:%M:%S')} UTC",
        f"**Engine:** SovereignEvolution v1.1",
        f"**Total Cycles:** {memory.get('total_cycles', 0)}",
        f"",
        f"## Ecosystem Snapshot",
        f"",
    ]
    for name, info in analysis.get("projects", {}).items():
        lines.append(f"### {name} (v{info.get('version', '?')} — {info.get('maturity')})")
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
    lines.append("Only real, high-value, safe changes are executed. Artificial changes are forbidden.")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by SovereignEvolution Engine*")
    return "\n".join(lines)

def main():
    log("=== SovereignEvolution Cycle Started ===")

    memory = load_memory()
    cycle_type = detect_cycle_type(memory)
    analysis = analyze_ecosystem()
    target = choose_next_target(analysis, memory)

    log(f"Cycle type: {cycle_type}")
    log(f"Selected next target: {target.get('id')} — {target.get('title')}")

    changes = [
        f"Performed {cycle_type} ecosystem analysis",
        f"Selected next target: {target.get('id')}"
    ]
    capabilities = memory.get("known_capabilities", [])[:]
    discoveries = analysis.get("system_gaps", [])[:4]

    memory = record_cycle(
        memory,
        cycle_type=cycle_type,
        changes=changes,
        capabilities=[],
        discoveries=discoveries,
        next_target=target.get("id", "unknown"),
        notes=target.get("description", "")
    )

    save_json(MEMORY_FILE, memory)

    report = generate_daily_report(memory, analysis, target, cycle_type)
    with open(DAILY_REPORT, "w", encoding="utf-8") as f:
        f.write(report)

    status = {
        "last_run": utc_now().isoformat(),
        "engine_version": "1.1",
        "cycle_type": cycle_type,
        "total_cycles": memory.get("total_cycles", 0),
        "next_target": target,
        "ecosystem": [p["name"] for p in ECOSYSTEM],
        "known_capabilities_count": len(memory.get("known_capabilities", []))
    }
    save_json(STATUS_FILE, status)

    print(report)
    log("=== SovereignEvolution Cycle Completed ===")

if __name__ == "__main__":
    main()
