# Sample Repo — Failing Test

Used for Lab 2.1, task card 3: `"Fix the failing test in this repository."`

This is a two-file sample: `contract_alerts.py` contains a small utility with
one deliberate off-by-one bug, and `test_contract_alerts.py` is a pytest
suite that catches it.

Run it yourself first, so you can see exactly what a student will see:

```
pip install pytest
pytest -v
```

One test fails (`test_days_until_basic`), two pass. The fix is a one-line
change in `days_until()`.

This is a fictional sample created for AI training purposes only.
