import numpy as np
import utility as util
import GetTransPower
import RunPF
import DSSStartup

from tqdm import tqdm
from matplotlib import pyplot as plt

result_path = 'result/500_mix_w.txt'
base_load_path = 'base_load/10_min/'
env_path = 'env/500_mix.txt'

DSSObj = DSSStartup.dssstartup('master33Full.dss')

tol = 0.05

result = util.load_dict(result_path)
env = util.load_dict(env_path)

slot = 140
connected = result['central'][slot]['connected']


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
    return 6.6*np.ones(len(connected))
    
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


T, A, U = get_TAU()
scale = 1e-4
legend = []

for tol in [0.05, 0.01]:
    gammas = []
    iters = []
    for gamma in tqdm(range(5, 100)):
        gammas.append(gamma)
        n_iter = 0

        lamda = np.ones(len(A))
        x = np.zeros(len(connected))
        LB = np.zeros(len(connected))

        for i in range(0, 200):
            n_iter = i+1
            
            x = np.minimum(np.maximum(LB, w/np.dot(T.T, lamda)), get_UB())

            ev_power = np.zeros(env['evNumber'])
            for j in range(0, len(connected)):
                ev_power[connected[j]] = x[j]

            g = np.array(env['transRating']) - get_trans_load(ev_power) 
            g = np.array([g[e] for e in U])

            lamda = np.maximum(0.0, lamda - gamma*scale*g)


            #if np.allclose(self.get_trans_load(ev_power,P,Q), central['trans_load'], atol=0.0, rtol=self.params['tol'])==True:
            #    break
            #print(ev_power)
            #print(central['ev_power'])
            '''
            sub = [0,0]
            temp = get_trans_load(ev_power)

            sub[0] = result['central'][slot]['trans_load'][0]+result['central'][slot]['trans_load'][1]+result['central'][slot]['trans_load'][2]
            sub[1] = temp[0]+temp[1]+temp[2]
            
            #print(abs(sub[1]-sub[0])/sub[0])
            if abs(sub[1]-sub[0]) <= tol*sub[0]:
                break
            '''
            
            c = sum(result['central'][slot]['ev_power'])
            d = sum(ev_power)

            if abs(d-c) <= tol*c:
                break 
            
            #if np.allclose(ev_power, central['ev_power'], atol=0.0, rtol=self.params['tol'])==True:
            #    break
        print(n_iter)
        iters.append(n_iter)

    legend.append(str(100-tol*100)+'%')
    plt.plot(gammas, iters)

plt.legend(legend)
plt.title('Convergence Analysis of Decentral Algo')
plt.xlabel('step-size ($x10^{-4}$)')
plt.ylabel('# of iterations')

plt.show()
