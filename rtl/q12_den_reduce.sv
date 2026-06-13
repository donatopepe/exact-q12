module q12_den_reduce #(
    parameter int W = 32,
    parameter int EW = 8
)(
    input  logic signed [W-1:0] a_in,
    input  logic signed [W-1:0] b_in,
    input  logic signed [W-1:0] c_in,
    input  logic signed [W-1:0] d_in,
    input  logic        [EW-1:0] e_in,

    output logic signed [W-1:0] a_out,
    output logic signed [W-1:0] b_out,
    output logic signed [W-1:0] c_out,
    output logic signed [W-1:0] d_out,
    output logic        [EW-1:0] e_out,
    output logic                 reduced
);

    logic all_zero;
    logic all_divisible_by_12;

    always_comb begin
        all_zero = (a_in == '0) && (b_in == '0) && (c_in == '0) && (d_in == '0);
        all_divisible_by_12 = ((a_in % 12) == 0) &&
                              ((b_in % 12) == 0) &&
                              ((c_in % 12) == 0) &&
                              ((d_in % 12) == 0);

        if (all_zero) begin
            a_out = '0;
            b_out = '0;
            c_out = '0;
            d_out = '0;
            e_out = '0;
            reduced = (e_in != '0);
        end else if ((e_in != '0) && all_divisible_by_12) begin
            a_out = a_in / 12;
            b_out = b_in / 12;
            c_out = c_in / 12;
            d_out = d_in / 12;
            e_out = e_in - 1'b1;
            reduced = 1'b1;
        end else begin
            a_out = a_in;
            b_out = b_in;
            c_out = c_in;
            d_out = d_in;
            e_out = e_in;
            reduced = 1'b0;
        end
    end

endmodule
