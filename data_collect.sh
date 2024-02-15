#!/bin/bash

record_time=15 # set time
filename="capture.pcap" # tcpdump_save

source /home/nuc/miniconda3/etc/profile.d/conda.sh
conda activate mmwave

# run python script
python /home/nuc/Documents/mmwave/feb12-main/test_mmwave.py &

# run tcpdump
sudo timeout ${record_time} tcpdump -i enp89s0 -w ${filename} -B 524288

# optional: deactivate the conda environment
conda deactivate
