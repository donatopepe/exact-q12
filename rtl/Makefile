IVERILOG ?= iverilog
VVP ?= vvp
BUILD_DIR ?= build

.PHONY: sim q12_mul_tb q12_add_tb q12_add_aligned_tb q12_complex_add_tb q12_complex_add_aligned_tb instruction_decoder_tb exactq12_sequencer_tb clean

sim: q12_mul_tb q12_add_tb q12_add_aligned_tb q12_complex_add_tb q12_complex_add_aligned_tb instruction_decoder_tb exactq12_sequencer_tb

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

q12_mul_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/q12_mul_tb.vvp q12_mul.sv tb/q12_mul_tb.sv
	$(VVP) $(BUILD_DIR)/q12_mul_tb.vvp

q12_add_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/q12_add_tb.vvp q12_add.sv tb/q12_add_tb.sv
	$(VVP) $(BUILD_DIR)/q12_add_tb.vvp

q12_complex_add_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/q12_complex_add_tb.vvp q12_add.sv q12_complex_add.sv tb/q12_complex_add_tb.sv
	$(VVP) $(BUILD_DIR)/q12_complex_add_tb.vvp

q12_add_aligned_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/q12_add_aligned_tb.vvp q12_add_aligned.sv tb/q12_add_aligned_tb.sv
	$(VVP) $(BUILD_DIR)/q12_add_aligned_tb.vvp

q12_complex_add_aligned_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/q12_complex_add_aligned_tb.vvp q12_add_aligned.sv q12_complex_add_aligned.sv tb/q12_complex_add_aligned_tb.sv
	$(VVP) $(BUILD_DIR)/q12_complex_add_aligned_tb.vvp

instruction_decoder_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/instruction_decoder_tb.vvp exactq12_pkg.sv instruction_decoder.sv tb/instruction_decoder_tb.sv
	$(VVP) $(BUILD_DIR)/instruction_decoder_tb.vvp

exactq12_sequencer_tb: $(BUILD_DIR)
	$(IVERILOG) -g2012 -o $(BUILD_DIR)/exactq12_sequencer_tb.vvp exactq12_pkg.sv instruction_decoder.sv exactq12_sequencer.sv tb/exactq12_sequencer_tb.sv
	$(VVP) $(BUILD_DIR)/exactq12_sequencer_tb.vvp

clean:
	rm -rf $(BUILD_DIR)
