#!/bin/bash
#
#SBATCH --job-name=ltco
#SBATCH --output=ltco_rmc.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=1000000:00
#SBATCH --mem-per-cpu=256

ulimit -s unlimited
export OMP_NUM_THREADS=8

RMCProfile_PATH=/Applications/RMCProfile_package_V6.7.9_CUDA
export PGPLOT_DIR=$RMCProfile_PATH/exe/libs
export LD_LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export PATH=$PATH:$RMCProfile_PATH/exe
$RMCProfile_PATH/exe/rmcprofile glass_ceramic
