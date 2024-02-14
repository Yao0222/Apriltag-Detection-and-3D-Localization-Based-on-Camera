#!/bin/bash

source /home/nuc/miniconda3/etc/profile.d/conda.sh
conda activate mmwave

# run python script
python /home/nuc/Documents/mmwave/feb12-main/test_mmwave.py &

# optional: deactivate the conda environment
conda deactivate
