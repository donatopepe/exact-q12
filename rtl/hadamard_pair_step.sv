module hadamard_pair_step #(
    parameter int ADDR_W = 8,
    parameter int QUBIT_W = 8,
    parameter int COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter int ADD_W = 64,
    parameter int OUT_COEFF_W = 68,
    parameter int MAX_SHIFT = 4,
    parameter int AMP_W = (8 * COEFF_W) + (2 * EXP_W),
    parameter int OUT_AMP_W = (8 * OUT_COEFF_W) + (2 * EXP_W)
)(
    input  logic [ADDR_W-1:0]         pair_index,
    input  logic [QUBIT_W-1:0]        target_qubit,
    input  logic [AMP_W-1:0]          amp_rdata0,
    input  logic [AMP_W-1:0]          amp_rdata1,

    output logic [ADDR_W-1:0]         addr0,
    output logic [ADDR_W-1:0]         addr1,
    output logic [OUT_AMP_W-1:0]      amp_wdata0,
    output logic [OUT_AMP_W-1:0]      amp_wdata1,
    output logic                      valid
);

    logic address_valid;
    logic datapath_valid;

    hadamard_address_pair #(.ADDR_W(ADDR_W), .QUBIT_W(QUBIT_W)) address_pair (
        .pair_index(pair_index),
        .target_qubit(target_qubit),
        .addr0(addr0),
        .addr1(addr1),
        .valid(address_valid)
    );

    hadamard_pair_packed #(
        .COEFF_W(COEFF_W),
        .EXP_W(EXP_W),
        .ADD_W(ADD_W),
        .OUT_COEFF_W(OUT_COEFF_W),
        .MAX_SHIFT(MAX_SHIFT)
    ) datapath (
        .amp_in0(amp_rdata0),
        .amp_in1(amp_rdata1),
        .amp_out0(amp_wdata0),
        .amp_out1(amp_wdata1),
        .valid(datapath_valid)
    );

    always_comb begin
        valid = address_valid && datapath_valid;
    end

endmodule
