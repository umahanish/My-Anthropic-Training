from datetime import date

from contract_alerts import days_until, needs_renewal_notice


def test_days_until_basic():
    # There are 10 days between August 1 and August 11.
    assert days_until(date(2026, 8, 11), date(2026, 8, 1)) == 10


def test_needs_renewal_notice_true_on_boundary():
    # Exactly on the notice-day boundary should count as needing notice.
    assert needs_renewal_notice(date(2026, 8, 31), 30, date(2026, 8, 1)) is True


def test_needs_renewal_notice_false_outside_window():
    assert needs_renewal_notice(date(2026, 10, 1), 30, date(2026, 8, 1)) is False
