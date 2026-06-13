import exactq12_pkg::*;

module instruction_decoder (
    input  logic [23:0] instr,
    output logic [7:0]  opcode,
    output logic [7:0]  arg0,
    output logic [7:0]  arg1,
    output logic        valid,
    output logic        uses_arg0,
    output logic        uses_arg1
);

    always_comb begin
        opcode = instr[23:16];
        arg0 = instr[15:8];
        arg1 = instr[7:0];
        valid = 1'b1;
        uses_arg0 = 1'b0;
        uses_arg1 = 1'b0;

        unique case (opcode)
            OP_RESET,
            OP_X,
            OP_Z,
            OP_H,
            OP_S,
            OP_T,
            OP_P30,
            OP_P60,
            OP_MEASURE: begin
                uses_arg0 = 1'b1;
            end

            OP_CNOT,
            OP_SWAP: begin
                uses_arg0 = 1'b1;
                uses_arg1 = 1'b1;
            end

            OP_DUMP,
            OP_PROB: begin
                uses_arg0 = 1'b0;
                uses_arg1 = 1'b0;
            end

            default: begin
                valid = 1'b0;
            end
        endcase
    end

endmodule
