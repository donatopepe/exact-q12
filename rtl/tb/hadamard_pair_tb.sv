module hadamard_pair_tb;

    logic signed [31:0] ar0;
    logic signed [31:0] br0;
    logic signed [31:0] cr0;
    logic signed [31:0] dr0;
    logic [7:0] er0;
    logic signed [31:0] ai0;
    logic signed [31:0] bi0;
    logic signed [31:0] ci0;
    logic signed [31:0] di0;
    logic [7:0] ei0;
    logic signed [31:0] ar1;
    logic signed [31:0] br1;
    logic signed [31:0] cr1;
    logic signed [31:0] dr1;
    logic [7:0] er1;
    logic signed [31:0] ai1;
    logic signed [31:0] bi1;
    logic signed [31:0] ci1;
    logic signed [31:0] di1;
    logic [7:0] ei1;

    logic signed [67:0] ar_out0;
    logic signed [67:0] br_out0;
    logic signed [67:0] cr_out0;
    logic signed [67:0] dr_out0;
    logic [7:0] er_out0;
    logic signed [67:0] ai_out0;
    logic signed [67:0] bi_out0;
    logic signed [67:0] ci_out0;
    logic signed [67:0] di_out0;
    logic [7:0] ei_out0;
    logic signed [67:0] ar_out1;
    logic signed [67:0] br_out1;
    logic signed [67:0] cr_out1;
    logic signed [67:0] dr_out1;
    logic [7:0] er_out1;
    logic signed [67:0] ai_out1;
    logic signed [67:0] bi_out1;
    logic signed [67:0] ci_out1;
    logic signed [67:0] di_out1;
    logic [7:0] ei_out1;
    logic valid;

    hadamard_pair dut (
        .ar0(ar0), .br0(br0), .cr0(cr0), .dr0(dr0), .er0(er0),
        .ai0(ai0), .bi0(bi0), .ci0(ci0), .di0(di0), .ei0(ei0),
        .ar1(ar1), .br1(br1), .cr1(cr1), .dr1(dr1), .er1(er1),
        .ai1(ai1), .bi1(bi1), .ci1(ci1), .di1(di1), .ei1(ei1),
        .ar_out0(ar_out0), .br_out0(br_out0), .cr_out0(cr_out0), .dr_out0(dr_out0), .er_out0(er_out0),
        .ai_out0(ai_out0), .bi_out0(bi_out0), .ci_out0(ci_out0), .di_out0(di_out0), .ei_out0(ei_out0),
        .ar_out1(ar_out1), .br_out1(br_out1), .cr_out1(cr_out1), .dr_out1(dr_out1), .er_out1(er_out1),
        .ai_out1(ai_out1), .bi_out1(bi_out1), .ci_out1(ci_out1), .di_out1(di_out1), .ei_out1(ei_out1),
        .valid(valid)
    );

    initial begin
        ar0 = 32'sd1; br0 = 32'sd0; cr0 = 32'sd0; dr0 = 32'sd0; er0 = 8'd0;
        ai0 = 32'sd0; bi0 = 32'sd0; ci0 = 32'sd0; di0 = 32'sd0; ei0 = 8'd0;
        ar1 = 32'sd0; br1 = 32'sd0; cr1 = 32'sd0; dr1 = 32'sd0; er1 = 8'd0;
        ai1 = 32'sd0; bi1 = 32'sd0; ci1 = 32'sd0; di1 = 32'sd0; ei1 = 8'd0;
        #1;
        if (!valid) $fatal(1, "hadamard basis valid mismatch");
        if (ar_out0 !== 68'sd0 || br_out0 !== 68'sd6 || cr_out0 !== 68'sd0 || dr_out0 !== 68'sd0 || er_out0 !== 8'd1) $fatal(1, "hadamard basis out0 real mismatch");
        if (ar_out1 !== 68'sd0 || br_out1 !== 68'sd6 || cr_out1 !== 68'sd0 || dr_out1 !== 68'sd0 || er_out1 !== 8'd1) $fatal(1, "hadamard basis out1 real mismatch");
        if (ai_out0 !== 68'sd0 || bi_out0 !== 68'sd0 || ci_out0 !== 68'sd0 || di_out0 !== 68'sd0) $fatal(1, "hadamard basis out0 imag mismatch");
        if (ai_out1 !== 68'sd0 || bi_out1 !== 68'sd0 || ci_out1 !== 68'sd0 || di_out1 !== 68'sd0) $fatal(1, "hadamard basis out1 imag mismatch");

        ar0 = 32'sd3; br0 = -32'sd2; cr0 = 32'sd4; dr0 = -32'sd5; er0 = 8'd1;
        ai0 = 32'sd1; bi0 = 32'sd2; ci0 = 32'sd3; di0 = 32'sd4; ei0 = 8'd2;
        ar1 = -32'sd1; br1 = 32'sd7; cr1 = -32'sd3; dr1 = 32'sd2; er1 = 8'd3;
        ai1 = 32'sd5; bi1 = -32'sd6; ci1 = 32'sd7; di1 = -32'sd8; ei1 = 8'd1;
        #1;
        if (!valid) $fatal(1, "hadamard general valid mismatch");
        if (ar_out0 !== -68'sd3372 || br_out0 !== 68'sd2586 || cr_out0 !== -68'sd8616 || dr_out0 !== 68'sd3438 || er_out0 !== 8'd4) $fatal(1, "hadamard general out0 real mismatch");
        if (ai_out0 !== -68'sd840 || bi_out0 !== 68'sd366 || ci_out0 !== -68'sd1104 || di_out0 !== 68'sd522 || ei_out0 !== 8'd3) $fatal(1, "hadamard general out0 imag mismatch");
        if (ar_out1 !== -68'sd3540 || br_out1 !== 68'sd2598 || cr_out1 !== -68'sd8664 || dr_out1 !== 68'sd3474 || er_out1 !== 8'd4) $fatal(1, "hadamard general out1 real mismatch");
        if (ai_out1 !== 68'sd888 || bi_out1 !== -68'sd354 || ci_out1 !== 68'sd1200 || di_out1 !== -68'sd486 || ei_out1 !== 8'd3) $fatal(1, "hadamard general out1 imag mismatch");

        er0 = 8'd0;
        er1 = 8'd6;
        #1;
        if (valid) $fatal(1, "hadamard accepted exponent gap beyond MAX_SHIFT");

        $display("hadamard_pair_tb passed");
        $finish;
    end

endmodule
