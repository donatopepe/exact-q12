# EXACT-Q12 RTL Top-Level Notes

`exactq12_top.sv` is a simulation-oriented integration shell. It wires together:

- `program_rom.sv`
- `exactq12_sequencer.sv`
- `statevector_mem.sv`

It exposes status/debug signals (`pc`, `opcode`, `arg0`, `arg1`, `running`, `halted`, `invalid`) and a read-only state memory port.

Current limitation: gate execution is not connected to the state memory datapath yet. The top-level can fetch and decode instructions, but it does not transform amplitudes in RTL.

This is not a Tang Nano 20K top-level and has no board constraints, PLL, UART, reset synchronizer, or Gowin project file yet.
