#!/bin/bash
#
#SBATCH --job-name=hdz_1p0
#SBATCH --output=hdz_ytso_1p0_rmc.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=1000000:00
#SBATCH --mem-per-cpu=256

ulimit -s unlimited
export OMP_NUM_THREADS=4

RMCProfile_PATH=/Applications/RMCProfile_package_V6.7.9
export PGPLOT_DIR=$RMCProfile_PATH/exe/libs
export LD_LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export PATH=$PATH:$RMCProfile_PATH/exe
$RMCProfile_PATH/exe/rmcprofile ytso_1p0
