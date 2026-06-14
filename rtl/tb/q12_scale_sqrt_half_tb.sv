module q12_scale_sqrt_half_tb;

    logic signed [31:0] a_in;
    logic signed [31:0] b_in;
    logic signed [31:0] c_in;
    logic signed [31:0] d_in;
    logic [7:0] e_in;
    logic signed [35:0] a_out;
    logic signed [35:0] b_out;
    logic signed [35:0] c_out;
    logic signed [35:0] d_out;
    logic [7:0] e_out;

    q12_scale_sqrt_half #(.W(32), .EW(8), .OUT_W(36)) dut (
        .a_in(a_in), .b_in(b_in), .c_in(c_in), .d_in(d_in), .e_in(e_in),
        .a_out(a_out), .b_out(b_out), .c_out(c_out), .d_out(d_out), .e_out(e_out)
    );

    initial begin
        a_in = 32'sd1; b_in = 32'sd0; c_in = 32'sd0; d_in = 32'sd0; e_in = 8'd0;
        #1;
        if (a_out !== 36'sd0 || b_out !== 36'sd6 || c_out !== 36'sd0 || d_out !== 36'sd0 || e_out !== 8'd1) $fatal(1, "sqrt half one mismatch");

        a_in = 32'sd3; b_in = -32'sd2; c_in = 32'sd4; d_in = -32'sd5; e_in = 8'd2;
        #1;
        if (a_out !== -36'sd24 || b_out !== 36'sd18 || c_out !== -36'sd60 || d_out !== 36'sd24 || e_out !== 8'd3) $fatal(1, "sqrt half general mismatch");

        $display("q12_scale_sqrt_half_tb passed");
        $finish;
    end

endmodule
