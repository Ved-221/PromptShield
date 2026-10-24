from collections import Counter
from typing import List, Tuple, Dict
from schemas import Finding, StatsSummary

PENALTIES = {
    "Critical": 25,
    "High": 15,
    "Medium": 8,
    "Low": 3
}

def compute_risk_score(findings: List[Finding]) -> Tuple[int, str, StatsSummary]:
    if not findings:
        empty_stats = StatsSummary(
            total_findings=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            by_category={}
        )
        return 100, "Safe", empty_stats

    sev_counts = Counter(f.risk_level for f in findings)
    crit_cnt = sev_counts["Critical"]
    high_cnt = sev_counts["High"]
    med_cnt = sev_counts["Medium"]
    low_cnt = sev_counts["Low"]

    total_penalty = sum(PENALTIES.get(f.risk_level, 5) for f in findings)
    score = max(0, 100 - total_penalty)

    if score >= 95 and not crit_cnt and not high_cnt:
        overall_risk = "Safe"
    elif score >= 80:
        overall_risk = "Low"
    elif score >= 60:
        overall_risk = "Medium"
    elif score >= 35:
        overall_risk = "High"
    else:
        overall_risk = "Critical"

    stats = StatsSummary(
        total_findings=len(findings),
        critical_count=crit_cnt,
        high_count=high_cnt,
        medium_count=med_cnt,
        low_count=low_cnt,
        by_category=dict(Counter(f.category for f in findings))
    )

    return score, overall_risk, stats
