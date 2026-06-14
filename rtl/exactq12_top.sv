module exactq12_top #(
    parameter int PC_W = 8,
    parameter int STATE_ADDR_W = 2,
    parameter int COEFF_W = 32,
    parameter int EXP_W = 8,
    parameter string PROGRAM_INIT_FILE = "bell.memh"
)(
    input  logic                    clk,
    input  logic                    rst,
    input  logic                    start,

    input  logic [STATE_ADDR_W-1:0] state_addr,
    output logic [(8*COEFF_W)+(2*EXP_W)-1:0] state_rdata,

    output logic                    running,
    output logic                    halted,
    output logic                    invalid,
    output logic [PC_W-1:0]         pc,
    output logic [7:0]              opcode,
    output logic [7:0]              arg0,
    output logic [7:0]              arg1
);

    localparam int AMP_W = (8 * COEFF_W) + (2 * EXP_W);

    logic [23:0] instr;

    program_rom #(
        .ADDR_W(PC_W),
        .INIT_FILE(PROGRAM_INIT_FILE)
    ) program (
        .addr(pc),
        .instr(instr)
    );

    exactq12_sequencer #(
        .PC_W(PC_W)
    ) sequencer (
        .clk(clk),
        .rst(rst),
        .start(start),
        .instr(instr),
        .pc(pc),
        .running(running),
        .halted(halted),
        .invalid(invalid),
        .opcode(opcode),
        .arg0(arg0),
        .arg1(arg1)
    );

    statevector_mem #(
        .ADDR_W(STATE_ADDR_W),
        .COEFF_W(COEFF_W),
        .EXP_W(EXP_W),
        .AMP_W(AMP_W)
    ) state_mem (
        .clk(clk),
        .we(1'b0),
        .addr(state_addr),
        .wdata('0),
        .rdata(state_rdata)
    );

endmodule
