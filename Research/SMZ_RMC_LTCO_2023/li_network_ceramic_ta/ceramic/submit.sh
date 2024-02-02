#!/bin/bash
#
#SBATCH --job-name=ceramic
#SBATCH --output=ceramic.out
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=1000000:00
#SBATCH --mem-per-cpu=256

ulimit -s unlimited

source /opt/conda/etc/profile.d/conda.sh
conda activate pymatgen
python local_env_extractor.py
conda deactivate
