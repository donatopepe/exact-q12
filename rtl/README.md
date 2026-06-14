# EXACT-Q12 RTL

This directory contains the first hardware-oriented SystemVerilog building blocks.

Current modules:

- `exactq12_pkg.sv`: shared opcode constants matching the Python binary encoder.
- `instruction_decoder.sv`: combinational decoder for 24-bit `[opcode][arg0][arg1]` instructions.
- `program_rom.sv`: generic 24-bit instruction ROM loaded with `$readmemh`.
- `statevector_mem.sv`: synchronous memory for packed `CQ12` amplitudes.
- `exactq12_sequencer.sv`: first fetch/decode/halt sequencer skeleton.
- `exactq12_top.sv`: simulation-oriented shell wiring ROM, sequencer, and state memory.
- `q12_mul.sv`: combinational multiplication for `a + b√2 + c√3 + d√6` numerators.
- `q12_complex_mul.sv`: combinational complex multiplication using four `q12_mul` instances.
- `q12_den_reduce.sv`: one-step denominator reduction by base 12.
- `bell.memh`: binary Bell program in ROM hex format.
- `README_TOP.md`: top-level limitations and integration notes.

Python helpers:

- `exactq12 export --format memh` writes ROM-compatible 24-bit instruction hex.
- `exactq12.rtl_pack` packs and unpacks `Q12`/`CQ12` values using the same field order expected by `statevector_mem.sv`.

The sequencer currently decodes instructions and halts on `DUMP` or invalid opcodes. The top-level wires memory and control blocks together for future HDL simulation, but it does not yet execute gate datapaths over statevector memory. These modules do not yet implement a complete datapath, UART, board constraints, or Tang Nano 20K integration. The Python model remains the reference implementation.
