vlib work
vcom *.vhd
vsim work.TB
add wave -r /*
run -all

vlib work
vmap work work

vcom transmitter.vhd
vcom receiver.vhd
vcom FSM.vhd
vcom tran_rec_top.vhd
vcom TB.vhd

vsim work.TB
add wave -r *
run -all
