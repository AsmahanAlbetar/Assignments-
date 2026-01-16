vcom TB.vhd
vsim work.TB
add wave -position insertpoint  \
sim:/tb/Clk \
sim:/tb/reset \
sim:/tb/en \
sim:/tb/fill_Led \
sim:/tb/wash_Led \
sim:/tb/rinse_Led \
sim:/tb/spin_Led
run 29 sec