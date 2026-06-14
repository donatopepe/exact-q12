module hadamard_pair_repack_tb;

    localparam int IN_COEFF_W = 12;
    localparam int OUT_COEFF_W = 8;
    localparam int EXP_W = 4;
    localparam int IN_AMP_W = (8 * IN_COEFF_W) + (2 * EXP_W);
    localparam int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W);

    logic [IN_AMP_W-1:0] amp_in0;
    logic [IN_AMP_W-1:0] amp_in1;
    logic [OUT_AMP_W-1:0] amp_out0;
    logic [OUT_AMP_W-1:0] amp_out1;
    logic valid;

    hadamard_pair_repack #(
        .IN_COEFF_W(IN_COEFF_W),
        .OUT_COEFF_W(OUT_COEFF_W),
        .EXP_W(EXP_W)
    ) dut (
        .amp_in0(amp_in0),
        .amp_in1(amp_in1),
        .amp_out0(amp_out0),
        .amp_out1(amp_out1),
        .valid(valid)
    );

    initial begin
        amp_in0 = {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1};
        amp_in1 = {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1};
        #1;
        if (!valid) $fatal(1, "repack rejected fitting coefficients");
        if (amp_out0 !== {8'sd0, 8'sd6, 8'sd0, 8'sd0, 4'd1, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd1}) $fatal(1, "repack out0 mismatch");
        if (amp_out1 !== {8'sd0, 8'sd6, 8'sd0, 8'sd0, 4'd1, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd1}) $fatal(1, "repack out1 mismatch");

        amp_in1 = {12'sd128, 12'sd0, 12'sd0, 12'sd0, 4'd0, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd0};
        #1;
        if (valid) $fatal(1, "repack accepted positive overflow");

        amp_in1 = {-12'sd129, 12'sd0, 12'sd0, 12'sd0, 4'd0, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd0};
        #1;
        if (valid) $fatal(1, "repack accepted negative overflow");

        $display("hadamard_pair_repack_tb passed");
        $finish;
    end

endmodule
