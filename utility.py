import numpy as np
import sys


tol = 1e-4
inf = 1e8

def log(x):
    #return np.log(x)
    #return np.array([0.0 if e <= 0.0 else np.log(e)+inf for e in x])
    return np.array([-12 if e <= 1e-12 else np.log(e) for e in x])


def reciprocal(x):
    return np.array([inf if e <= 0.0 else 1.0 / e for e in x])


def w(x, y):
    x = np.array(x)
    y = np.array(y)
    z = -x-y
    return np.exp(z/100.0)

def f(x):
    #shift = 500
    #return np.array([1.0 if e <= -shift else e + shift + 1 for e in x])
    #return np.ones(len(x))
    temp = []
    for e in x:
        if e==0:
            temp.append(4.0)
        elif e==1:
            temp.append(1.0)
        elif e==2:
            temp.append(1.0)
        else:
            print('e')
            print(e)

    return np.array(temp)

def g(x):
    #return 1.0 / (1.0 + np.exp(x))
    temp = []
    for e in x:
        if e<=0.0:
            temp.append(3.0)
        elif e<=10.0:
            temp.append(2.0)
        else:
            temp.append(1.0)
    return np.array(temp)

def jain_index(x, w=None):
    x = np.array(x)
    if w != None:
        x = x * np.array(w)
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
    return eval(data.replace('array(', '').replace('])', ']'))

