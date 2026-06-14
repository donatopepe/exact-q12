module statevector_pair_mem_tb;

    logic clk;
    logic we0;
    logic we1;
    logic [1:0] addr0;
    logic [1:0] addr1;
    logic [7:0] wdata0;
    logic [7:0] wdata1;
    logic [7:0] rdata0;
    logic [7:0] rdata1;

    statevector_pair_mem #(.ADDR_W(2), .COEFF_W(1), .EXP_W(0), .AMP_W(8)) dut (
        .clk(clk),
        .we0(we0),
        .we1(we1),
        .addr0(addr0),
        .addr1(addr1),
        .wdata0(wdata0),
        .wdata1(wdata1),
        .rdata0(rdata0),
        .rdata1(rdata1)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 1'b0;
        we0 = 1'b0;
        we1 = 1'b0;
        addr0 = 2'd0;
        addr1 = 2'd1;
        wdata0 = 8'h00;
        wdata1 = 8'h00;

        @(negedge clk);
        we0 = 1'b1;
        we1 = 1'b1;
        addr0 = 2'd0;
        addr1 = 2'd1;
        wdata0 = 8'ha5;
        wdata1 = 8'h5a;
        @(negedge clk);
        we0 = 1'b0;
        we1 = 1'b0;
        addr0 = 2'd0;
        addr1 = 2'd1;
        @(negedge clk);
        if (rdata0 !== 8'ha5 || rdata1 !== 8'h5a) $fatal(1, "pair readback mismatch");

        we0 = 1'b1;
        we1 = 1'b1;
        addr0 = 2'd2;
        addr1 = 2'd2;
        wdata0 = 8'h11;
        wdata1 = 8'h22;
        @(negedge clk);
        we0 = 1'b0;
        we1 = 1'b0;
        addr0 = 2'd2;
        addr1 = 2'd2;
        @(negedge clk);
        if (rdata0 !== 8'h22 || rdata1 !== 8'h22) $fatal(1, "write collision priority mismatch");

        $display("statevector_pair_mem_tb passed");
        $finish;
    end

endmodule
