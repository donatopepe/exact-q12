module q12_complex_mul #(
    parameter int W = 32
)(
    input  logic signed [W-1:0] ar,
    input  logic signed [W-1:0] br,
    input  logic signed [W-1:0] cr,
    input  logic signed [W-1:0] dr,
    input  logic signed [W-1:0] ai,
    input  logic signed [W-1:0] bi,
    input  logic signed [W-1:0] ci,
    input  logic signed [W-1:0] di,

    input  logic signed [W-1:0] er,
    input  logic signed [W-1:0] fr,
    input  logic signed [W-1:0] gr,
    input  logic signed [W-1:0] hr,
    input  logic signed [W-1:0] ei,
    input  logic signed [W-1:0] fi,
    input  logic signed [W-1:0] gi,
    input  logic signed [W-1:0] hi,

    output logic signed [(2*W)+4:0] out_ar,
    output logic signed [(2*W)+4:0] out_br,
    output logic signed [(2*W)+4:0] out_cr,
    output logic signed [(2*W)+4:0] out_dr,
    output logic signed [(2*W)+4:0] out_ai,
    output logic signed [(2*W)+4:0] out_bi,
    output logic signed [(2*W)+4:0] out_ci,
    output logic signed [(2*W)+4:0] out_di
);

    logic signed [(2*W)+3:0] rr_a;
    logic signed [(2*W)+3:0] rr_b;
    logic signed [(2*W)+3:0] rr_c;
    logic signed [(2*W)+3:0] rr_d;
    logic signed [(2*W)+3:0] ii_a;
    logic signed [(2*W)+3:0] ii_b;
    logic signed [(2*W)+3:0] ii_c;
    logic signed [(2*W)+3:0] ii_d;
    logic signed [(2*W)+3:0] ri_a;
    logic signed [(2*W)+3:0] ri_b;
    logic signed [(2*W)+3:0] ri_c;
    logic signed [(2*W)+3:0] ri_d;
    logic signed [(2*W)+3:0] ir_a;
    logic signed [(2*W)+3:0] ir_b;
    logic signed [(2*W)+3:0] ir_c;
    logic signed [(2*W)+3:0] ir_d;

    q12_mul #(.W(W)) real_real (
        .a(ar), .b(br), .c(cr), .d(dr),
        .e(er), .f(fr), .g(gr), .h(hr),
        .A(rr_a), .B(rr_b), .C(rr_c), .D(rr_d)
    );

    q12_mul #(.W(W)) imag_imag (
        .a(ai), .b(bi), .c(ci), .d(di),
        .e(ei), .f(fi), .g(gi), .h(hi),
        .A(ii_a), .B(ii_b), .C(ii_c), .D(ii_d)
    );

    q12_mul #(.W(W)) real_imag (
        .a(ar), .b(br), .c(cr), .d(dr),
        .e(ei), .f(fi), .g(gi), .h(hi),
        .A(ri_a), .B(ri_b), .C(ri_c), .D(ri_d)
    );

    q12_mul #(.W(W)) imag_real (
        .a(ai), .b(bi), .c(ci), .d(di),
        .e(er), .f(fr), .g(gr), .h(hr),
        .A(ir_a), .B(ir_b), .C(ir_c), .D(ir_d)
    );

    always_comb begin
        out_ar = rr_a - ii_a;
        out_br = rr_b - ii_b;
        out_cr = rr_c - ii_c;
        out_dr = rr_d - ii_d;

        out_ai = ri_a + ir_a;
        out_bi = ri_b + ir_b;
        out_ci = ri_c + ir_c;
        out_di = ri_d + ir_d;
    end

endmodule
