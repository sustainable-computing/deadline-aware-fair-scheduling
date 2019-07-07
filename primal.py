import numpy as np
import utility as util
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint

######### The Optimization Problem #########
#Maximize:    \sum_e log x_e
#Subject to:  LB_e <= x_e <= UB_e,
#             Tx <= A
# where, T is the (L by E) topology matrix
#and, A is the available resource vector
############################################

############## Objective Function ##########################
# We are posing the problem as a minimization task
# So taking negative of logarithm:
def obj(x):
    return -np.sum(util.log(x))
############################################################

############# Derivative of Objective Function #############
def obj_der(x):
    return -util.reciprocal(x)
############################################################

############# Hessian of Objective Function ################
def obj_hess(x):
    return np.diag(util.reciprocal(x*x))
############################################################

######################## Solving ###########################
def solve(LB,UB,A,T):
    ################ Making Numpy Array ###################
    LB = np.array(LB)
    UB = np.array(UB)
    A = np.array(A)
    T = np.array(T)
    ###################################################### 
    
    ################ Making Sure that UB >= LB #############
    '''
    for i in range(len(UB)):
        if LB[i] >= UB[i]:
            print('Warning (primal.py): LB >= UB')
            print('LB: {}'.format(LB[i]))
            print('UB: {}'.format(UB[i]))
            UB[i] = LB[i]+util.tol
    '''
    ########################################################
    
    ##################### Optimization Variables ###########
    # LB <= x <= UB
    # To avoid small values we multiply each bound by a factor
    bounds = Bounds(LB/util.tol, UB/util.tol)
    ########################################################

    ##################### Constraints ######################
    # 0.0 <= Tx <= A
    linear_constraint = LinearConstraint(T, 0.0, A/util.tol)
    ########################################################

    ##################### Initial Guess ####################
    x0 = UB/util.tol
    #x0 = np.zeros(len(LB))
    ########################################################
    method = 'trust-constr'
    #method = 'SLSQP'
    ##################### Solution #########################
    res = minimize(obj, x0, method=method, 
                   jac=obj_der, hess=obj_hess, 
                   constraints=[linear_constraint], 
                   options={'gtol':util.tol, 'verbose':0, 'maxiter':1000}, bounds=bounds)
    ########################################################
    return res.x*util.tol
    return [0.0 if e<=util.tol else e*util.tol for e in res.x]
############################################################  

if __name__=="__main__":
    ########### Testing ##############
    # Problem:
    # maximize:    log x1 + log x2
    # subject to:  1.0 <= x1 <= 10.0
    #              3.0 <= x2 <= 8.0
    #              x1 + x2 <= 10.0 
    LB = [0.0,3.0]
    UB = [0.0001,3.0]
    A = [10.0]
    T = [[1,1]]

    print(solve(LB,UB,A,T))
