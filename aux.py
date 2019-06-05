import numpy as np
import util
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint

######### The Optimization Problem #########
#Maximize:    \sum_e w_elog x_e
#Subject to:  LB_e <= x_e <= UB_e,
#             Tx <= \theta*A
# where, T is the (L by E) topology matrix
#, A is the available resource vector and, 
# at most \theta % of A will be provided to
# urgent users
############################################

epsilon = util.epsilon

############### Updating Weights ###############
w = np.array([])
def w_update(laxity,urgent):
    global w

    laxity = np.asarray(laxity)
    urgent = np.asarray(urgent)

    w = urgent*util.f(-laxity)
################################################

############## Objective Function ##########################
# We are posing the problem as a minimization task
# So taking negative of logarithm:
def obj(x):
    global w
    return -np.sum(w*util.log(x))
############################################################

############# Derivative of Objective Function #############
def obj_der(x):
    global w
    return -w*util.reciprocal(x)
############################################################

############# Hessian of Objective Function ################
def obj_hess(x):
    global w
    return np.diag(w*util.reciprocal(x*x))
############################################################

######################## Solving ###########################
def solve(laxity,urgent,theta,UB,A,T):
    
    # Giving weights according to laxity and urgency
    w_update(laxity,urgent)

    # \epsilon lower bound
    LB = np.zeros(len(UB))
    ##################### Optimization Variables ###########
    # LB <= x <= UB
    bounds = Bounds(LB, UB)
    ########################################################

    ##################### Constraints ######################
    # 0.0 <= Tx <= theta*A
    linear_constraint = LinearConstraint(T, 0.0, theta*np.array(A))
    ########################################################

    ##################### Initial Guess ####################
    x0 = LB
    ########################################################
    
    ##################### Solution #########################
    res = minimize(obj, x0, method='trust-constr', 
                   jac=obj_der, hess=obj_hess, 
                   constraints=[linear_constraint], 
                   options={'maxiter': 101}, bounds=bounds)
    ########################################################

    return urgent*res.x
############################################################  

if __name__=="__main__":
    ########### Testing ##############
    # Problem:
    # maximize:    log x1 + log x2
    # subject to:  1.0 <= x1 <= 10.0
    #              3.0 <= x2 <= 8.0
    #              x1 + x2 <= 10.0 

    urgent = [1,0]
    laxity = [-2,1]
    UB = [10.0,8.0]
    A = [10.0]
    T = [[1,1]]
    print(solve(laxity,urgent,0.95,UB,A,T))
