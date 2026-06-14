module statevector_pair_mem #(
    parameter int ADDR_W = 8,
    parameter int COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W)
)(
    input  logic                 clk,
    input  logic                 we0,
    input  logic                 we1,
    input  logic [ADDR_W-1:0]    addr0,
    input  logic [ADDR_W-1:0]    addr1,
    input  logic [AMP_W-1:0]     wdata0,
    input  logic [AMP_W-1:0]     wdata1,
    output logic [AMP_W-1:0]     rdata0,
    output logic [AMP_W-1:0]     rdata1
);

    logic [AMP_W-1:0] mem [0:(1 << ADDR_W)-1];

    always_ff @(posedge clk) begin
        if (we0) begin
            mem[addr0] <= wdata0;
        end
        if (we1) begin
            mem[addr1] <= wdata1;
        end

        rdata0 <= mem[addr0];
        rdata1 <= mem[addr1];
    end

endmodule
