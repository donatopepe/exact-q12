import exactq12_pkg::*;

module instruction_decoder_tb;

    logic [23:0] instr;
    logic [7:0] opcode;
    logic [7:0] arg0;
    logic [7:0] arg1;
    logic valid;
    logic uses_arg0;
    logic uses_arg1;

    instruction_decoder dut (
        .instr(instr),
        .opcode(opcode),
        .arg0(arg0),
        .arg1(arg1),
        .valid(valid),
        .uses_arg0(uses_arg0),
        .uses_arg1(uses_arg1)
    );

    initial begin
        instr = {OP_H, 8'h02, 8'h00};
        #1;
        if (!valid || opcode !== OP_H || arg0 !== 8'h02 || arg1 !== 8'h00) $fatal(1, "H decode mismatch");
        if (!uses_arg0 || uses_arg1) $fatal(1, "H arg usage mismatch");

        instr = {OP_CNOT, 8'h00, 8'h01};
        #1;
        if (!valid || opcode !== OP_CNOT || arg0 !== 8'h00 || arg1 !== 8'h01) $fatal(1, "CNOT decode mismatch");
        if (!uses_arg0 || !uses_arg1) $fatal(1, "CNOT arg usage mismatch");

        instr = {OP_DUMP, 8'h00, 8'h00};
        #1;
        if (!valid || uses_arg0 || uses_arg1) $fatal(1, "DUMP decode mismatch");

        instr = 24'hff0000;
        #1;
        if (valid) $fatal(1, "invalid opcode accepted");

        $display("instruction_decoder_tb passed");
        $finish;
    end

endmodule
