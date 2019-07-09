import numpy as np
import cvxpy as cp
import utility as util

def solve(driver_type, UB, A, T):
    w = util.f(driver_type)

    x = cp.Variable(len(UB))
    obj = cp.Maximize(sum(np.diag(w) * cp.log(x)))

    constraints = [0 <= x, x <= UB, T * x <= A]
    #print(A)
    prob = cp.Problem(obj, constraints)
    
    # Solve with MOSEK.
    prob.solve(solver=cp.MOSEK, verbose=False)
    
    return x.value
