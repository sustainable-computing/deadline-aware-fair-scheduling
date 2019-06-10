from algo import algo 
import utility as util
import numpy as np
import LB
import primal

class decentral_algo(algo):
    def update(self):
        theta = 0.9
        gamma = util.eps
        max_iter = 600

        connected = self.get_connected()
        y = np.zeros(len(connected))

        urgent = self.get_urgent(connected)
        if len(urgent)>0:
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
            T, A = self.get_TA(urgent, available)
            
            lb = LB.solve(self.get_laxity(urgent), theta, A, T)
            for i in range(0, len(connected)):
                for j in range(0, len(urgent)):
                    if connected[i]==urgent[j]:
                        y[i] = lb[j]
        if len(connected)>0:
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
            T, A = self.get_TA(connected, available)
            lamda = util.inf*np.ones(T.shape[0])
            x = np.zeros(len(connected))
            
            for i in range(0, max_iter):
                lamda = lamda - gamma*(A-np.dot(T,x))
                
                x = np.minimum(np.maximum(y, 1.0/(np.dot(T.T, lamda)+util.eps)), self.get_UB(connected))

        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
            
        self.update_remaining_demand(ev_power, self.time_unit_in_sec)
        self.current_time+=self.time_unit_in_sec

        return (self.get_trans_load(ev_power), ev_power)
            
