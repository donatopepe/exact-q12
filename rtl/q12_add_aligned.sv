module q12_add_aligned #(
    parameter int W = 32,
    parameter int EW = 8,
    parameter int OUT_W = 64,
    parameter int MAX_SHIFT = 4
)(
    input  logic signed [W-1:0]       a0,
    input  logic signed [W-1:0]       b0,
    input  logic signed [W-1:0]       c0,
    input  logic signed [W-1:0]       d0,
    input  logic        [EW-1:0]      e0,

    input  logic signed [W-1:0]       a1,
    input  logic signed [W-1:0]       b1,
    input  logic signed [W-1:0]       c1,
    input  logic signed [W-1:0]       d1,
    input  logic        [EW-1:0]      e1,

    input  logic                      subtract,

    output logic signed [OUT_W-1:0]   a_out,
    output logic signed [OUT_W-1:0]   b_out,
    output logic signed [OUT_W-1:0]   c_out,
    output logic signed [OUT_W-1:0]   d_out,
    output logic        [EW-1:0]      e_out,
    output logic                      valid
);

    logic [EW-1:0] diff0;
    logic [EW-1:0] diff1;
    logic signed [OUT_W-1:0] scale0;
    logic signed [OUT_W-1:0] scale1;

    function automatic logic signed [OUT_W-1:0] pow12(input logic [EW-1:0] exponent);
        logic signed [OUT_W-1:0] result;
        int i;
        begin
            result = {{(OUT_W-1){1'b0}}, 1'b1};
            for (i = 0; i < MAX_SHIFT; i = i + 1) begin
                if (i < exponent) begin
                    result = result * 12;
                end
            end
            pow12 = result;
        end
    endfunction

    always_comb begin
        e_out = (e0 >= e1) ? e0 : e1;
        diff0 = e_out - e0;
        diff1 = e_out - e1;
        valid = (diff0 <= MAX_SHIFT) && (diff1 <= MAX_SHIFT);

        scale0 = pow12(diff0);
        scale1 = pow12(diff1);

        if (subtract) begin
            a_out = (a0 * scale0) - (a1 * scale1);
            b_out = (b0 * scale0) - (b1 * scale1);
            c_out = (c0 * scale0) - (c1 * scale1);
            d_out = (d0 * scale0) - (d1 * scale1);
        end else begin
            a_out = (a0 * scale0) + (a1 * scale1);
            b_out = (b0 * scale0) + (b1 * scale1);
            c_out = (c0 * scale0) + (c1 * scale1);
            d_out = (d0 * scale0) + (d1 * scale1);
        end
    end

endmodule
