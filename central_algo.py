from algo import algo
import numpy as np, lower_bound as lb, primal, sys

class central_algo(algo):

    def update(self):
        connected = self.get_connected()
        LB = np.zeros(len(connected))
        urgent = self.get_urgent(connected)
        if len(urgent) > 0:
            T, A, _ = self.get_TA(urgent)
            ur_LB = lb.solve(self.get_laxity(urgent), self.params['theta'], self.get_UB(urgent), A, T)
            for i in range(0, len(urgent)):
                j, = np.where(connected == urgent[i])
                LB[j[0]] = ur_LB[i]

        if len(connected) > 0:
            T, A, _ = self.get_TA(connected)
            x = primal.solve(LB, self.get_UB(connected), A, T)
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]

        self.update_remaining_demand(ev_power, self.time_unit_in_sec)
        self.current_time += self.time_unit_in_sec
        result = {'trans_load':self.get_trans_load(ev_power).tolist(), 
         'ev_power':ev_power.tolist(),  'remaining_demand':self.remaining_demand.tolist()}
        return result

