module hadamard_address_pair #(
    parameter int ADDR_W = 8,
    parameter int QUBIT_W = 8
)(
    input  logic [ADDR_W-1:0]       pair_index,
    input  logic [QUBIT_W-1:0]      target_qubit,

    output logic [ADDR_W-1:0]       addr0,
    output logic [ADDR_W-1:0]       addr1,
    output logic                    valid
);

    int unsigned target_bit;
    logic [ADDR_W-1:0] lower_mask;
    logic [ADDR_W-1:0] lower_bits;
    logic [ADDR_W-1:0] upper_bits;
    logic [ADDR_W-1:0] target_mask;

    always_comb begin
        valid = (target_qubit < ADDR_W);
        target_bit = valid ? (ADDR_W - 1 - target_qubit) : 0;

        lower_mask = (target_bit == 0) ? '0 : (({{(ADDR_W-1){1'b0}}, 1'b1} << target_bit) - 1'b1);
        lower_bits = pair_index & lower_mask;
        upper_bits = (pair_index & ~lower_mask) << 1;
        target_mask = {{(ADDR_W-1){1'b0}}, 1'b1} << target_bit;

        addr0 = upper_bits | lower_bits;
        addr1 = addr0 | target_mask;
    end

endmodule
