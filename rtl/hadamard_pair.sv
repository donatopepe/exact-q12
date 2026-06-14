module hadamard_pair #(
    parameter int W = 32,
    parameter int EW = 8,
    parameter int ADD_W = 64,
    parameter int OUT_W = 68,
    parameter int MAX_SHIFT = 4
)(
    input  logic signed [W-1:0]       ar0,
    input  logic signed [W-1:0]       br0,
    input  logic signed [W-1:0]       cr0,
    input  logic signed [W-1:0]       dr0,
    input  logic        [EW-1:0]      er0,
    input  logic signed [W-1:0]       ai0,
    input  logic signed [W-1:0]       bi0,
    input  logic signed [W-1:0]       ci0,
    input  logic signed [W-1:0]       di0,
    input  logic        [EW-1:0]      ei0,

    input  logic signed [W-1:0]       ar1,
    input  logic signed [W-1:0]       br1,
    input  logic signed [W-1:0]       cr1,
    input  logic signed [W-1:0]       dr1,
    input  logic        [EW-1:0]      er1,
    input  logic signed [W-1:0]       ai1,
    input  logic signed [W-1:0]       bi1,
    input  logic signed [W-1:0]       ci1,
    input  logic signed [W-1:0]       di1,
    input  logic        [EW-1:0]      ei1,

    output logic signed [OUT_W-1:0]   ar_out0,
    output logic signed [OUT_W-1:0]   br_out0,
    output logic signed [OUT_W-1:0]   cr_out0,
    output logic signed [OUT_W-1:0]   dr_out0,
    output logic        [EW-1:0]      er_out0,
    output logic signed [OUT_W-1:0]   ai_out0,
    output logic signed [OUT_W-1:0]   bi_out0,
    output logic signed [OUT_W-1:0]   ci_out0,
    output logic signed [OUT_W-1:0]   di_out0,
    output logic        [EW-1:0]      ei_out0,

    output logic signed [OUT_W-1:0]   ar_out1,
    output logic signed [OUT_W-1:0]   br_out1,
    output logic signed [OUT_W-1:0]   cr_out1,
    output logic signed [OUT_W-1:0]   dr_out1,
    output logic        [EW-1:0]      er_out1,
    output logic signed [OUT_W-1:0]   ai_out1,
    output logic signed [OUT_W-1:0]   bi_out1,
    output logic signed [OUT_W-1:0]   ci_out1,
    output logic signed [OUT_W-1:0]   di_out1,
    output logic        [EW-1:0]      ei_out1,
    output logic                      valid
);

    logic signed [ADD_W-1:0] ar_sum;
    logic signed [ADD_W-1:0] br_sum;
    logic signed [ADD_W-1:0] cr_sum;
    logic signed [ADD_W-1:0] dr_sum;
    logic [EW-1:0] er_sum;
    logic signed [ADD_W-1:0] ai_sum;
    logic signed [ADD_W-1:0] bi_sum;
    logic signed [ADD_W-1:0] ci_sum;
    logic signed [ADD_W-1:0] di_sum;
    logic [EW-1:0] ei_sum;
    logic sum_valid;

    logic signed [ADD_W-1:0] ar_diff;
    logic signed [ADD_W-1:0] br_diff;
    logic signed [ADD_W-1:0] cr_diff;
    logic signed [ADD_W-1:0] dr_diff;
    logic [EW-1:0] er_diff;
    logic signed [ADD_W-1:0] ai_diff;
    logic signed [ADD_W-1:0] bi_diff;
    logic signed [ADD_W-1:0] ci_diff;
    logic signed [ADD_W-1:0] di_diff;
    logic [EW-1:0] ei_diff;
    logic diff_valid;

    q12_complex_add_aligned #(.W(W), .EW(EW), .OUT_W(ADD_W), .MAX_SHIFT(MAX_SHIFT)) add_pair (
        .ar0(ar0), .br0(br0), .cr0(cr0), .dr0(dr0), .er0(er0),
        .ai0(ai0), .bi0(bi0), .ci0(ci0), .di0(di0), .ei0(ei0),
        .ar1(ar1), .br1(br1), .cr1(cr1), .dr1(dr1), .er1(er1),
        .ai1(ai1), .bi1(bi1), .ci1(ci1), .di1(di1), .ei1(ei1),
        .subtract(1'b0),
        .ar_out(ar_sum), .br_out(br_sum), .cr_out(cr_sum), .dr_out(dr_sum), .er_out(er_sum),
        .ai_out(ai_sum), .bi_out(bi_sum), .ci_out(ci_sum), .di_out(di_sum), .ei_out(ei_sum),
        .valid(sum_valid)
    );

    q12_complex_add_aligned #(.W(W), .EW(EW), .OUT_W(ADD_W), .MAX_SHIFT(MAX_SHIFT)) sub_pair (
        .ar0(ar0), .br0(br0), .cr0(cr0), .dr0(dr0), .er0(er0),
        .ai0(ai0), .bi0(bi0), .ci0(ci0), .di0(di0), .ei0(ei0),
        .ar1(ar1), .br1(br1), .cr1(cr1), .dr1(dr1), .er1(er1),
        .ai1(ai1), .bi1(bi1), .ci1(ci1), .di1(di1), .ei1(ei1),
        .subtract(1'b1),
        .ar_out(ar_diff), .br_out(br_diff), .cr_out(cr_diff), .dr_out(dr_diff), .er_out(er_diff),
        .ai_out(ai_diff), .bi_out(bi_diff), .ci_out(ci_diff), .di_out(di_diff), .ei_out(ei_diff),
        .valid(diff_valid)
    );

    q12_complex_scale_sqrt_half #(.W(ADD_W), .EW(EW), .OUT_W(OUT_W)) scale_sum (
        .ar_in(ar_sum), .br_in(br_sum), .cr_in(cr_sum), .dr_in(dr_sum), .er_in(er_sum),
        .ai_in(ai_sum), .bi_in(bi_sum), .ci_in(ci_sum), .di_in(di_sum), .ei_in(ei_sum),
        .ar_out(ar_out0), .br_out(br_out0), .cr_out(cr_out0), .dr_out(dr_out0), .er_out(er_out0),
        .ai_out(ai_out0), .bi_out(bi_out0), .ci_out(ci_out0), .di_out(di_out0), .ei_out(ei_out0)
    );

    q12_complex_scale_sqrt_half #(.W(ADD_W), .EW(EW), .OUT_W(OUT_W)) scale_diff (
        .ar_in(ar_diff), .br_in(br_diff), .cr_in(cr_diff), .dr_in(dr_diff), .er_in(er_diff),
        .ai_in(ai_diff), .bi_in(bi_diff), .ci_in(ci_diff), .di_in(di_diff), .ei_in(ei_diff),
        .ar_out(ar_out1), .br_out(br_out1), .cr_out(cr_out1), .dr_out(dr_out1), .er_out(er_out1),
        .ai_out(ai_out1), .bi_out(bi_out1), .ci_out(ci_out1), .di_out(di_out1), .ei_out(ei_out1)
    );

    always_comb begin
        valid = sum_valid && diff_valid;
    end

endmodule
