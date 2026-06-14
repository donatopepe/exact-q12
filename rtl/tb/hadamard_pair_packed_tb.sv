module hadamard_pair_packed_tb;

    localparam int COEFF_W = 8;
    localparam int EXP_W = 4;
    localparam int ADD_W = 16;
    localparam int OUT_COEFF_W = 12;
    localparam int AMP_W = (8 * COEFF_W) + (2 * EXP_W);
    localparam int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W);

    logic [AMP_W-1:0] amp_in0;
    logic [AMP_W-1:0] amp_in1;
    logic [OUT_AMP_W-1:0] amp_out0;
    logic [OUT_AMP_W-1:0] amp_out1;
    logic valid;

    hadamard_pair_packed #(
        .COEFF_W(COEFF_W),
        .EXP_W(EXP_W),
        .ADD_W(ADD_W),
        .OUT_COEFF_W(OUT_COEFF_W),
        .MAX_SHIFT(2)
    ) dut (
        .amp_in0(amp_in0),
        .amp_in1(amp_in1),
        .amp_out0(amp_out0),
        .amp_out1(amp_out1),
        .valid(valid)
    );

    initial begin
        amp_in0 = {8'sd1, 8'sd0, 8'sd0, 8'sd0, 4'd0, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        amp_in1 = {8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        #1;
        if (!valid) $fatal(1, "packed hadamard basis valid mismatch");
        if (amp_out0 !== {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1}) $fatal(1, "packed hadamard out0 mismatch");
        if (amp_out1 !== {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1}) $fatal(1, "packed hadamard out1 mismatch");

        amp_in0 = {8'sd1, 8'sd0, 8'sd0, 8'sd0, 4'd0, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        amp_in1 = {8'sd1, 8'sd0, 8'sd0, 8'sd0, 4'd3, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        #1;
        if (valid) $fatal(1, "packed hadamard accepted exponent gap beyond MAX_SHIFT");

        $display("hadamard_pair_packed_tb passed");
        $finish;
    end

endmodule
