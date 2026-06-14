module q12_scale_sqrt_half #(
    parameter int W = 64,
    parameter int EW = 8,
    parameter int OUT_W = W + 4
)(
    input  logic signed [W-1:0]       a_in,
    input  logic signed [W-1:0]       b_in,
    input  logic signed [W-1:0]       c_in,
    input  logic signed [W-1:0]       d_in,
    input  logic        [EW-1:0]      e_in,

    output logic signed [OUT_W-1:0]   a_out,
    output logic signed [OUT_W-1:0]   b_out,
    output logic signed [OUT_W-1:0]   c_out,
    output logic signed [OUT_W-1:0]   d_out,
    output logic        [EW-1:0]      e_out
);

    always_comb begin
        a_out = 12 * b_in;
        b_out = 6 * a_in;
        c_out = 12 * d_in;
        d_out = 6 * c_in;
        e_out = e_in + 1'b1;
    end

endmodule
