module q12_add #(
    parameter int W = 32,
    parameter int EW = 8
)(
    input  logic signed [W-1:0] a0,
    input  logic signed [W-1:0] b0,
    input  logic signed [W-1:0] c0,
    input  logic signed [W-1:0] d0,
    input  logic        [EW-1:0] e0,

    input  logic signed [W-1:0] a1,
    input  logic signed [W-1:0] b1,
    input  logic signed [W-1:0] c1,
    input  logic signed [W-1:0] d1,
    input  logic        [EW-1:0] e1,

    input  logic                 subtract,

    output logic signed [W:0]    a_out,
    output logic signed [W:0]    b_out,
    output logic signed [W:0]    c_out,
    output logic signed [W:0]    d_out,
    output logic        [EW-1:0] e_out,
    output logic                 valid
);

    always_comb begin
        valid = (e0 == e1);
        e_out = e0;

        if (subtract) begin
            a_out = a0 - a1;
            b_out = b0 - b1;
            c_out = c0 - c1;
            d_out = d0 - d1;
        end else begin
            a_out = a0 + a1;
            b_out = b0 + b1;
            c_out = c0 + c1;
            d_out = d0 + d1;
        end
    end

endmodule
