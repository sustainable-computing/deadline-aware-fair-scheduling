import numpy as np
import sys


tol = 1e-08
inf = 1e8

def log(x):
    return np.array([-inf if e <= 0.0 else np.log(e) for e in x])


def reciprocal(x):
    return np.array([inf if e <= 0.0 else 1.0 / e for e in x])


def f(x):
    shift = 500
    return np.array([0.0 if e <= -shift else e + shift + 1 for e in x])

def jain_index(x):
    x = np.array(x)
    sqr_sum = np.sum(x**2)
    if sqr_sum <= tol:
        return 1.0
    return (np.sum(x)**2)/(len(x)*sqr_sum)

def save_dict(file_name, dict_):
    f = open(file_name, 'w')
    f.write(str(dict_))
    f.close()


def load_dict(file_name):
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    return eval(data)

