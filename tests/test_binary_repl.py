import subprocess
import sys
from io import StringIO

import pytest

from exactq12.binary import decode_instructions, decode_memh, encode_instructions, encode_memh, export_binary, export_memh, run_binary, run_memh
from exactq12.complex_q12 import CQ12
from exactq12.parser import Instruction, parse_text
from exactq12.q12 import Q12
from exactq12.repl import repl


def test_binary_roundtrip_preserves_instructions() -> None:
    instructions = parse_text("""
RESET 2
H q0
CNOT q0 q1
DUMP
PROB
""")
    payload = encode_instructions(instructions)
    assert payload == bytes([0x00, 0x02, 0x00, 0x03, 0x00, 0x00, 0x08, 0x00, 0x01, 0x0A, 0x00, 0x00, 0x0B, 0x00, 0x00])
    assert decode_instructions(payload) == instructions


def test_binary_rejects_invalid_payload() -> None:
    with pytest.raises(ValueError, match="multiple of 3"):
        decode_instructions(b"\x00\x01")
    with pytest.raises(ValueError, match="unknown binary opcode"):
        decode_instructions(b"\xff\x00\x00")
    with pytest.raises(ValueError, match="one byte"):
        encode_instructions([Instruction("H", (256,))])


def test_export_binary_and_run_binary(tmp_path) -> None:
    source = tmp_path / "bell.q12"
    output = tmp_path / "bell.bin"
    source.write_text("RESET 2\nH q0\nCNOT q0 q1\nDUMP\n", encoding="utf-8")

    byte_count = export_binary(source, output)
    assert byte_count == 12

    state, dump = run_binary(output)
    bell = CQ12(Q12.sqrt2_half(), Q12.zero())
    assert state.amplitudes == [bell, CQ12.zero(), CQ12.zero(), bell]
    assert dump[0].startswith("|00> = ")


def test_export_memh_matches_instruction_hex(tmp_path) -> None:
    source = tmp_path / "bell.q12"
    output = tmp_path / "bell.memh"
    source.write_text("RESET 2\nH q0\nCNOT q0 q1\nDUMP\nPROB\n", encoding="utf-8")
    instructions = parse_text(source.read_text(encoding="utf-8"))

    instruction_count = export_memh(source, output)
    assert instruction_count == 5
    assert output.read_text(encoding="utf-8") == encode_memh(instructions)
    assert decode_memh(output.read_text(encoding="utf-8")) == instructions


def test_run_memh_executes_instruction_hex(tmp_path) -> None:
    output = tmp_path / "bell.memh"
    output.write_text("000200\n030000\n080001\n0a0000\n", encoding="utf-8")
    state, dump = run_memh(output)
    bell = CQ12(Q12.sqrt2_half(), Q12.zero())
    assert state.amplitudes == [bell, CQ12.zero(), CQ12.zero(), bell]
    assert dump[0].startswith("|00> = ")


def test_repl_executes_incremental_program() -> None:
    output = StringIO()
    repl(StringIO("RESET 1\nH q0\nDUMP\nQUIT\n"), output)
    text = output.getvalue()
    assert "|0>" in text
    assert "|1>" in text


def test_repl_reports_errors_and_continues() -> None:
    output = StringIO()
    repl(StringIO("H q0\nRESET 1\nDUMP\n"), output)
    text = output.getvalue()
    assert "ERROR:" in text
    assert "|0>" in text


def test_cli_export_and_fpga_run(tmp_path) -> None:
    source = tmp_path / "bell.q12"
    output = tmp_path / "bell.bin"
    source.write_text("RESET 2\nH q0\nCNOT q0 q1\nDUMP\n", encoding="utf-8")

    export_completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "export", str(source), "--format", "bin", "--out", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "wrote 12 bytes" in export_completed.stdout

    run_completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "fpga", "run", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "|00>" in run_completed.stdout
    assert "|11>" in run_completed.stdout


def test_cli_export_memh(tmp_path) -> None:
    source = tmp_path / "bell.q12"
    output = tmp_path / "bell.memh"
    source.write_text("RESET 2\nH q0\nCNOT q0 q1\nDUMP\n", encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "export", str(source), "--format", "memh", "--out", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "wrote 4 instructions" in completed.stdout
    assert output.read_text(encoding="utf-8").splitlines() == ["000200", "030000", "080001", "0a0000"]


def test_cli_fpga_run_accepts_memh(tmp_path) -> None:
    output = tmp_path / "bell.memh"
    output.write_text("000200\n030000\n080001\n0a0000\n", encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "fpga", "run", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "|00>" in completed.stdout
    assert "|11>" in completed.stdout


def test_cli_state_init_exports_reset_memh(tmp_path) -> None:
    output = tmp_path / "reset2.memh"
    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "state-init", "--qubits", "2", "--out", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = output.read_text(encoding="utf-8").splitlines()
    assert "wrote 4 amplitudes" in completed.stdout
    assert len(lines) == 4
    assert int(lines[0], 16) != 0
    assert lines[1:] == ["0" * len(lines[0])] * 3


def test_cli_dump_prints_final_state_without_dump_instruction(tmp_path) -> None:
    source = tmp_path / "state.q12"
    source.write_text("RESET 1\nH q0\n", encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-m", "exactq12.cli", "dump", str(source)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "|0>" in completed.stdout
    assert "|1>" in completed.stdout
