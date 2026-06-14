# EXACT-Q12 RTL

This directory contains the first hardware-oriented SystemVerilog building blocks.

Current modules:

- `exactq12_pkg.sv`: shared opcode constants matching the Python binary encoder.
- `instruction_decoder.sv`: combinational decoder for 24-bit `[opcode][arg0][arg1]` instructions.
- `program_rom.sv`: generic 24-bit instruction ROM loaded with `$readmemh`.
- `statevector_mem.sv`: synchronous memory for packed `CQ12` amplitudes.
- `statevector_pair_mem.sv`: synchronous two-read/two-write memory for amplitude pairs.
- `exactq12_sequencer.sv`: first fetch/decode/halt sequencer skeleton.
- `exactq12_top.sv`: simulation-oriented shell wiring ROM, sequencer, and state memory.
- `q12_add.sv`: combinational add/subtract for `Q12` values with already aligned exponents.
- `q12_complex_add.sv`: combinational add/subtract for `CQ12` values using two `q12_add` instances.
- `q12_add_aligned.sv`: combinational `Q12` add/subtract with limited scaling to `12^max(E0,E1)`.
- `q12_complex_add_aligned.sv`: combinational `CQ12` add/subtract with independent real and imaginary exponent alignment.
- `q12_scale_sqrt_half.sv`: exact multiply by `√2/2 = 6√2/12`.
- `q12_complex_scale_sqrt_half.sv`: `CQ12` scaling by `√2/2`.
- `hadamard_address_pair.sv`: address pair generator for Hadamard traversal using `q0` as the most-significant qubit.
- `hadamard_pair.sv`: combinational Hadamard butterfly over two `CQ12` amplitudes in unpacked fields.
- `hadamard_pair_packed.sv`: wrapper around `hadamard_pair` for packed `CQ12` memory payloads.
- `hadamard_pair_repack.sv`: wide-to-memory payload repacker with signed coefficient fit checks.
- `hadamard_pair_step.sv`: combinational address/read-payload/write-payload step for one Hadamard pair.
- `hadamard_pair_writeback_step.sv`: Hadamard pair step with writeback payloads repacked to memory width.
- `q12_mul.sv`: combinational multiplication for `a + b√2 + c√3 + d√6` numerators.
- `q12_complex_mul.sv`: combinational complex multiplication using four `q12_mul` instances.
- `q12_den_reduce.sv`: one-step denominator reduction by base 12.
- `bell.memh`: binary Bell program in ROM hex format.
- `README_TOP.md`: top-level limitations and integration notes.
- `tb/`: optional self-checking SystemVerilog testbenches.
- `Makefile`: optional Icarus Verilog simulation targets.

Python helpers:

- `exactq12 export --format memh` writes ROM-compatible 24-bit instruction hex.
- `exactq12.rtl_pack` packs and unpacks `Q12`/`CQ12` values using the same field order expected by `statevector_mem.sv`.

The sequencer currently decodes instructions and halts on `DUMP` or invalid opcodes. The top-level wires memory and control blocks together for future HDL simulation, but it does not yet execute gate datapaths over statevector memory. These modules do not yet implement a complete datapath, UART, board constraints, or Tang Nano 20K integration. The Python model remains the reference implementation.

Optional local HDL simulation:

```bash
make -C rtl sim
```

This requires `iverilog` and `vvp` to be installed locally. It is not required by the Python test suite or CI yet.
