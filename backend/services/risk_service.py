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

    total_penalty = 0
    crit_cnt = 0
    high_cnt = 0
    med_cnt = 0
    low_cnt = 0
    by_cat: Dict[str, int] = {}

    for f in findings:
        sev = f.risk_level
        total_penalty += PENALTIES.get(sev, 5)

        if sev == "Critical":
            crit_cnt += 1
        elif sev == "High":
            high_cnt += 1
        elif sev == "Medium":
            med_cnt += 1
        else:
            low_cnt += 1

        cat = f.category
        by_cat[cat] = by_cat.get(cat, 0) + 1

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
        by_category=by_cat
    )

    return score, overall_risk, stats
