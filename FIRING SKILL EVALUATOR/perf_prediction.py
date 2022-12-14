import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression
X = np.array([[2, 33, 0.0, 11.0, 7.35], [2, 33, 0.0, 11.0, 7.35], [4, 30, 0.0, 11.0, 7.33], [1, 3, 0.0, 11.0, 7.34], [1, 3, 0.0, 11.0, 7.34], [7, 0, 1.5, 11.224657534246575, 8.108571428571429],[2, 33, 0.0, 11.0, 7.35], [2, 33, 0.0, 11.0, 7.35], [4, 30, 0.0, 11.0, 7.33], [1, 3, 0.0, 11.0, 7.34], [1, 3, 0.0, 11.0, 7.34], [7, 0, 1.5, 11.224657534246575, 8.108571428571429]])
y = [65.53, 70.68, 65.57, 66.26, 67.73, 69.3916, 66.26, 67.73, 69.3916, 65.53, 70.68, 65.57] 

reg = LinearRegression().fit(X, y)

result  = reg.predict(np.array([[1, 3, 5, 11, 7.34]]))
reg.score([[1, 3, 5, 11, 7.34]], [70.3])
