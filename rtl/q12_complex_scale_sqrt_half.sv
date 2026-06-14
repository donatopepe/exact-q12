module q12_complex_scale_sqrt_half #(
    parameter int W = 64,
    parameter int EW = 8,
    parameter int OUT_W = W + 4
)(
    input  logic signed [W-1:0]       ar_in,
    input  logic signed [W-1:0]       br_in,
    input  logic signed [W-1:0]       cr_in,
    input  logic signed [W-1:0]       dr_in,
    input  logic        [EW-1:0]      er_in,
    input  logic signed [W-1:0]       ai_in,
    input  logic signed [W-1:0]       bi_in,
    input  logic signed [W-1:0]       ci_in,
    input  logic signed [W-1:0]       di_in,
    input  logic        [EW-1:0]      ei_in,

    output logic signed [OUT_W-1:0]   ar_out,
    output logic signed [OUT_W-1:0]   br_out,
    output logic signed [OUT_W-1:0]   cr_out,
    output logic signed [OUT_W-1:0]   dr_out,
    output logic        [EW-1:0]      er_out,
    output logic signed [OUT_W-1:0]   ai_out,
    output logic signed [OUT_W-1:0]   bi_out,
    output logic signed [OUT_W-1:0]   ci_out,
    output logic signed [OUT_W-1:0]   di_out,
    output logic        [EW-1:0]      ei_out
);

    q12_scale_sqrt_half #(.W(W), .EW(EW), .OUT_W(OUT_W)) real_scale (
        .a_in(ar_in), .b_in(br_in), .c_in(cr_in), .d_in(dr_in), .e_in(er_in),
        .a_out(ar_out), .b_out(br_out), .c_out(cr_out), .d_out(dr_out), .e_out(er_out)
    );

    q12_scale_sqrt_half #(.W(W), .EW(EW), .OUT_W(OUT_W)) imag_scale (
        .a_in(ai_in), .b_in(bi_in), .c_in(ci_in), .d_in(di_in), .e_in(ei_in),
        .a_out(ai_out), .b_out(bi_out), .c_out(ci_out), .d_out(di_out), .e_out(ei_out)
    );

endmodule
