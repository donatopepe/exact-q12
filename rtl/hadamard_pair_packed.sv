module hadamard_pair_packed #(
    parameter int COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter int ADD_W = 64,
    parameter int OUT_COEFF_W = 68,
    parameter int MAX_SHIFT = 4,
    parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W),
    parameter int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W)
)(
    input  logic [AMP_W-1:0]          amp_in0,
    input  logic [AMP_W-1:0]          amp_in1,

    output logic [OUT_AMP_W-1:0]      amp_out0,
    output logic [OUT_AMP_W-1:0]      amp_out1,
    output logic                      valid
);

    logic signed [COEFF_W-1:0] ar0;
    logic signed [COEFF_W-1:0] br0;
    logic signed [COEFF_W-1:0] cr0;
    logic signed [COEFF_W-1:0] dr0;
    logic [EXP_W-1:0] er0;
    logic signed [COEFF_W-1:0] ai0;
    logic signed [COEFF_W-1:0] bi0;
    logic signed [COEFF_W-1:0] ci0;
    logic signed [COEFF_W-1:0] di0;
    logic [EXP_W-1:0] ei0;

    logic signed [COEFF_W-1:0] ar1;
    logic signed [COEFF_W-1:0] br1;
    logic signed [COEFF_W-1:0] cr1;
    logic signed [COEFF_W-1:0] dr1;
    logic [EXP_W-1:0] er1;
    logic signed [COEFF_W-1:0] ai1;
    logic signed [COEFF_W-1:0] bi1;
    logic signed [COEFF_W-1:0] ci1;
    logic signed [COEFF_W-1:0] di1;
    logic [EXP_W-1:0] ei1;

    logic signed [OUT_COEFF_W-1:0] ar_out0;
    logic signed [OUT_COEFF_W-1:0] br_out0;
    logic signed [OUT_COEFF_W-1:0] cr_out0;
    logic signed [OUT_COEFF_W-1:0] dr_out0;
    logic [EXP_W-1:0] er_out0;
    logic signed [OUT_COEFF_W-1:0] ai_out0;
    logic signed [OUT_COEFF_W-1:0] bi_out0;
    logic signed [OUT_COEFF_W-1:0] ci_out0;
    logic signed [OUT_COEFF_W-1:0] di_out0;
    logic [EXP_W-1:0] ei_out0;

    logic signed [OUT_COEFF_W-1:0] ar_out1;
    logic signed [OUT_COEFF_W-1:0] br_out1;
    logic signed [OUT_COEFF_W-1:0] cr_out1;
    logic signed [OUT_COEFF_W-1:0] dr_out1;
    logic [EXP_W-1:0] er_out1;
    logic signed [OUT_COEFF_W-1:0] ai_out1;
    logic signed [OUT_COEFF_W-1:0] bi_out1;
    logic signed [OUT_COEFF_W-1:0] ci_out1;
    logic signed [OUT_COEFF_W-1:0] di_out1;
    logic [EXP_W-1:0] ei_out1;

    always_comb begin
        ar0 = amp_in0[AMP_W-1 -: COEFF_W];
        br0 = amp_in0[AMP_W-COEFF_W-1 -: COEFF_W];
        cr0 = amp_in0[AMP_W-(2*COEFF_W)-1 -: COEFF_W];
        dr0 = amp_in0[AMP_W-(3*COEFF_W)-1 -: COEFF_W];
        er0 = amp_in0[AMP_W-(4*COEFF_W)-1 -: EXP_W];
        ai0 = amp_in0[AMP_W-(4*COEFF_W)-EXP_W-1 -: COEFF_W];
        bi0 = amp_in0[AMP_W-(5*COEFF_W)-EXP_W-1 -: COEFF_W];
        ci0 = amp_in0[AMP_W-(6*COEFF_W)-EXP_W-1 -: COEFF_W];
        di0 = amp_in0[AMP_W-(7*COEFF_W)-EXP_W-1 -: COEFF_W];
        ei0 = amp_in0[EXP_W-1:0];

        ar1 = amp_in1[AMP_W-1 -: COEFF_W];
        br1 = amp_in1[AMP_W-COEFF_W-1 -: COEFF_W];
        cr1 = amp_in1[AMP_W-(2*COEFF_W)-1 -: COEFF_W];
        dr1 = amp_in1[AMP_W-(3*COEFF_W)-1 -: COEFF_W];
        er1 = amp_in1[AMP_W-(4*COEFF_W)-1 -: EXP_W];
        ai1 = amp_in1[AMP_W-(4*COEFF_W)-EXP_W-1 -: COEFF_W];
        bi1 = amp_in1[AMP_W-(5*COEFF_W)-EXP_W-1 -: COEFF_W];
        ci1 = amp_in1[AMP_W-(6*COEFF_W)-EXP_W-1 -: COEFF_W];
        di1 = amp_in1[AMP_W-(7*COEFF_W)-EXP_W-1 -: COEFF_W];
        ei1 = amp_in1[EXP_W-1:0];

        amp_out0 = {ar_out0, br_out0, cr_out0, dr_out0, er_out0, ai_out0, bi_out0, ci_out0, di_out0, ei_out0};
        amp_out1 = {ar_out1, br_out1, cr_out1, dr_out1, er_out1, ai_out1, bi_out1, ci_out1, di_out1, ei_out1};
    end

    hadamard_pair #(
        .W(COEFF_W),
        .EW(EXP_W),
        .ADD_W(ADD_W),
        .OUT_W(OUT_COEFF_W),
        .MAX_SHIFT(MAX_SHIFT)
    ) pair (
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

endmodule
