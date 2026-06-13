module program_rom #(
    parameter int ADDR_W = 8,
    parameter string INIT_FILE = ""
)(
    input  logic [ADDR_W-1:0] addr,
    output logic [23:0]       instr
);

    logic [23:0] rom [0:(1 << ADDR_W)-1];

    initial begin
        if (INIT_FILE != "") begin
            $readmemh(INIT_FILE, rom);
        end
    end

    assign instr = rom[addr];

endmodule
