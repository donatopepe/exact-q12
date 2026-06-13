import exactq12_pkg::*;

module exactq12_sequencer #(
    parameter int PC_W = 8
)(
    input  logic              clk,
    input  logic              rst,
    input  logic              start,
    input  logic [23:0]       instr,

    output logic [PC_W-1:0]   pc,
    output logic              running,
    output logic              halted,
    output logic              invalid,
    output logic [7:0]        opcode,
    output logic [7:0]        arg0,
    output logic [7:0]        arg1
);

    typedef enum logic [1:0] {
        ST_IDLE,
        ST_FETCH,
        ST_DECODE,
        ST_HALT
    } state_t;

    state_t state;
    logic decoder_valid;
    logic uses_arg0;
    logic uses_arg1;

    instruction_decoder decoder (
        .instr(instr),
        .opcode(opcode),
        .arg0(arg0),
        .arg1(arg1),
        .valid(decoder_valid),
        .uses_arg0(uses_arg0),
        .uses_arg1(uses_arg1)
    );

    always_ff @(posedge clk) begin
        if (rst) begin
            state <= ST_IDLE;
            pc <= '0;
            running <= 1'b0;
            halted <= 1'b0;
            invalid <= 1'b0;
        end else begin
            unique case (state)
                ST_IDLE: begin
                    halted <= 1'b0;
                    invalid <= 1'b0;
                    if (start) begin
                        pc <= '0;
                        running <= 1'b1;
                        state <= ST_FETCH;
                    end
                end

                ST_FETCH: begin
                    state <= ST_DECODE;
                end

                ST_DECODE: begin
                    if (!decoder_valid) begin
                        invalid <= 1'b1;
                        running <= 1'b0;
                        halted <= 1'b1;
                        state <= ST_HALT;
                    end else if (opcode == OP_DUMP) begin
                        running <= 1'b0;
                        halted <= 1'b1;
                        state <= ST_HALT;
                    end else begin
                        pc <= pc + 1'b1;
                        state <= ST_FETCH;
                    end
                end

                ST_HALT: begin
                    if (!start) begin
                        state <= ST_IDLE;
                    end
                end
            endcase
        end
    end

endmodule
