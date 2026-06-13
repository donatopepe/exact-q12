# EXACT-Q12

EXACT-Q12 is an exact symbolic quantum circuit simulator using values in
`Q(sqrt(2), sqrt(3))` represented as:

```text
(a + b√2 + c√3 + d√6) / 12^E
```

Phase 1 implements the Python model, parser, CLI `run`, and pytest coverage for
the required exact gates.
