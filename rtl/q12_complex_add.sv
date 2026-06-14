module q12_complex_add #(
    parameter int W = 32,
    parameter int EW = 8
)(
    input  logic signed [W-1:0] ar0,
    input  logic signed [W-1:0] br0,
    input  logic signed [W-1:0] cr0,
    input  logic signed [W-1:0] dr0,
    input  logic        [EW-1:0] er0,
    input  logic signed [W-1:0] ai0,
    input  logic signed [W-1:0] bi0,
    input  logic signed [W-1:0] ci0,
    input  logic signed [W-1:0] di0,
    input  logic        [EW-1:0] ei0,

    input  logic signed [W-1:0] ar1,
    input  logic signed [W-1:0] br1,
    input  logic signed [W-1:0] cr1,
    input  logic signed [W-1:0] dr1,
    input  logic        [EW-1:0] er1,
    input  logic signed [W-1:0] ai1,
    input  logic signed [W-1:0] bi1,
    input  logic signed [W-1:0] ci1,
    input  logic signed [W-1:0] di1,
    input  logic        [EW-1:0] ei1,

    input  logic                 subtract,

    output logic signed [W:0]    ar_out,
    output logic signed [W:0]    br_out,
    output logic signed [W:0]    cr_out,
    output logic signed [W:0]    dr_out,
    output logic        [EW-1:0] er_out,
    output logic signed [W:0]    ai_out,
    output logic signed [W:0]    bi_out,
    output logic signed [W:0]    ci_out,
    output logic signed [W:0]    di_out,
    output logic        [EW-1:0] ei_out,
    output logic                 valid
);

    logic real_valid;
    logic imag_valid;

    q12_add #(.W(W), .EW(EW)) real_add (
        .a0(ar0), .b0(br0), .c0(cr0), .d0(dr0), .e0(er0),
        .a1(ar1), .b1(br1), .c1(cr1), .d1(dr1), .e1(er1),
        .subtract(subtract),
        .a_out(ar_out), .b_out(br_out), .c_out(cr_out), .d_out(dr_out), .e_out(er_out),
        .valid(real_valid)
    );

    q12_add #(.W(W), .EW(EW)) imag_add (
        .a0(ai0), .b0(bi0), .c0(ci0), .d0(di0), .e0(ei0),
        .a1(ai1), .b1(bi1), .c1(ci1), .d1(di1), .e1(ei1),
        .subtract(subtract),
        .a_out(ai_out), .b_out(bi_out), .c_out(ci_out), .d_out(di_out), .e_out(ei_out),
        .valid(imag_valid)
    );

    always_comb begin
        valid = real_valid && imag_valid;
    end

endmodule
