import numpy as np

T = []
for i in range(0, 5):
    temp = np.zeros(3)
    temp[i%3] = 1
    T.append(temp)
T = np.array(T)
print(T.shape)
