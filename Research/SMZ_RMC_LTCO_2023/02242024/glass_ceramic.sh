#!/bin/bash

for var in `ls`;
do
    echo $var | grep -q "glcm_try2_" && a=1 || a=0
    if [ $a == 1 ] ; then
        echo $var
        cp li_network_glass_ceramic_cl.py $var
        cd $var
        /opt/conda/envs/RMCProfile/bin/python li_network_glass_ceramic_cl.py
        cd ..
    fi
done
