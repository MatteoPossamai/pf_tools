#!/bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $script_dir

source "/home/matteopossamai/miniconda3/etc/profile.d/conda.sh"
conda activate pf
python get_transactions.py