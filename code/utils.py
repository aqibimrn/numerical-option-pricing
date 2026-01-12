# code/utils.py

## import libraries
import os
import time
import numpy as np
import pandas as pd

## standard error of the mean for the given samples. 
## uses sample standard deviation (degrees of freedom (ddof) = 1) / sqrt(n).
def compute_stderr(samples: np.ndarray) -> float:
    n = samples.size
    if n <= 1:
        return float("nan")
    return float(np.std(samples, ddof = 1) / np.sqrt(n))


## simple timing wrapper
def time_it(func, *args, **kwargs):
    t0 = time.time() ### mark the start time
    res = func(*args, **kwargs)
    return res, time.time() - t0 ### subtract current time with start time


## function to save results
def save_results_table(df: pd.DataFrame, folder: str):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, "results/results.csv")
    df.to_csv(filename, index=False)
