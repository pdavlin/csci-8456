#!/bin/bash

SYSTEM="clingo"
# SYSTEM="clingcon"

# ENCODINGS="action-MPP-3.lp goal-D-r.lp output-MPPD-3.lp -c horizon=$2"
# ENCODINGS="xapf/action-M.ilp   xapf/goal-m.ilp"
# ENCODINGS="xapf/action-M-XY.ilp   xapf/goal-m-XY.ilp"
# ENCODINGS="m/action-M.iclp   m/goal-m.iclp"
ENCODINGS="."
VISUALIZER="--outf=0 -V0 --out-atomf=%s. | head -n1 | visualizer"

clingo --out-atomf='%s.' -V0 \
-c horizon=15 \
$ENCODINGS/m/{action-M.lp,goal-M-mod.lp,output-M.lp} \
../instances/x11_y6_n66_r1_s8_ps1_pr8_u8_o8_N001.lp

# for f in $1/*.lp ;
# do
#     $SYSTEM $ENCODINGS $f;
# done

# # CALL="clingo1facts assign.lp $1 | clingo $ENCODINGS control.lp - $3 $VISUALIZER"
