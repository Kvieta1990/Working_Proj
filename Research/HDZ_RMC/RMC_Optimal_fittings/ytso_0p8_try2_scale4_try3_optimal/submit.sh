#!/bin/bash
#
#SBATCH --job-name=hdz_0p8
#SBATCH --output=hdz_ytso_0p8_rmc.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=1000000:00
#SBATCH --mem-per-cpu=256

ulimit -s unlimited
export OMP_NUM_THREADS=8

RMCProfile_PATH=/Applications/RMCProfile_package_V6.7.9
export PGPLOT_DIR=$RMCProfile_PATH/exe/libs
export LD_LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export PATH=$PATH:$RMCProfile_PATH/exe
$RMCProfile_PATH/exe/rmcprofile ytso_0p8
