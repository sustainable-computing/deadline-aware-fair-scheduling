from algo import algo 
import numpy as np
import lower_bound as lb
import primal
import utility as util

class gpa_algo(algo):
    def update(self, P, Q, central={}):

        connected = self.get_connected()

        #w = util.f(self.get_driver_type(connected)) * util.g(self.get_laxity(connected, scale=0.0))
        w = util.w(self.get_discrepancy(connected), self.get_laxity(connected, scale=0.0))
        #laxity = self.get_laxity(connected)
        #w = w * (144-laxity)

        LB = np.zeros(len(connected))

        n_iter = 0
        gamma = 0.0
        x = []
        '''
        urgent = self.get_urgent(connected)
        if len(urgent)>0:
            T, A, _ = self.get_TAU(urgent, P, Q)
            ur_LB = lb.solve(self.get_laxity(urgent), self.params['theta'], self.get_UB(urgent), A, T)
            
            for i in range(0, len(urgent)):
                j, = np.where(connected == urgent[i])
                LB[j[0]] = ur_LB[i]
        '''
        if len(connected)>0:
            T, A, U = self.get_TAU(connected, P, Q)
            '''
            m  = (np.amax(self.get_UB(connected)))**2
            L = np.amax(np.sum(T, axis=0))
            S = np.amax(np.sum(T, axis=1))
            '''
            #gamma = (2.0*self.params['step_factor'])/(m*L*S+util.tol)
            #gamma = 0.00060483158055174284
            
            gamma = 0.0015
            #print('gamma')
            #print(gamma)
            #lamda = np.zeros(len(A))
            lamda = np.ones(len(A))
            #print(np.dot(T.T, lamda))
            x = np.zeros(len(connected))
            
            for i in range(0, self.params['max_iter']):
            #for i in range(0, 40):
                n_iter = i+1
                x = np.minimum(np.maximum(LB, w/util.non_zero( np.dot(T.T, lamda) )), self.get_UB(connected))

                ev_power = np.zeros(self.env['evNumber'])
                for j in range(0, len(connected)):
                    ev_power[connected[j]] = x[j]
                #self.update_remaining_demand(ev_power, self.slot_len_in_min/self.params['max_iter'])

                g = np.array(self.env['transRating']) - self.get_trans_load(ev_power,P,Q)
                g = np.array([g[e] for e in U])
                  

                lamda = np.maximum(0.0, lamda - gamma*g)

                #if np.allclose(self.get_trans_load(ev_power,P,Q), central['trans_load'], atol=0.0, rtol=self.params['tol'])==True:
                #    break
                #print(ev_power)
                #print(central['ev_power'])
                '''
                sub = [0,0]
                temp = self.get_trans_load(ev_power,P,Q)
            
                sub[0] = central['trans_load'][0]+central['trans_load'][1]+central['trans_load'][2]
                sub[1] = temp[0]+temp[1]+temp[2]

                #print(abs(sub[1]-sub[0])/sub[0])
                if abs(sub[1]-sub[0]) <= self.params['tol']*sub[0]:
                    break
                '''

                
                c = sum(central['ev_power'])
                d = sum(ev_power)

                if abs(d-c) <= self.params['tol']*c:
                    break 
                
                #if np.allclose(ev_power, central['ev_power'], atol=0.0, rtol=self.params['tol'])==True:
                #    break

                
        print('gpa')
        print(n_iter)
        #print(x)
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
        self.update_remaining_demand(ev_power, self.slot_len_in_min)
        '''
        c = sum(central['ev_power'])
        d = sum(ev_power)
        z = 1 - abs(d-c)/(c + util.tol)

        print( z*100 )
        '''
        #self.update_remaining_demand(ev_power)

        result = {'trans_load':self.get_trans_load(ev_power, P, Q).tolist(), 'ev_power':ev_power.tolist(),'x':x, 'connected':connected.tolist(), 'remaining_demand':self.remaining_demand.tolist(),'gamma':gamma, 'n_iter':n_iter}
        self.current_slot += 1
        
        #print('decentral')
        #print(result['ev_power'])
        return result
