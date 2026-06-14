module hadamard_address_pair_tb;

    logic [2:0] pair_index;
    logic [7:0] target_qubit;
    logic [2:0] addr0;
    logic [2:0] addr1;
    logic valid;

    hadamard_address_pair #(.ADDR_W(3), .QUBIT_W(8)) dut (
        .pair_index(pair_index),
        .target_qubit(target_qubit),
        .addr0(addr0),
        .addr1(addr1),
        .valid(valid)
    );

    initial begin
        pair_index = 3'd0; target_qubit = 8'd0;
        #1;
        if (!valid || addr0 !== 3'd0 || addr1 !== 3'd4) $fatal(1, "q0 pair 0 mismatch");

        pair_index = 3'd1; target_qubit = 8'd0;
        #1;
        if (!valid || addr0 !== 3'd1 || addr1 !== 3'd5) $fatal(1, "q0 pair 1 mismatch");

        pair_index = 3'd2; target_qubit = 8'd1;
        #1;
        if (!valid || addr0 !== 3'd4 || addr1 !== 3'd6) $fatal(1, "q1 pair 2 mismatch");

        pair_index = 3'd3; target_qubit = 8'd2;
        #1;
        if (!valid || addr0 !== 3'd6 || addr1 !== 3'd7) $fatal(1, "q2 pair 3 mismatch");

        pair_index = 3'd0; target_qubit = 8'd3;
        #1;
        if (valid) $fatal(1, "out-of-range target accepted");

        $display("hadamard_address_pair_tb passed");
        $finish;
    end

endmodule
