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
            #gamma = 0.00060483158055174284
            
            gamma = 0.0005
            print('gamma')
            print(gamma)
            #lamda = np.zeros(len(A))
            lamda = np.ones(len(A))
            x = np.zeros(len(connected))
            
            for i in range(0, self.params['max_iter']):
                n_iter = i+1

                x = np.minimum(np.maximum(LB, 1.0/(np.dot(T.T, lamda)+util.tol)), self.get_UB(connected))

                ev_power = np.zeros(self.env['evNumber'])
                for j in range(0, len(connected)):
                    ev_power[connected[j]] = x[j]

                if self.params['x']==True:
                    lamda = np.maximum(0.0, lamda - gamma*(A-np.dot(T,x)))
                else:
                    g = np.array(self.env['transRating']) - self.get_trans_load(ev_power,P,Q)
                    g = np.array([g[e] for e in U])
                  

                    lamda = np.maximum(0.0, lamda - gamma*g)
                    #print(g)

                #if np.allclose(self.get_trans_load(ev_power,P,Q), central['trans_load'], atol=0.0, rtol=self.params['tol'])==True:
                #    break
                #print(ev_power)
                #print(central['ev_power'])
                """
                sub = [0,0]
                temp = self.get_trans_load(ev_power,P,Q)
            
                sub[0] = central['trans_load'][0]+central['trans_load'][1]+central['trans_load'][2]
                sub[1] = temp[0]+temp[1]+temp[2]

                #print(abs(sub[1]-sub[0])/sub[0])
                if abs(sub[1]-sub[0]) <= self.params['tol']*sub[0]:
                    break
                """

                
                c = sum(central['ev_power'])
                d = sum(ev_power)

                if abs(d-c) <= self.params['tol']*c:
                    break 
                
                #if np.allclose(ev_power, central['ev_power'], atol=0.0, rtol=self.params['tol'])==True:
                #    break

                

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

    def convergence(self, P,Q, central={}):

        connected = self.get_connected()
        LB = np.zeros(len(connected))

        n_iter = 0
        result = {}
        
        result['params'] = {}
        result['gamma'] = {}

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
            
            gamma_star = 2.0/(m*L*S+util.tol)

            result['params']['gamma_star'] = gamma_star

            lamda = np.zeros(len(A))
            x = np.zeros(len(connected))
            
            scale = 0.6e-5
            result['params']['scale'] = scale

            for gamma in range(250, 500):
                n_iter = 0
                for i in range(0, self.params['max_iter']):
                    n_iter = i+1
                    
                    x = np.minimum(np.maximum(LB, 1.0/(np.dot(T.T, lamda)+util.tol)), self.get_UB(connected))

                    ev_power = np.zeros(self.env['evNumber'])
                    for j in range(0, len(connected)):
                        ev_power[connected[j]] = x[j]

                    if self.params['x']==True:
                        lamda = np.maximum(0.0, lamda - gamma*scale*(A-np.dot(T,x)))
                    else:
                        g = np.array(self.env['transRating']) - self.get_trans_load(ev_power,P,Q) 
                        g = np.array([g[e] for e in U])

                        lamda = np.maximum(0.0, lamda - gamma*scale*g)


                    #if np.allclose(self.get_trans_load(ev_power,P,Q), central['trans_load'], atol=0.0, rtol=self.params['tol'])==True:
                    #    break
                    #print(ev_power)
                    #print(central['ev_power'])
                    """
                    sub = [0,0]
                    temp = self.get_trans_load(ev_power,P,Q)
                
                    sub[0] = central['trans_load'][0]+central['trans_load'][1]+central['trans_load'][2]
                    sub[1] = temp[0]+temp[1]+temp[2]

                    #print(abs(sub[1]-sub[0])/sub[0])
                    if abs(sub[1]-sub[0]) <= self.params['tol']*sub[0]:
                        break
                    """

                    c = sum(central['ev_power'])
                    d = sum(ev_power)

                    if abs(d-c) <= self.params['tol']*c:
                        break 
                    #if np.allclose(ev_power, central['ev_power'], atol=0.0, rtol=self.params['tol'])==True:
                    #    break
                result['gamma'][gamma] = n_iter
            
            
        #self.update_remaining_demand(ev_power)
        #result = {'trans_load':self.get_trans_load(ev_power, P, Q).tolist(), 'ev_power':ev_power.tolist(), 'remaining_demand':self.remaining_demand.tolist(),'gamma':gamma, 'n_iter':n_iter}
        #self.current_slot += 1
        
        #print('decentral')
        #print(result['ev_power'])
        return result
