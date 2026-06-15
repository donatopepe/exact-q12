module hadamard_pair_traversal #(
    parameter int ADDR_W = 8,
    parameter int QUBIT_W = 8
)(
    input  logic                  clk,
    input  logic                  rst,
    input  logic                  start,
    input  logic [QUBIT_W-1:0]    num_qubits,

    output logic [ADDR_W-1:0]     pair_index,
    output logic                  pair_valid,
    output logic                  busy,
    output logic                  done
);

    typedef enum logic [1:0] {
        ST_IDLE,
        ST_RUN,
        ST_DONE
    } state_t;

    state_t state;
    logic [ADDR_W-1:0] last_pair;
    logic config_valid;

    always_comb begin
        config_valid = (num_qubits > 0) && (num_qubits <= ADDR_W);
        last_pair = config_valid ? (({{(ADDR_W-1){1'b0}}, 1'b1} << (num_qubits - 1'b1)) - 1'b1) : '0;
        pair_valid = (state == ST_RUN);
        busy = (state == ST_RUN);
        done = (state == ST_DONE);
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            state <= ST_IDLE;
            pair_index <= '0;
        end else begin
            case (state)
                ST_IDLE: begin
                    pair_index <= '0;
                    if (start) begin
                        state <= config_valid ? ST_RUN : ST_DONE;
                    end
                end

                ST_RUN: begin
                    if (pair_index == last_pair) begin
                        state <= ST_DONE;
                    end else begin
                        pair_index <= pair_index + 1'b1;
                    end
                end

                ST_DONE: begin
                    if (!start) begin
                        state <= ST_IDLE;
                    end
                end

                default: begin
                    state <= ST_IDLE;
                    pair_index <= '0;
                end
            endcase
        end
    end

endmodule
