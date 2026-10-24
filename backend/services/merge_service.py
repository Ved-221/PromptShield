import re
from typing import List, Dict, Any, Optional
from schemas import Finding
from services.placeholders import get_placeholder

SEVERITY_ORDER = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

SEVERITY_NAMES = {v: k for k, v in SEVERITY_ORDER.items()}

def merge_findings(raw_findings: List[Dict[str, Any]], prompt: str = "") -> List[Finding]:
    """
    Unions overlapping and adjacent-overlapping findings into single non-overlapping spans.
    Preserves highest severity, highest confidence, dominant entity attributes,
    and joins contributing detector sources.
    """
    if not raw_findings:
        return []

    # Sort primarily by start ASC, then end DESC
    def sort_key(item: Dict[str, Any]):
        return (item["start"], -item["end"])

    sorted_raw = sorted(raw_findings, key=sort_key)

    # Group overlapping or adjacent spans into clusters
    clusters: List[List[Dict[str, Any]]] = []
    current_cluster: List[Dict[str, Any]] = []
    current_cluster_end = -1

    for f in sorted_raw:
        if not current_cluster:
            current_cluster = [f]
            current_cluster_end = f["end"]
            continue

        # Overlapping or adjacent: start <= current_cluster_end
        if f["start"] <= current_cluster_end:
            current_cluster.append(f)
            current_cluster_end = max(current_cluster_end, f["end"])
        else:
            clusters.append(current_cluster)
            current_cluster = [f]
            current_cluster_end = f["end"]

    if current_cluster:
        clusters.append(current_cluster)

    # Resolve each cluster into a single unioned Finding
    result: List[Finding] = []
    for idx, cluster in enumerate(clusters):
        start = min(f["start"] for f in cluster)
        end = max(f["end"] for f in cluster)

        # Determine highest severity
        max_sev_rank = max(SEVERITY_ORDER.get(f.get("risk_level", "Low"), 1) for f in cluster)
        risk_level = SEVERITY_NAMES.get(max_sev_rank, "Low")

        # Determine highest confidence
        max_confidence = round(max(float(f.get("confidence", 0.0)) for f in cluster), 2)

        # Determine dominant finding for type, category, placeholder, reason, recommendation
        # Priority: highest severity, then highest confidence, then longest span
        def dominant_key(item: Dict[str, Any]):
            sev_rank = SEVERITY_ORDER.get(item.get("risk_level", "Low"), 1)
            conf = float(item.get("confidence", 0.0))
            span_len = item["end"] - item["start"]
            return (sev_rank, conf, span_len)

        dominant = max(cluster, key=dominant_key)

        # Collect unique contributing detector sources
        sources: List[str] = []
        seen_sources = set()
        for f in cluster:
            src = f.get("source", "Engine")
            for part in str(src).split(" + "):
                part_clean = part.strip()
                if part_clean and part_clean not in seen_sources:
                    seen_sources.add(part_clean)
                    sources.append(part_clean)
        joined_source = " + ".join(sources) if sources else "Engine"

        # Reconstruct text from prompt if available
        if prompt and 0 <= start < end <= len(prompt):
            text = prompt[start:end]
        else:
            text = dominant.get("text", "")

        dominant_type = dominant.get("type", "UNKNOWN")
        placeholder = get_placeholder(dominant_type)

        result.append(
            Finding(
                id=f"finding_{idx}",
                text=text,
                type=dominant_type,
                category=dominant.get("category", "General"),
                start=start,
                end=end,
                confidence=max_confidence,
                risk_level=risk_level,
                reason=dominant.get("reason", "Detected sensitive information."),
                recommendation=dominant.get("recommendation", "Review and redact sensitive content."),
                placeholder=placeholder,
                source=joined_source
            )
        )

    return result

def generate_sanitized_prompt(
    prompt: str,
    findings: List[Finding],
    actions: Optional[Dict[str, str]] = None
) -> str:
    """
    Applies sanitization based on user action overrides ('replace', 'remove', 'keep').
    Validates finding bounds and non-overlapping invariants.
    Ignores client placeholder/text and enforces server-side allowlist.
    Normalizes whitespace on 'remove' actions.
    """
    if not findings:
        return prompt

    if actions is None:
        actions = {}

    # Sort ascending by start position
    sorted_findings = sorted(findings, key=lambda x: x.start)

    # Validate offsets and overlap invariants
    for i, f in enumerate(sorted_findings):
        if not (0 <= f.start < f.end <= len(prompt)):
            raise ValueError(
                f"Invalid finding bounds [{f.start}, {f.end}) for prompt length {len(prompt)}"
            )
        if i > 0 and f.start < sorted_findings[i - 1].end:
            raise ValueError(
                f"Overlapping findings detected between {sorted_findings[i-1].id} and {f.id}"
            )

    pieces: List[str] = []
    last_idx = 0

    for f in sorted_findings:
        action = actions.get(f.id, "replace")
        prefix = prompt[last_idx:f.start]

        if action == "keep":
            pieces.append(prefix)
            pieces.append(prompt[f.start:f.end])
            last_idx = f.end
        elif action == "replace":
            pieces.append(prefix)
            pieces.append(get_placeholder(f.type))
            last_idx = f.end
        elif action == "remove":
            # Whitespace normalization around removed span
            after_is_space = (f.end < len(prompt) and prompt[f.end].isspace())
            before_is_space = (len(prefix) > 0 and prefix[-1].isspace())

            if before_is_space and after_is_space:
                # Collapse trailing space from prefix so adjoining words don't have double space
                pieces.append(prefix.rstrip(" "))
                last_idx = f.end
            elif before_is_space and f.end == len(prompt):
                # Removed at the very end of prompt
                pieces.append(prefix.rstrip(" "))
                last_idx = f.end
            elif f.start == 0 and after_is_space:
                # Removed at the very start of prompt: skip immediate trailing spaces
                pieces.append(prefix)
                idx = f.end
                while idx < len(prompt) and prompt[idx] == " ":
                    idx += 1
                last_idx = idx
            else:
                pieces.append(prefix)
                last_idx = f.end

    if last_idx < len(prompt):
        pieces.append(prompt[last_idx:])

    output = "".join(pieces)
    # Collapse multiple consecutive spaces
    output = re.sub(r"[ ]{2,}", " ", output)
    if not prompt.startswith(" "):
        output = output.lstrip(" ")
    if not prompt.endswith(" "):
        output = output.rstrip(" ")
    return output
