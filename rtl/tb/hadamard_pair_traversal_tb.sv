module hadamard_pair_traversal_tb;

    logic clk;
    logic rst;
    logic start;
    logic [7:0] num_qubits;
    logic [2:0] pair_index;
    logic pair_valid;
    logic busy;
    logic done;

    hadamard_pair_traversal #(.ADDR_W(3), .QUBIT_W(8)) dut (
        .clk(clk),
        .rst(rst),
        .start(start),
        .num_qubits(num_qubits),
        .pair_index(pair_index),
        .pair_valid(pair_valid),
        .busy(busy),
        .done(done)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 1'b0;
        rst = 1'b1;
        start = 1'b0;
        num_qubits = 8'd3;

        @(negedge clk);
        rst = 1'b0;
        start = 1'b1;

        @(negedge clk);
        if (!pair_valid || !busy || done || pair_index !== 3'd0) $fatal(1, "pair 0 mismatch");
        @(negedge clk);
        if (!pair_valid || pair_index !== 3'd1) $fatal(1, "pair 1 mismatch");
        @(negedge clk);
        if (!pair_valid || pair_index !== 3'd2) $fatal(1, "pair 2 mismatch");
        @(negedge clk);
        if (!pair_valid || pair_index !== 3'd3) $fatal(1, "pair 3 mismatch");
        @(negedge clk);
        if (pair_valid || busy || !done || pair_index !== 3'd3) $fatal(1, "done mismatch");

        start = 1'b0;
        @(negedge clk);
        if (pair_valid || busy || done || pair_index !== 3'd0) $fatal(1, "idle after done mismatch");

        num_qubits = 8'd0;
        start = 1'b1;
        @(negedge clk);
        if (pair_valid || busy || !done) $fatal(1, "invalid config should finish without pairs");

        $display("hadamard_pair_traversal_tb passed");
        $finish;
    end

endmodule
