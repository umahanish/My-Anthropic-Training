"""The five course contracts and the reference risk rule every lab is graded against."""
from datetime import date, timedelta

from common import TODAY

CONTRACTS = [
    {"vendor": "Nimbus Cloud Services", "ref": "NCS-2025-0142", "end": "2026-09-25", "notice_days": 30, "auto_renews": True, "annual_value": 63000},
    {"vendor": "BrightPath Security Solutions", "ref": "BPS-2025-0087", "end": "2026-10-10", "notice_days": 45, "auto_renews": True, "annual_value": 24000},
    {"vendor": "Vertex Networking Group", "ref": "VNG-2025-0219", "end": "2026-11-05", "notice_days": 60, "auto_renews": True, "annual_value": 19500},
    {"vendor": "Alderwood Office Supplies", "ref": "AOS-2025-0033", "end": "2026-12-15", "notice_days": 60, "auto_renews": True, "annual_value": 4200},
    {"vendor": "Fixed-Term Consulting LLC", "ref": "FTC-2025-0061", "end": "2026-09-20", "notice_days": 0, "auto_renews": False, "annual_value": 47000},
]

RISK_RULE = """Risk rule (apply exactly):
- cancellation_deadline = end date minus notice days.
- days_until_deadline = cancellation_deadline minus today, in calendar days.
- Does not auto-renew -> LOW.
- Auto-renews and days_until_deadline < 0 -> HIGH (deadline missed).
- Auto-renews and 0 <= days_until_deadline <= 30 -> HIGH.
- Auto-renews and 31 <= days_until_deadline <= 60 -> MEDIUM.
- Otherwise -> LOW."""


def describe(c: dict) -> str:
    renew = f"auto-renews unless cancelled {c['notice_days']} days before the end date" if c["auto_renews"] else "fixed term, does not auto-renew"
    return f"{c['vendor']} (ref {c['ref']}), ends {c['end']}, {renew}, annual value ${c['annual_value']:,}."


def expected(c: dict, today: str = TODAY) -> dict:
    """Ground truth computed in code: the answer key for every eval."""
    end = date.fromisoformat(c["end"])
    deadline = end - timedelta(days=c["notice_days"])
    days = (deadline - date.fromisoformat(today)).days
    if not c["auto_renews"]:
        risk = "LOW"
    elif days <= 30:
        risk = "HIGH"
    elif days <= 60:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    return {
        "vendor": c["vendor"],
        "cancellation_deadline": deadline.isoformat() if c["auto_renews"] else None,
        "days_until_deadline": days if c["auto_renews"] else None,
        "risk": risk,
    }


def find(text: str) -> dict | None:
    for c in CONTRACTS:
        if c["vendor"] in text or c["ref"] in text:
            return c
    return None
