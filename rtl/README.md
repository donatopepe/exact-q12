# EXACT-Q12 RTL

This directory contains the first hardware-oriented SystemVerilog building blocks.

Current modules:

- `q12_mul.sv`: combinational multiplication for `a + b√2 + c√3 + d√6` numerators.
- `q12_complex_mul.sv`: combinational complex multiplication using four `q12_mul` instances.

These modules do not yet implement denominator reduction, statevector memory, sequencing, UART, board constraints, or Tang Nano 20K integration. The Python model remains the reference implementation.
