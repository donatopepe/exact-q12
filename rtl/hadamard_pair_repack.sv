module hadamard_pair_repack #(
    parameter int IN_COEFF_W = 68,
    parameter int OUT_COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter int IN_AMP_W = (8 * IN_COEFF_W) + (2 * EXP_W),
    parameter int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W)
)(
    input  logic [IN_AMP_W-1:0]       amp_in0,
    input  logic [IN_AMP_W-1:0]       amp_in1,

    output logic [OUT_AMP_W-1:0]      amp_out0,
    output logic [OUT_AMP_W-1:0]      amp_out1,
    output logic                      valid
);

    logic signed [IN_COEFF_W-1:0] c0 [0:7];
    logic signed [IN_COEFF_W-1:0] c1 [0:7];
    logic [EXP_W-1:0] er0;
    logic [EXP_W-1:0] ei0;
    logic [EXP_W-1:0] er1;
    logic [EXP_W-1:0] ei1;
    logic fit0;
    logic fit1;

    function automatic logic coeff_fits(input logic signed [IN_COEFF_W-1:0] value);
        int i;
        logic sign;
        begin
            coeff_fits = 1'b1;
            sign = value[OUT_COEFF_W-1];
            for (i = OUT_COEFF_W; i < IN_COEFF_W; i = i + 1) begin
                if (value[i] != sign) begin
                    coeff_fits = 1'b0;
                end
            end
        end
    endfunction

    always_comb begin
        c0[0] = amp_in0[IN_AMP_W-1 -: IN_COEFF_W];
        c0[1] = amp_in0[IN_AMP_W-IN_COEFF_W-1 -: IN_COEFF_W];
        c0[2] = amp_in0[IN_AMP_W-(2*IN_COEFF_W)-1 -: IN_COEFF_W];
        c0[3] = amp_in0[IN_AMP_W-(3*IN_COEFF_W)-1 -: IN_COEFF_W];
        er0 = amp_in0[IN_AMP_W-(4*IN_COEFF_W)-1 -: EXP_W];
        c0[4] = amp_in0[IN_AMP_W-(4*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c0[5] = amp_in0[IN_AMP_W-(5*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c0[6] = amp_in0[IN_AMP_W-(6*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c0[7] = amp_in0[IN_AMP_W-(7*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        ei0 = amp_in0[EXP_W-1:0];

        c1[0] = amp_in1[IN_AMP_W-1 -: IN_COEFF_W];
        c1[1] = amp_in1[IN_AMP_W-IN_COEFF_W-1 -: IN_COEFF_W];
        c1[2] = amp_in1[IN_AMP_W-(2*IN_COEFF_W)-1 -: IN_COEFF_W];
        c1[3] = amp_in1[IN_AMP_W-(3*IN_COEFF_W)-1 -: IN_COEFF_W];
        er1 = amp_in1[IN_AMP_W-(4*IN_COEFF_W)-1 -: EXP_W];
        c1[4] = amp_in1[IN_AMP_W-(4*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c1[5] = amp_in1[IN_AMP_W-(5*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c1[6] = amp_in1[IN_AMP_W-(6*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        c1[7] = amp_in1[IN_AMP_W-(7*IN_COEFF_W)-EXP_W-1 -: IN_COEFF_W];
        ei1 = amp_in1[EXP_W-1:0];

        fit0 = coeff_fits(c0[0]) && coeff_fits(c0[1]) && coeff_fits(c0[2]) && coeff_fits(c0[3]) && coeff_fits(c0[4]) && coeff_fits(c0[5]) && coeff_fits(c0[6]) && coeff_fits(c0[7]);
        fit1 = coeff_fits(c1[0]) && coeff_fits(c1[1]) && coeff_fits(c1[2]) && coeff_fits(c1[3]) && coeff_fits(c1[4]) && coeff_fits(c1[5]) && coeff_fits(c1[6]) && coeff_fits(c1[7]);
        valid = fit0 && fit1;

        amp_out0 = {c0[0][OUT_COEFF_W-1:0], c0[1][OUT_COEFF_W-1:0], c0[2][OUT_COEFF_W-1:0], c0[3][OUT_COEFF_W-1:0], er0, c0[4][OUT_COEFF_W-1:0], c0[5][OUT_COEFF_W-1:0], c0[6][OUT_COEFF_W-1:0], c0[7][OUT_COEFF_W-1:0], ei0};
        amp_out1 = {c1[0][OUT_COEFF_W-1:0], c1[1][OUT_COEFF_W-1:0], c1[2][OUT_COEFF_W-1:0], c1[3][OUT_COEFF_W-1:0], er1, c1[4][OUT_COEFF_W-1:0], c1[5][OUT_COEFF_W-1:0], c1[6][OUT_COEFF_W-1:0], c1[7][OUT_COEFF_W-1:0], ei1};
    end

endmodule
