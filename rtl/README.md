# EXACT-Q12 RTL

This directory contains the first hardware-oriented SystemVerilog building blocks.

Current modules:

- `exactq12_pkg.sv`: shared opcode constants matching the Python binary encoder.
- `instruction_decoder.sv`: combinational decoder for 24-bit `[opcode][arg0][arg1]` instructions.
- `program_rom.sv`: generic 24-bit instruction ROM loaded with `$readmemh`.
- `statevector_mem.sv`: synchronous memory for packed `CQ12` amplitudes.
- `exactq12_sequencer.sv`: first fetch/decode/halt sequencer skeleton.
- `q12_mul.sv`: combinational multiplication for `a + b√2 + c√3 + d√6` numerators.
- `q12_complex_mul.sv`: combinational complex multiplication using four `q12_mul` instances.
- `q12_den_reduce.sv`: one-step denominator reduction by base 12.
- `bell.memh`: binary Bell program in ROM hex format.

The sequencer currently decodes instructions and halts on `DUMP` or invalid opcodes. It does not yet execute gate datapaths over statevector memory. These modules do not yet implement a complete datapath, UART, board constraints, or Tang Nano 20K integration. The Python model remains the reference implementation.
