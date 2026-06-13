package exactq12_pkg;

    localparam logic [7:0] OP_RESET   = 8'h00;
    localparam logic [7:0] OP_X       = 8'h01;
    localparam logic [7:0] OP_Z       = 8'h02;
    localparam logic [7:0] OP_H       = 8'h03;
    localparam logic [7:0] OP_S       = 8'h04;
    localparam logic [7:0] OP_T       = 8'h05;
    localparam logic [7:0] OP_P30     = 8'h06;
    localparam logic [7:0] OP_P60     = 8'h07;
    localparam logic [7:0] OP_CNOT    = 8'h08;
    localparam logic [7:0] OP_SWAP    = 8'h09;
    localparam logic [7:0] OP_DUMP    = 8'h0a;
    localparam logic [7:0] OP_PROB    = 8'h0b;
    localparam logic [7:0] OP_MEASURE = 8'h0c;

endpackage
