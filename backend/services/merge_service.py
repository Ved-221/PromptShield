from typing import List, Dict, Any
from schemas import Finding

SEVERITY_ORDER = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def merge_findings(raw_findings: List[Dict[str, Any]]) -> List[Finding]:
    if not raw_findings:
        return []

    # Sort primarily by start ASC, then length DESC, then severity DESC, then confidence DESC
    def sort_key(item):
        length = item["end"] - item["start"]
        severity = SEVERITY_ORDER.get(item["risk_level"], 1)
        return (item["start"], -length, -severity, -item["confidence"])

    sorted_raw = sorted(raw_findings, key=sort_key)
    merged = []

    for current in sorted_raw:
        if not merged:
            merged.append(current)
            continue

        prev = merged[-1]

        # Check for overlap: current.start < prev.end
        if current["start"] < prev["end"]:
            # They overlap. Decide which one to keep or if prev completely encloses current.
            prev_len = prev["end"] - prev["start"]
            curr_len = current["end"] - current["start"]

            prev_sev = SEVERITY_ORDER.get(prev["risk_level"], 1)
            curr_sev = SEVERITY_ORDER.get(current["risk_level"], 1)

            # If current has higher severity (e.g. Critical vs Medium), replace prev
            if curr_sev > prev_sev:
                merged[-1] = current
            # If equal severity and current is longer
            elif curr_sev == prev_sev and curr_len > prev_len:
                merged[-1] = current
            # Otherwise keep prev
            else:
                pass
        else:
            merged.append(current)

    # Convert to schema Finding models and reassign IDs
    result = []
    for idx, f in enumerate(merged):
        f["id"] = f"finding_{idx}"
        result.append(Finding(**f))

    return result

def generate_sanitized_prompt(prompt: str, findings: List[Finding], actions: Dict[str, str] = None) -> str:
    """
    Applies sanitization based on user action overrides.
    actions map: finding_id -> "replace" | "remove" | "keep"
    Default action is "replace".
    """
    if not findings:
        return prompt

    if actions is None:
        actions = {}

    # Sort findings by start descending so string replacements don't corrupt indices
    sorted_findings = sorted(findings, key=lambda x: x.start, reverse=True)

    sanitized = prompt
    for f in sorted_findings:
        action = actions.get(f.id, "replace")
        if action == "keep":
            continue
        elif action == "remove":
            sanitized = sanitized[:f.start] + sanitized[f.end:]
        else:  # "replace"
            replacement = f.placeholder
            sanitized = sanitized[:f.start] + replacement + sanitized[f.end:]

    return sanitized
