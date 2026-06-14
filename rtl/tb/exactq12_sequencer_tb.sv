import exactq12_pkg::*;

module exactq12_sequencer_tb;

    logic clk;
    logic rst;
    logic start;
    logic [23:0] instr;
    logic [7:0] pc;
    logic running;
    logic halted;
    logic invalid;
    logic [7:0] opcode;
    logic [7:0] arg0;
    logic [7:0] arg1;

    exactq12_sequencer dut (
        .clk(clk),
        .rst(rst),
        .start(start),
        .instr(instr),
        .pc(pc),
        .running(running),
        .halted(halted),
        .invalid(invalid),
        .opcode(opcode),
        .arg0(arg0),
        .arg1(arg1)
    );

    always #5 clk = ~clk;

    always_comb begin
        unique case (pc)
            8'd0: instr = {OP_RESET, 8'h02, 8'h00};
            8'd1: instr = {OP_H, 8'h00, 8'h00};
            8'd2: instr = {OP_CNOT, 8'h00, 8'h01};
            8'd3: instr = {OP_DUMP, 8'h00, 8'h00};
            default: instr = 24'hff0000;
        endcase
    end

    initial begin
        clk = 1'b0;
        rst = 1'b1;
        start = 1'b0;
        repeat (2) @(posedge clk);
        rst = 1'b0;
        start = 1'b1;

        repeat (12) @(posedge clk);
        if (!halted) $fatal(1, "sequencer did not halt");
        if (invalid) $fatal(1, "sequencer reported invalid for Bell program");
        if (pc !== 8'd3) $fatal(1, "sequencer halted at unexpected pc: %0d", pc);
        if (opcode !== OP_DUMP) $fatal(1, "sequencer did not halt on DUMP");

        start = 1'b0;
        repeat (2) @(posedge clk);
        $display("exactq12_sequencer_tb passed");
        $finish;
    end

endmodule
