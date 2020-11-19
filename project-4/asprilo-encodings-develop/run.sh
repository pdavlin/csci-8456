#!/bin/bash

SYSTEM="clingo"
# SYSTEM="clingcon"

# ENCODINGS="action-MPP-3.lp goal-D-r.lp output-MPPD-3.lp -c horizon=$2"
# ENCODINGS="xapf/action-M.ilp   xapf/goal-m.ilp"
# ENCODINGS="xapf/action-M-XY.ilp   xapf/goal-m-XY.ilp"
# ENCODINGS="m/action-M.iclp   m/goal-m.iclp"
ENCODINGS="."
# VISUALIZER="--outf=0 -V0 --out-atomf=%s. | head -n1 | visualizer"
VISUALIZER="head -n1 | visualizer"

# Exercise 1-1 Command
# clingo --out-atomf='%s.' -V0 \
# -c horizon=15 \
# ./m/{action-M-mod.lp,goal-M-mod.lp,output-M.lp} \
# instances/x11_y6_n66_r1_s8_ps1_pr8_u8_o8_N001.lp | viz

# Exercise 1-2 Command
# clingo --out-atomf='%s.' -V0 \
# -c horizon=10 \
# $ENCODINGS/m/{action-M-mod.lp,goal-M-mod.lp,output-M.lp} \
# instances/x11_y6_n66_r1_s8_ps1_pr8_u8_o8_N001.lp | viz

# Exercise 2-1 Command
clingo --out-atomf='%s.' -V0 \
-c horizon=20 \
$ENCODINGS/m/{action-M-mod.lp,goal-M.lp,output-M.lp} \
instances/x11_y6_n66_r8_s8_ps1_pr8_u8_o8_N001.lp | viz

# Exercise 2-2
# clingo --out-atomf='%s.' -V0 \
# -c horizon=25 \
# $ENCODINGS/control/{sides.lp,highways.lp} \
# $ENCODINGS/abc/{action-MPP.lp,goal-D-a.lp,output-MPPD.lp} \
# instances/x9_y6_n54_r4_s8_ps2_pr8_u8_o8_N001.lp | viz

# Exercise 3-1
# clingo --out-atomf='%s.' -V0 \
# -c horizon=25 \
# $ENCODINGS/control/{sides.lp,highways.lp} \
# $ENCODINGS/abc/{action-MPP.lp,goal-D-a.lp,output-MPPD.lp} \
# instances/x9_y6_n54_r4_s8_ps2_pr8_u8_o8_N001.lp | viz

# Exercise 3-2
# clingo --out-atomf='%s.' -V0 \
# $ENCODINGS/control/assign-a-sides.lp \
# instances/x9_y6_n54_r4_s8_ps2_pr8_u8_o8_N001.lp | \
# head -n 1 | \
# clingo --out-atomf='%s.' -V0 \
# -c horizon=40 \
# - \
# $ENCODINGS/control/{control-abc.lp,highways.lp} \
# $ENCODINGS/abc/{action-MPP.lp,goal-D-a.lp,output-MPPD.lp} \
# instances/x9_y6_n54_r4_s8_ps2_pr8_u8_o8_N001.lp | viz

# Exercise 4
# clingo --out-atomf='%s.' -V0 \
# -c horizon=30 \
# $ENCODINGS/control/{energy.lp,highways.lp} \
# $ENCODINGS/abc/{action-MPP.lp,goal-D-a.lp,output-MPPD.lp} \
# instances/x7_y6_n42_r3_s6_ps1_pr12_u24_o3_nrg_N001.lp