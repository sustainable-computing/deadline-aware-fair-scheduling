import numpy as np
import utility as util
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

############### Updating Weights ###############
w = np.array([])
def w_update(driver_type, claimed_duration):
    laxity = np.asarray(driver_type)
    global w
    w = util.f(driver_type)*(144 - np.array(claimed_duration))
################################################

############## Objective Function ##########################
# We are posing the problem as a minimization task
# So taking negative of logarithm:
def obj(x):
    global w
    #return np.sum(w*x*x)
    return -np.sum(w*util.log(x))
############################################################

############# Derivative of Objective Function #############
def obj_der(x):
    global w
    #return 2*w*x
    return -w*util.reciprocal(x)
############################################################

############# Hessian of Objective Function ################
def obj_hess(x):
    global w
    #return np.diag(2*w*np.ones(len(x)))
    return np.diag(w*util.reciprocal(x*x))
############################################################

######################## Solving ###########################
def solve(driver_type, claimed_duration, if_over_time, UB, A, T):
    
    # Giving weights according to laxity and urgency
    w_update(driver_type, claimed_duration)

    # Lower bounds
    LB = np.zeros(len(UB))
    
    ################ Changing UB Based on Over-Time ##########
    for i in range(len(UB)):
        if if_over_time[i]==True:
            UB[i] *= 0.4
    
    ################ Making Numpy Array ###################
    LB = np.array(LB)/util.tol
    UB = np.array(UB)/util.tol
    A = np.array(A)/util.tol
    T = np.array(T)
    ###################################################### 

    
    ################ Making Sure that UB >= LB #############
    '''
    for i in range(len(UB)):
        if LB[i] >= UB[i]:
            print('Warning (lower_bound.py): LB >= UB')
            print('LB: {}'.format(LB[i]))
            print('UB: {}'.format(UB[i]))
            UB[i] = LB[i]+util.tol
    '''
    ########################################################
    
    ##################### Optimization Variables ###########
    # LB <= x <= UB
    bounds = Bounds(LB, UB)
    ########################################################

    ##################### Constraints ######################
    # 0.0 <= Tx <= theta*A
    #linear_constraint = LinearConstraint(T, 0.0, theta*A)
    ########################################################

    #method = 'trust-constr'
    method = 'SLSQP'
    
    ##################### Solution #########################
    #print(T)
    
    ineq_cons = {'type': 'ineq',
                  'fun' : lambda x: A - np.dot(T,x),
                  'jac' : lambda x: -T}
    maxiter = 600
    for i in range(0,10):
        print('Try {}'.format(i))
        ##################### Initial Guess ####################
        a = np.random.uniform(high=1.0)
        x0 = a*LB + (1.0-a)*UB
        #print(LB)
        #x0 = LB
        ########################################################
        res = minimize(obj, x0, method=method, 
                       jac=obj_der, 
                       constraints=[ineq_cons], 
                       options={'ftol':1e-6, 'maxiter':maxiter, 'disp':True}, bounds=bounds)
        if res.success==True:
            break
        #if res.status == 9:
        maxiter += 100
    
    '''
    res = minimize(obj, x0, method=method, 
                   jac=obj_der, hess=obj_hess, 
                   constraints=[linear_constraint], 
                   options={'disp':True}, bounds=bounds)
    Inequality constraints incompatible    (Exit mode 4)
    ########################################################
    '''
    #print(A/util.tol-np.dot(T,res.x))
    return res.x*util.tol
    #return [0.0 if e<=util.tol else e for e in res.x]
############################################################  

if __name__=="__main__":
    ########### Testing ##############
    # Problem:
    # maximize:    log x1 + log x2
    # subject to:  1.0 <= x1 <= 10.0
    #              3.0 <= x2 <= 8.0
    #              x1 + x2 <= 10.0 
    laxity = [2,2]
    UB = [10.0,10.0]
    A = [30.0]
    T = [[1,1]]
    print(solve(laxity,0.95,UB,A,T))
