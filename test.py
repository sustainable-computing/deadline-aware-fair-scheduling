import numpy as np

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

        a_i = r_i * np.dot(s_i, q)
        a = [a_i] + a
        q = q - a_i * y_i

    gamma_k = 1.0
    if latest >= 0:
        s_k_1, y_k_1 = history[latest]
        gamma_k = np.dot(s_k_1, y_k_1) / ( np.dot(y_k_1, y_k_1) + e )

    z = gamma_k * q
    latest += 1
    for i in range(0, latest):
        s_i, y_i = history[i]
        r_i = 1.0 / ( np.dot(y_i, s_i) + e )
        b_i = r_i * np.dot(y_i, z)
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

a = []

for i in 1,2:
    a.append( (i*np.ones(2), (i+1) * np.ones(2)) )

a.remove(a[0])
print(a)

