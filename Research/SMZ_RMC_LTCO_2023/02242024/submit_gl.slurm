#!/bin/bash
#SBATCH -t 21:00:00
#SBATCH -N 1
#SBATCH -o SMZ_RMC_GL-%j
#SBATCH -q regular
#SBATCH -J SMZ_RMC_GL
#SBATCH -C cpu
#SBATCH --mail-user=zyroc1990@gmail.com
#SBATCH --mail-type=ALL
#SBATCH --array=0-9

#OpenMP settings:
export OMP_NUM_THREADS=8
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

RMCProfile_PATH=/global/homes/y/y8z/Packages/RMCProfile_package_V6.7.9.5
export PGPLOT_DIR=$RMCProfile_PATH/exe/libs
export LD_LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export LIBRARY_PATH=$RMCProfile_PATH/exe/libs
export PATH=$PATH:$RMCProfile_PATH/exe

var_tmp=$((SLURM_ARRAY_TASK_ID + 1))
cd /global/homes/y/y8z/yuanpeng/SMZ_RMC_LTOC/gl_try2_RP${var_tmp}
rmcprofile glass
