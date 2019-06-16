from algo import algo 
import numpy as np
import lower_bound as lb
import primal
import utility as util

class decentral_algo(algo):
    def update(self, central_power=[]):
        connected = self.get_connected()
        LB = np.zeros(len(connected))

        n_iter = 0
        gamma = 0.0
        flag = 0

        if len(central_power) > 0:
            flag = 1
            central_power = np.array(central_power)+util.tol

        urgent = self.get_urgent(connected)
        if len(urgent)>0:
            T, A, _ = self.get_TAU(urgent)
            ur_LB = lb.solve(self.get_laxity(urgent), self.params['theta'], self.get_UB(urgent), A, T)
            
            for i in range(0, len(urgent)):
                j, = np.where(connected == urgent[i])
                LB[j[0]] = ur_LB[i]

        if len(connected)>0:
            T, A, U = self.get_TAU(connected)
            
            m  = (np.amax(self.get_UB(connected)))**2
            L = np.amax(np.sum(T, axis=0))
            S = np.amax(np.sum(T, axis=1))
            
            gamma = (2.0*self.params['step_factor'])/(m*L*S+util.tol)
            #print('gamma')
            #print(gamma)
            lamda = np.zeros(len(A))
            #lamda = 0.1*np.ones(len(A))
            x = np.zeros(len(connected))
            
            
            for i in range(0, self.params['max_iter']):
                n_iter = i+1
                x = np.minimum(np.maximum(LB, 1.0/(np.dot(T.T, lamda)+util.tol)), self.get_UB(connected))
                #lamda = np.maximum(0.0, lamda - gamma*(A-np.dot(T,x)))

               
                ev_power = np.zeros(self.env['evNumber'])
                for i in range(0, len(connected)):
                    ev_power[connected[i]] = x[i]
                    
                g = self.env['transRating'] - self.get_trans_load(ev_power)
                g = np.array([g[e] for e in U])
                #print(g)
                #print(A-np.dot(T,x))
                lamda = np.maximum(0.0, lamda - gamma*g)
                
                if flag == 1:
                    """
                    ev_power = np.zeros(self.env['evNumber'])
                    for i in range(0, len(connected)):
                        ev_power[connected[i]] = x[i]
                    """
                    #error = np.absolute(ev_power-central_power)/central_power
                    if np.allclose(self.get_trans_load(ev_power), central_power, atol=0.0, rtol=self.params['tol'])==True:
                        #n_iter = i+1
                        break
                
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
            
            
        self.update_remaining_demand(ev_power, self.time_unit_in_sec)
        result = {'trans_load':self.get_trans_load(ev_power).tolist(), 'ev_power':ev_power.tolist(), 'remaining_demand':self.remaining_demand.tolist(),'gamma':gamma, 'n_iter':n_iter}
        self.current_time+=self.time_unit_in_sec
        
        #print('decentral')
        #print(result['ev_power'])
        return result
            
