module q12_complex_add_aligned_tb;

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
    logic subtract;
    logic signed [63:0] ar_out;
    logic signed [63:0] br_out;
    logic signed [63:0] cr_out;
    logic signed [63:0] dr_out;
    logic [7:0] er_out;
    logic signed [63:0] ai_out;
    logic signed [63:0] bi_out;
    logic signed [63:0] ci_out;
    logic signed [63:0] di_out;
    logic [7:0] ei_out;
    logic valid;

    q12_complex_add_aligned #(.MAX_SHIFT(2)) dut (
        .ar0(ar0), .br0(br0), .cr0(cr0), .dr0(dr0), .er0(er0),
        .ai0(ai0), .bi0(bi0), .ci0(ci0), .di0(di0), .ei0(ei0),
        .ar1(ar1), .br1(br1), .cr1(cr1), .dr1(dr1), .er1(er1),
        .ai1(ai1), .bi1(bi1), .ci1(ci1), .di1(di1), .ei1(ei1),
        .subtract(subtract),
        .ar_out(ar_out), .br_out(br_out), .cr_out(cr_out), .dr_out(dr_out), .er_out(er_out),
        .ai_out(ai_out), .bi_out(bi_out), .ci_out(ci_out), .di_out(di_out), .ei_out(ei_out),
        .valid(valid)
    );

    initial begin
        ar0 = 32'sd3; br0 = -32'sd2; cr0 = 32'sd4; dr0 = -32'sd5; er0 = 8'd1;
        ai0 = 32'sd1; bi0 = 32'sd2; ci0 = 32'sd3; di0 = 32'sd4; ei0 = 8'd2;
        ar1 = -32'sd1; br1 = 32'sd7; cr1 = -32'sd3; dr1 = 32'sd2; er1 = 8'd3;
        ai1 = 32'sd5; bi1 = -32'sd6; ci1 = 32'sd7; di1 = -32'sd8; ei1 = 8'd1;
        subtract = 1'b0;
        #1;
        if (!valid || er_out !== 8'd3 || ei_out !== 8'd2) $fatal(1, "complex aligned valid/e mismatch");
        if (ar_out !== 64'sd431 || br_out !== -64'sd281 || cr_out !== 64'sd573 || dr_out !== -64'sd718) $fatal(1, "complex aligned real mismatch");
        if (ai_out !== 64'sd61 || bi_out !== -64'sd70 || ci_out !== 64'sd87 || di_out !== -64'sd92) $fatal(1, "complex aligned imag mismatch");

        er0 = 8'd0;
        er1 = 8'd3;
        #1;
        if (valid) $fatal(1, "complex aligned accepted invalid real gap");

        $display("q12_complex_add_aligned_tb passed");
        $finish;
    end

endmodule
