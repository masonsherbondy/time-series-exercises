import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_RMSE(y, y_hat):
    #calculate residuals
    residuals = y - y_hat
    
    #residuals squared
    residuals_squared = residuals ** 2
    
    #sum of squared errors
    SSE = residuals_squared.sum()
    
    #explained sum of squares
    ESS = sum((y_hat - y.mean())**2)
    
    #total sum of squares
    TSS = ESS + SSE
    
    #mean of squared errors
    MSE = SSE / len(y)
    
    #root of mean of squared errors
    RMSE = MSE ** (1/2)
    
    return RMSE