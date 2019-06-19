from algo import algo 
import numpy as np
import lower_bound as lb
import primal
import utility as util

class decentral_algo(algo):
    def update(self, P, Q, central={}):
        connected = self.get_connected()
        LB = np.zeros(len(connected))

        n_iter = 0
        gamma = 0.0

        urgent = self.get_urgent(connected)
        if len(urgent)>0:
            T, A, _ = self.get_TAU(urgent, P, Q)
            ur_LB = lb.solve(self.get_laxity(urgent), self.params['theta'], self.get_UB(urgent), A, T)
            
            for i in range(0, len(urgent)):
                j, = np.where(connected == urgent[i])
                LB[j[0]] = ur_LB[i]

        if len(connected)>0:
            T, A, U = self.get_TAU(connected, P, Q)
            
            m  = (np.amax(self.get_UB(connected)))**2
            L = np.amax(np.sum(T, axis=0))
            S = np.amax(np.sum(T, axis=1))
            
            gamma = (2.0*self.params['step_factor'])/(m*L*S+util.tol)
            #gamma = 3.0483158055174284e-05
            #gamma = 4.0e-05
            print('gamma')
            print(gamma)
            lamda = np.zeros(len(A))
            #lamda = 0.1*np.ones(len(A))
            x = np.zeros(len(connected))
            
            
            for i in range(0, self.params['max_iter']):
                n_iter = i+1
                x = np.minimum(np.maximum(LB, 1.0/(np.dot(T.T, lamda)+util.tol)), self.get_UB(connected))
                #print(x)
                ev_power = np.zeros(self.env['evNumber'])
                for j in range(0, len(connected)):
                    ev_power[connected[j]] = x[j]

                if self.params['x']==True:
                    lamda = np.maximum(0.0, lamda - gamma*(A-np.dot(T,x)))
                else:
                    g = self.env['transRating'] - self.get_trans_load(ev_power,P,Q)
                    g = np.array([g[e] for e in U])

                    lamda = np.maximum(0.0, lamda - gamma*g)


                #if np.allclose(self.get_trans_load(ev_power,P,Q), central['trans_load'], atol=0.0, rtol=self.params['tol'])==True:
                #    break
                #print(ev_power)
                #print(central['ev_power'])
                if np.allclose(ev_power, central['ev_power'], atol=0.0, rtol=self.params['tol'])==True:
                    break

        print(n_iter)

        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
            
            
        self.update_remaining_demand(ev_power)
        result = {'trans_load':self.get_trans_load(ev_power, P, Q).tolist(), 'ev_power':ev_power.tolist(), 'remaining_demand':self.remaining_demand.tolist(),'gamma':gamma, 'n_iter':n_iter}
        self.current_slot += 1
        
        #print('decentral')
        #print(result['ev_power'])
        return result
            
