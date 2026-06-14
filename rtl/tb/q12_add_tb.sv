module q12_add_tb;

    logic signed [31:0] a0;
    logic signed [31:0] b0;
    logic signed [31:0] c0;
    logic signed [31:0] d0;
    logic [7:0] e0;
    logic signed [31:0] a1;
    logic signed [31:0] b1;
    logic signed [31:0] c1;
    logic signed [31:0] d1;
    logic [7:0] e1;
    logic subtract;
    logic signed [32:0] a_out;
    logic signed [32:0] b_out;
    logic signed [32:0] c_out;
    logic signed [32:0] d_out;
    logic [7:0] e_out;
    logic valid;

    q12_add dut (
        .a0(a0), .b0(b0), .c0(c0), .d0(d0), .e0(e0),
        .a1(a1), .b1(b1), .c1(c1), .d1(d1), .e1(e1),
        .subtract(subtract),
        .a_out(a_out), .b_out(b_out), .c_out(c_out), .d_out(d_out), .e_out(e_out),
        .valid(valid)
    );

    initial begin
        a0 = 32'sd3; b0 = -32'sd2; c0 = 32'sd4; d0 = -32'sd5; e0 = 8'd2;
        a1 = -32'sd1; b1 = 32'sd7; c1 = -32'sd3; d1 = 32'sd2; e1 = 8'd2;
        subtract = 1'b0;
        #1;
        if (!valid || e_out !== 8'd2) $fatal(1, "add valid/e mismatch");
        if (a_out !== 33'sd2 || b_out !== 33'sd5 || c_out !== 33'sd1 || d_out !== -33'sd3) $fatal(1, "add result mismatch");

        subtract = 1'b1;
        #1;
        if (!valid || e_out !== 8'd2) $fatal(1, "sub valid/e mismatch");
        if (a_out !== 33'sd4 || b_out !== -33'sd9 || c_out !== 33'sd7 || d_out !== -33'sd7) $fatal(1, "sub result mismatch");

        e1 = 8'd3;
        #1;
        if (valid) $fatal(1, "mismatched exponents accepted");

        $display("q12_add_tb passed");
        $finish;
    end

endmodule
