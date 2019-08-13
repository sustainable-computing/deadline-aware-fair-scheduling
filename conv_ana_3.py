import numpy as np
import utility as util
import GetTransPower
import RunPF
import DSSStartup

from tqdm import tqdm
from matplotlib import pyplot as plt

result_path = 'result/500_mix_f.txt'
base_load_path = 'base_load/10_min/'
env_path = 'env/500_mix.txt'

DSSObj = DSSStartup.dssstartup('master33Full.dss')

tol = 0.0001

result = util.load_dict(result_path)
env = util.load_dict(env_path)

slot = 119
#print(result['central'][slot]['x'])
connected = result['central'][slot]['connected']
#print('connected')
#print(len(connected))
factor = 0.1

n_slot_per_hr = 6
h = slot//n_slot_per_hr

bl_scale = 1.3
PQ_dict = util.load_dict(base_load_path+'h'+str(h)+'.txt')

P = bl_scale*np.array(PQ_dict['P'])
Q = bl_scale*np.array(PQ_dict['Q'])

def get_driver_type():
    driver_type = []
    for c in connected:
        driver_type.append(env['evDriverType'][c])
    return np.array(driver_type)
    
#w = util.f(get_driver_type())
w = result['central'][slot]['w']

def get_trans_load(ev_power): # In kVA
    DSSCircuit = RunPF.runPF(DSSObj, P[:, h%n_slot_per_hr], Q[:, h%n_slot_per_hr], env['evNodeNumber'], ev_power)
    
    
    # get the transformer power magnitudes
    trans_loads = GetTransPower.getTransPower(DSSCircuit)
    trans_loads = np.ravel(trans_loads)

    trans_loads = [np.sqrt(trans_loads[i]**2+trans_loads[i+1]**2) for i in range(0,len(trans_loads),2)]
    return(np.array(trans_loads))
    
def get_UB():
    return 8.0*np.ones(len(connected))
    
def get_available(trans_loads):
    return 0.9*np.maximum(0.0, np.array(env['transRating']) - trans_loads)
    
