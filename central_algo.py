from algo import algo 
import numpy as np
import LB
import primal

class central_algo(algo):
    def update(self):
        theta = 0.9
        connected = self.get_connected()
        LB_ = np.zeros(len(connected))
        
        urgent = self.get_urgent(connected)
        if len(urgent)>0:
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
            T, A = self.get_TA(urgent, available)
            
            lb = LB.solve(self.get_laxity(urgent), theta, A, T)
            for i in range(0, len(connected)):
                for j in range(0, len(urgent)):
                    if connected[i]==urgent[j]:
                        LB_[i] = lb[j]
        if len(connected)>0:
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
            T, A = self.get_TA(connected, available)
            
            x = primal.solve(LB_,self.get_UB(connected),A,T)
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
            
        self.update_remaining_demand(ev_power, self.time_unit_in_sec)
        self.current_time+=self.time_unit_in_sec

        return (self.get_trans_load(ev_power), ev_power)
            
