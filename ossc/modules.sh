#!/bin/bash

# Script to approximate venv on RA for SICSS. Run on the snellius login node.
# assume we don't need beautifulsoup4, QtPy, fastapi

echo "loading modules" 

module purge 
module load 2023 
module load Python/3.11.3-GCCcore-12.3.0
module load SciPy-bundle/2023.07-gfbf-2023a
module load scikit-learn/1.3.1-gfbf-2023a
module load PyTorch/2.1.2-foss-2023a-CUDA-12.1.1
module load TensorFlow/2.13.0-foss-2023a
# module load tensorboard/2.15.1-gfbf-2023a #-> see pip_requirements.txt
module load matplotlib/3.7.2-gfbf-2023a
module load LLVM/14.0.6-GCCcore-12.3.0-llvmlite
module load tqdm/4.66.1-GCCcore-12.3.0
module load dask/2023.9.2-foss-2023a
module load statsmodels/0.14.1-gfbf-2023a
module load scikit-image/0.22.0-foss-2023a
module load aiohttp/3.8.5-GCCcore-12.3.0
module load Graphviz/8.1.0-GCCcore-12.3.0
module load numba/0.58.1-foss-2023a
module load plotly.py/5.16.0-GCCcore-12.3.0

echo "installing from pip"
python -m venv .venv 
source .venv/bin/activate
pip install -r ossc/pip_requirements.txt


pip freeze > ossc/requirements_ossc.txt

python ossc/compare_requirements.py

deactivate 
rm -rf .venv

