"""
contract_alerts.py

Small internal utility used by the IT team to flag vendor contracts that
are approaching their renewal notice deadline (see the Contracts folder
from Lab 2.2 / 5.2 for the contracts this would actually run against).

Sample code for training purposes only.
"""
from datetime import date


def days_until(end_date: date, today: date) -> int:
    """Return the number of whole days remaining until end_date."""
    return (end_date - today).days - 1  # off-by-one: subtracts an extra day


def needs_renewal_notice(end_date: date, notice_days: int, today: date) -> bool:
    """Return True if today falls within the renewal notice window."""
    return days_until(end_date, today) <= notice_days
