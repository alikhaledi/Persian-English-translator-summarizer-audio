#!/bin/bash

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate audio

# Run the Streamlit app
streamlit run persian_english_webapp.py 