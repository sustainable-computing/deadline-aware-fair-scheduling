from algo import algo
import utility as util
import numpy as np, lower_bound as lb, primal, sys

class central_algo(algo):

    def update(self, P, Q):
        connected = self.get_connected()
        #LB = np.zeros(len(connected))
        #urgent = self.get_urgent(connected)
        x = []
        w = []
        '''
        if len(urgent) > 0:
            #print('yes')
            T, A, _ = self.get_TAU(urgent,P,Q)
            ur_UB = self.get_UB(urgent)
            ur_LB = lb.solve(self.get_driver_type(urgent), self.params['theta'], ur_UB, A, T)
            
            for i in range(len(ur_UB)):
                if ur_LB[i] >= ur_UB[i]:
                    print('Warning (Ganjam): LB >= UB')
                    print('LB: {}'.format(ur_LB[i]))
                    print('UB: {}'.format(ur_UB[i]))
            
            #ur_LB = lb.solve(self.get_laxity(urgent), self.params['theta'], self.get_UB(urgent), A, T)
            
            for i in range(0, len(urgent)):
                j, = np.where(connected == urgent[i])
                LB[j[0]] = ur_LB[i]

            #print(LB)
        '''
        if len(connected) > 0:
            T, A, U = self.get_TAU(connected,P,Q)
            
            #x = primal.solve(LB, self.get_UB(connected), A, T)
            #print(A)
            #print(self.get_UB(connected))
            #x = lb.solve(self.get_driver_type(connected), self.get_claimed(connected), self.get_over_time(connected), self.get_UB(connected), A, T)
            w = util.f(self.get_driver_type(connected)) * util.g(self.get_laxity(connected, scale=0.0))
            
            #laxity = self.get_laxity(connected)
            #w = w * (144-laxity)

            x = lb.solve(w=w, UB=self.get_UB(connected), A=A, T=T)
            #print(x)
            #x = primal.solve(np.zeros(len(connected)), 10*np.ones(len(connected)), A, T)
            #x = primal.solve(np.zeros(len(connected)), self.get_UB(connected)-LB+util.tol, A, T)


        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
        #T,A,_ = self.get_TAU(connected, P,Q, whole=1)
        #print('A')
        #print(A)
        #print('E')
        #print(np.dot(T, ev_power))
        #x = (np.array(x) - LB).tolist()
       

        self.update_remaining_demand(ev_power)

        result = {'trans_load':self.get_trans_load(ev_power, P, Q).tolist(), 'ev_power':ev_power.tolist(), 'x':x, 'connected':connected.tolist(), 'remaining_demand':self.remaining_demand.tolist(), 'w':w}

        self.current_slot += 1

        return result

