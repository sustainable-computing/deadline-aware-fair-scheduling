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

# return: the direction abtained by a single update of lbfgs (following wikipedia)
# history: a queue (python list of pair: (s_k, y_k) of np array) with latest update at the end
# g_k: gradient
def lbfgs_get_direction(history, g_k):
    q = g_k
    latest = len(history) - 1
    e = 1e-8

    a = []
    for i in range(latest, -1, -1):
        s_i, y_i = history[i]
        r_i = 1.0 / ( np.dot(y_i, s_i) + e )
        #r_i = 1.0 / ( y_i * s_i + e )

        a_i = r_i * np.dot(s_i, q)
        #a_i = r_i * s_i * q
        a = [a_i] + a
        q = q - a_i * y_i

    gamma_k = 1.0
    if latest >= 0:
        s_k_1, y_k_1 = history[latest]
        gamma_k = np.dot(s_k_1, y_k_1) / ( np.dot(y_k_1, y_k_1) + e )
        #gamma_k = ( s_k_1 * y_k_1 ) / ( y_k_1 * y_k_1 + e )

    z = gamma_k * q
    latest += 1
    for i in range(0, latest):
        s_i, y_i = history[i]
        r_i = 1.0 / ( np.dot(y_i, s_i) + e )
        #r_i = 1.0 / ( y_i * s_i + e )
        b_i = r_i * np.dot(y_i, z)
        #b_i = r_i * y_i * z
        z = z + s_i * (a[i] - b_i)
    return z

# return: none, update the history in-place
# max_len: maximum allowed length of history
def lbfgs_update_history(history, max_len, s_k, y_k):
    if len(history) == max_len:
        history.remove( history[0] )
    s_k_copy = np.copy( s_k )
    y_k_copy = np.copy( y_k )
    history.append( (s_k_copy, y_k_copy) )
    return history
    

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