def get_TAU(whole=0):
        if whole==1:
            connected_ = np.array(range(0,env['evNumber']))
        T = []
        A = []
        U = []
        trans_number = [env['evNodeNumber'][e]//55+1 for e in connected]
        phase_number = [env['loadPhase'][env['evNodeNumber'][e]%55]-1 for e in connected]
        
        available = get_available(get_trans_load(np.zeros(env['evNumber'])))
        # For primary tranformers
        for i in range(0,3):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if phase_number[j]==i:
                    temp[j] = 1
            if np.sum(temp)>0 or whole==1:
                T.append(temp)
                A.append(available[i])
                U.append(i)
        
        # For secondary transformers
        for i in range(3, len(available)):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if trans_number[j]==(i//3) and phase_number[j]==(i%3):
                    temp[j] = 1
            if np.sum(temp)>0 or whole==1:
                T.append(temp)
                A.append(available[i])
                U.append(i)
        A = np.array(A)
        #A = np.maximum(util.tol, A)
        return (np.array(T), A, np.array(U))

def get_load_nabla(T,A,U,LB,mu):

    x = np.minimum(np.maximum(LB, w/np.dot(T.T, (mu+tol)**2)), get_UB())

    ev_power = np.zeros(env['evNumber'])
    for j in range(0, len(connected)):
        ev_power[connected[j]] = x[j]
    
    load = get_trans_load(ev_power)
    nabla = np.array(env['transRating']) - load

    load = np.array([load[e] for e in U])

    nabla = 2 * mu * np.array([nabla[e] for e in U])

    return (load, nabla, x)
    
'''
def get_mu(mu_k, load_k, load_k_1, nabla_k, nabla_k_1, gamma=None):
    if gamma==None:
        mu = mu_k - ((load_k-load_k_1)/(nabla_k-nabla_k_1))*nabla_k
    else:
        mu = mu_k - gamma * ((load_k-load_k_1)/(nabla_k-nabla_k_1))*nabla_k
    return mu
'''
def get_mu(mu_k, mu_k_1, load_k, load_k_1, nabla_k, gamma=None):
    rating_load = nabla_k / (mu_k+tol)
    hessian = rating_load - 2 * mu_k * ((load_k-load_k_1)/(mu_k-mu_k_1+tol)) + tol
    hessian = factor / hessian
    if gamma==None: 
        mu = mu_k - hessian * nabla_k
    else:
        #mu = rating_load - 2 * mu_k * ((load_k-load_k_1)/(mu_k-mu_K_1))
        mu = mu_k - gamma * hessian * nabla_k
    return mu

T, A, U = get_TAU()
scale = 1e-5
legend = []

for name in ['diag','gpa']:
    gammas = []
    iters = []
    for gamma in tqdm(range(5, 100)):
        gammas.append(gamma)
        n_iter = 0

        lamda = np.ones(len(A))
        x = np.zeros(len(connected))
        LB = np.zeros(len(connected))

        if name == 'diag':
            ##################################################################
            mu_k_1 = 1.0*np.ones(len(A))
            load_k_1 = np.zeros(len(A))
        
            mu_k = np.ones(len(A))
        
            (load_k, nabla_k, _) = get_load_nabla(T,A,U,LB,mu_k)
            #lamda_k_1 = np.zeros(len(lamda))
            #lamda_k = np.copy( lamda )
            '''
            x = np.minimum(np.maximum(LB, w/np.dot(T.T, lamda_k**2)), get_UB())

            ev_power = np.zeros(env['evNumber'])
            load_k_1 = get_trans_load(ev_power)
            for j in range(0, len(connected)):
                ev_power[connected[j]] = x[j]
            
            
            load_k = get_trans_load(ev_power)
            
            g = np.array(env['transRating']) - load_k
            rating_load = np.copy(g)
            rating_load = np.array([rating_load[e] for e in U])
            g = 2 * lamda_k * np.array([g[e] for e in U])
            
            load_k_1 = np.array([load_k_1[e] for e in U])
            load_k = np.array([load_k[e] for e in U])
            '''
            ###################################################################

        for i in range(0, 200):
            n_iter = i+1
            
            if name == 'diag':
                #lamda = lamda - util.lbfgs_get_direction(history, g_k)
                #lamda = 2 * rating_load - 2 * lamda_k * ( ( load_k - load_k_1 ) / ( lamda_k - lamda_k_1 + 1e-7) )
                mu = get_mu(mu_k, mu_k_1, load_k, load_k_1, nabla_k)

                load_k_1 = np.copy(load_k)
                mu_k_1 = np.copy(mu_k)
                
                (load_k, nabla_k, x) = get_load_nabla(T,A,U,LB,mu)
                
                mu_k = np.copy(mu)
                
                #lamda = lamda_k - ( ( load_k-load_k_1 )/( nabla_k-nabla_k_1 ) ) * nabla_k
                #print(lamda)
                #lamda = 1.0 / (lamda+1e-7)
                #g = 2 * lamda * g
                #lamda = lamda_k - lamda * g
                #lamda = lamda - gamma*scale*g
                #x = np.minimum(np.maximum(LB, w/np.dot(T.T, (lamda+1e-7)**2)), get_UB())
            else:
                x = np.minimum(np.maximum(LB, w/np.dot(T.T, (lamda+1e-7))), get_UB())
        

            ev_power = np.zeros(env['evNumber'])
            for j in range(0, len(connected)):
                ev_power[connected[j]] = x[j]

            #load = get_trans_load(ev_power)
            #nabla = np.array(env['transRating']) - load
            
            #g = ( np.array(env['transRating']) - load )
            if name=='gpa':
                g = np.array(env['transRating']) - get_trans_load(ev_power) 
                g = np.array([g[e] for e in U])
                #print(gamma*scale)
                lamda = np.maximum(0.0, lamda - gamma*scale*g)
            '''
            if name == 'diag':
                #g = np.array(env['transRating']) - load_k
                #rating_load = np.copy(g)
                #rating_load = np.array([rating_load[e] for e in U])
                #g = 2 * lamda * np.array([g[e] for e in U])
                nabla = 2 * lamda * np.array([nabla[e] for e in U])

                load = np.array([load[e] for e in U])
                load_k_1 = np.copy( load_k )
                load_k = np.copy( load )
                
                lamda_k_1 = np.copy(lamda_k)
                lamda_k = np.copy(lamda)
            else:
                g = np.array([g[e] for e in U])
                lamda = np.maximum(0.0, lamda - gamma*scale*g)
            '''

            #if np.allclose(get_trans_load(ev_power), result['central'][slot]['trans_load'], atol=0.0, rtol=0.05)==True:
            #    break
            #print(ev_power)
            #print(central['ev_power'])
            '''
            sub = [0,0]
            temp = get_trans_load(ev_power)

            sub[0] = result['central'][slot]['trans_load'][0]+result['central'][slot]['trans_load'][1]+result['central'][slot]['trans_load'][2]
            sub[1] = temp[0]+temp[1]+temp[2]
            
            #print(abs(sub[1]-sub[0])/sub[0])
            if abs(sub[1]-sub[0]) <= 0.05*sub[0]:
                break
            
            '''
            c = sum(result['central'][slot]['ev_power'])
            d = sum(ev_power)

            if abs(d-c) <= 0.05*c:
                break 
            
            #if np.allclose(x, result['central'][slot]['x'], atol=0.0, rtol=0.05)==True:
            #    break
        
        print(n_iter)
        #print('central')
        #print(result['central'][slot]['x'])
        #print('decentral')
        #print(x)
        iters.append(n_iter)

    #legend.append(str(100-tol*100)+'%')
    
    legend.append(name)

    
    plt.plot(gammas, iters)

plt.legend(legend)
plt.title('95% Convergence Analysis of Decentral Algo')
plt.xlabel('step-size ($x10^{-5}$)')
plt.ylabel('# of iterations')

plt.show()
