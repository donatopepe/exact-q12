module statevector_mem #(
    parameter int ADDR_W = 8,
    parameter int COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W)
)(
    input  logic                 clk,
    input  logic                 we,
    input  logic [ADDR_W-1:0]    addr,
    input  logic [AMP_W-1:0]     wdata,
    output logic [AMP_W-1:0]     rdata
);

    logic [AMP_W-1:0] mem [0:(1 << ADDR_W)-1];

    always_ff @(posedge clk) begin
        if (we) begin
            mem[addr] <= wdata;
        end
        rdata <= mem[addr];
    end

endmodule
