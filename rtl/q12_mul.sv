module q12_mul #(
    parameter int W = 32
)(
    input  logic signed [W-1:0] a,
    input  logic signed [W-1:0] b,
    input  logic signed [W-1:0] c,
    input  logic signed [W-1:0] d,

    input  logic signed [W-1:0] e,
    input  logic signed [W-1:0] f,
    input  logic signed [W-1:0] g,
    input  logic signed [W-1:0] h,

    output logic signed [(2*W)+3:0] A,
    output logic signed [(2*W)+3:0] B,
    output logic signed [(2*W)+3:0] C,
    output logic signed [(2*W)+3:0] D
);

    always_comb begin
        A = (a * e) + 2 * (b * f) + 3 * (c * g) + 6 * (d * h);
        B = (a * f) + (b * e) + 3 * (c * h) + 3 * (d * g);
        C = (a * g) + (c * e) + 2 * (b * h) + 2 * (d * f);
        D = (a * h) + (d * e) + (b * g) + (c * f);
    end

endmodule
