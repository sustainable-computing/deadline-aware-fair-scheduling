from algo import algo 
import numpy as np
import lower_bound as lb
import primal
import utility as util

class diag_algo(algo):
    def get_load_nabla(self, T,A,U,LB,UB,connected,P,Q,w,mu):

        x = np.minimum(np.maximum(LB, w/util.non_zero(np.dot(T.T, mu**2))), UB)

        ev_power = np.zeros(self.env['evNumber'])
        for j in range(0, len(connected)):
            ev_power[connected[j]] = x[j]
        
        load = self.get_trans_load(ev_power,P,Q)
        nabla = np.array(self.env['transRating']) - load

        load = np.array([load[e] for e in U])

        rating_load = np.array([nabla[e] for e in U])

        nabla = 2 * mu * rating_load

        return (load, nabla, x, rating_load)

    def get_mu(self, mu_k, mu_k_1, load_k, load_k_1, nabla_k, rating_load, gamma=None):
        #rating_load = nabla_k / (mu_k+tol)
        hessian = np.absolute(rating_load - 2 * mu_k * ((load_k-load_k_1)/util.non_zero((mu_k-mu_k_1+0.5))))
        #hessian = np.array([util.tol if e <= util.tol else e for e in hessian])
        hessian = 0.3 / util.non_zero(hessian) 
        if gamma==None: 
            mu = mu_k - hessian * nabla_k
        else:
            #mu = rating_load - 2 * mu_k * ((load_k-load_k_1)/(mu_k-mu_K_1))
            mu = mu_k - gamma * hessian * nabla_k
        return mu
    def update(self, P, Q, central={}):

        connected = self.get_connected()

        #w = util.f(self.get_driver_type(connected)) * util.g(self.get_laxity(connected, scale=0.0))
        w = util.w(self.get_discrepancy(connected), self.get_laxity(connected, scale=0.0))
        #laxity = self.get_laxity(connected)
        #w = w * (144-laxity)

        LB = np.zeros(len(connected))
        UB = self.get_UB(connected)

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
            
            gamma = 0.008

            mu_k_1 = 0.0*np.ones(len(A))
            load_k_1 = np.zeros(len(A))
        
            mu_k = 1.0*np.ones(len(A))
        
            (load_k, nabla_k, _, rating_load) = self.get_load_nabla(T,A,U,LB,UB,connected,P,Q,w,mu_k)
            #print('gamma')
            #print(gamma)
            #lamda = np.zeros(len(A))
            #lamda = np.ones(len(A))
            #print(np.dot(T.T, lamda))
            #x = np.zeros(len(connected))
            
            for i in range(0, self.params['max_iter']):
            #for i in range(0, 40):
                n_iter = i+1
                mu = self.get_mu(mu_k, mu_k_1, load_k, load_k_1, nabla_k, rating_load)

                load_k_1 = np.copy(load_k)
                mu_k_1 = np.copy(mu_k)
                
                (load_k, nabla_k, x, rating_load) = self.get_load_nabla(T,A,U,LB,UB,connected,P,Q,w,mu)
                
                mu_k = np.copy(mu)

                #x = np.minimum(np.maximum(LB, w/util.non_zero( np.dot(T.T, lamda) )), self.get_UB(connected))

                ev_power = np.zeros(self.env['evNumber'])
                for j in range(0, len(connected)):
                    ev_power[connected[j]] = x[j]
                #self.update_remaining_demand(ev_power, self.slot_len_in_min/self.params['max_iter'])

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

                
        print('diag')
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
