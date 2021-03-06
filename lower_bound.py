import numpy as np
import cvxpy as cp
import utility as util

def solve(w, UB, A, T, scale=1.0):
    #w = util.f(driver_type)

    z = cp.Variable(len(UB))

    #print(A)
    #print(w)
    obj = cp.Maximize(sum(np.diag(w) * cp.log(z + util.tol)))
    #print(T)
    #print(A)
    constraints = [0 <= z, z <= UB, T * z <= A]
    #print(A)
    prob = cp.Problem(obj, constraints)
    
    # Solve with MOSEK.
    prob.solve(solver=cp.MOSEK, verbose=False)
    #print(z.value)
    return z.value * scale
