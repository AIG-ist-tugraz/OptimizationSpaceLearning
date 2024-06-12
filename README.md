# Optimization Space Learning
This repository contains the files to reproduce the evaluation of OSL performed for the paper "Optimization Space Learning: A Lightweight, Noniterative Technique for Compiler Autotuning", accepted at SPLC'24.

## Prerequisites
You need a Python 3.10 environment with the libraries `numpy`, `scipy`, and `scikit-learn` installed (e.g., via `pip`), as well as the GCC compiler. For the training phase (see below), you also need perf installed on your device, which is why Linux is a requirement for this step. 
Also, the PolyBench benchmark must be present in the correct location on the device. However, to prevent issues with these requirements, we provide you with our complete training data.

Currently, the paths only work on Linux/Unix devices. To this end, we are currently working on a fix.

## Framework
We have a python framework which can produce the training data and do the CV-based testing for us.

### Training
**Disclaimer: A training run can take hours or even several days!**
Go to `main.py` and set the `mode` variable to `"train"`. Then run `python3 main.py`.

### Testing
Go to `main.py` and set the `mode` variable to `"test"`. Then run `python3 main.py`. The interesting thing is the output on `stdout`, which can be piped into a file. If GCC error messages are in the output, use `grep` in the command line to catch only lines that start with a digit.

### Miscellaneous
The files `feature_importance.py` and `feature_norm.py` were used to compute feature importance and to normalize the features of the program metrics data. They can be run using `python3 <filename>` with the corresponding file name instead of the placeholder.

## Data
The `data/` directory provides you with the data that needs to be present at the very beginning, such as the configurations used for training. Also, some additional files are in there, such as a list of benchmarks.

The `results/` directory contains the training results. The files named `train_*.csv` contain the training data, where the * is replaced by the configurations used for training.

## Evaluation results
The `eval/` directory contains the results of our evaluation, including all required data.

Run `python3 analysis.py` to use our analysis script and receive an overview of the performance of OSL.
