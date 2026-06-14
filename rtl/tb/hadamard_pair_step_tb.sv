module hadamard_pair_step_tb;

    localparam int ADDR_W = 3;
    localparam int QUBIT_W = 8;
    localparam int COEFF_W = 8;
    localparam int EXP_W = 4;
    localparam int ADD_W = 16;
    localparam int OUT_COEFF_W = 12;
    localparam int AMP_W = (8 * COEFF_W) + (2 * EXP_W);
    localparam int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W);

    logic [ADDR_W-1:0] pair_index;
    logic [QUBIT_W-1:0] target_qubit;
    logic [AMP_W-1:0] amp_rdata0;
    logic [AMP_W-1:0] amp_rdata1;
    logic [ADDR_W-1:0] addr0;
    logic [ADDR_W-1:0] addr1;
    logic [OUT_AMP_W-1:0] amp_wdata0;
    logic [OUT_AMP_W-1:0] amp_wdata1;
    logic valid;

    hadamard_pair_step #(
        .ADDR_W(ADDR_W),
        .QUBIT_W(QUBIT_W),
        .COEFF_W(COEFF_W),
        .EXP_W(EXP_W),
        .ADD_W(ADD_W),
        .OUT_COEFF_W(OUT_COEFF_W),
        .MAX_SHIFT(2)
    ) dut (
        .pair_index(pair_index),
        .target_qubit(target_qubit),
        .amp_rdata0(amp_rdata0),
        .amp_rdata1(amp_rdata1),
        .addr0(addr0),
        .addr1(addr1),
        .amp_wdata0(amp_wdata0),
        .amp_wdata1(amp_wdata1),
        .valid(valid)
    );

    initial begin
        pair_index = 3'd2;
        target_qubit = 8'd1;
        amp_rdata0 = {8'sd1, 8'sd0, 8'sd0, 8'sd0, 4'd0, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        amp_rdata1 = {8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        #1;
        if (!valid) $fatal(1, "hadamard step valid mismatch");
        if (addr0 !== 3'd4 || addr1 !== 3'd6) $fatal(1, "hadamard step address mismatch");
        if (amp_wdata0 !== {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1}) $fatal(1, "hadamard step wdata0 mismatch");
        if (amp_wdata1 !== {12'sd0, 12'sd6, 12'sd0, 12'sd0, 4'd1, 12'sd0, 12'sd0, 12'sd0, 12'sd0, 4'd1}) $fatal(1, "hadamard step wdata1 mismatch");

        target_qubit = 8'd3;
        #1;
        if (valid) $fatal(1, "hadamard step accepted invalid target");

        target_qubit = 8'd1;
        amp_rdata1 = {8'sd1, 8'sd0, 8'sd0, 8'sd0, 4'd3, 8'sd0, 8'sd0, 8'sd0, 8'sd0, 4'd0};
        #1;
        if (valid) $fatal(1, "hadamard step accepted invalid datapath exponent gap");

        $display("hadamard_pair_step_tb passed");
        $finish;
    end

endmodule
