module q12_mul_tb;

    logic signed [31:0] a;
    logic signed [31:0] b;
    logic signed [31:0] c;
    logic signed [31:0] d;
    logic signed [31:0] e;
    logic signed [31:0] f;
    logic signed [31:0] g;
    logic signed [31:0] h;
    logic signed [67:0] A;
    logic signed [67:0] B;
    logic signed [67:0] C;
    logic signed [67:0] D;

    q12_mul dut (
        .a(a), .b(b), .c(c), .d(d),
        .e(e), .f(f), .g(g), .h(h),
        .A(A), .B(B), .C(C), .D(D)
    );

    initial begin
        a = 32'sd1;
        b = 32'sd2;
        c = 32'sd3;
        d = 32'sd4;
        e = 32'sd5;
        f = 32'sd6;
        g = 32'sd7;
        h = 32'sd8;
        #1;
        if (A !== 68'sd284) $fatal(1, "A mismatch: %0d", A);
        if (B !== 68'sd172) $fatal(1, "B mismatch: %0d", B);
        if (C !== 68'sd102) $fatal(1, "C mismatch: %0d", C);
        if (D !== 68'sd60) $fatal(1, "D mismatch: %0d", D);

        a = -32'sd3;
        b = 32'sd0;
        c = 32'sd2;
        d = -32'sd1;
        e = 32'sd4;
        f = -32'sd5;
        g = 32'sd0;
        h = 32'sd6;
        #1;
        if (A !== -68'sd48) $fatal(1, "A signed mismatch: %0d", A);
        if (B !== 68'sd51) $fatal(1, "B signed mismatch: %0d", B);
        if (C !== 68'sd18) $fatal(1, "C signed mismatch: %0d", C);
        if (D !== -68'sd32) $fatal(1, "D signed mismatch: %0d", D);

        $display("q12_mul_tb passed");
        $finish;
    end

endmodule
