from algo import algo 
import utility as util
import numpy as np


class base_line_algo(algo):

    def sort(self, connected, value):
        self.dtype = [('index', int), ('ev', int), ('value', float)]

        x = [(i, connected[i],value[i]) for i in range(0,len(value))]
        x = np.array(x, dtype=self.dtype)
        return np.sort(x, order='value')

    def svf(self, connected, value, A, UB, evNode, phase):
        power = np.zeros(len(value))
        B = np.copy(A)
        #B = A
        order = self.sort(connected, value)
        
        for i in range(0,len(value)):
            index = order[i][0] 
            ev_no = order[i][1]
            #print('index')
            #print(index)
            j=phase[evNode[ev_no]%55]-1
            k=3*(evNode[ev_no]//55+1)+j
            #print(j)
            #print(k)
            if B[j]>=UB[index] and B[k]>=UB[index]:
                power[index]=0.9*UB[index]
            else:
                power[index]=0.9*np.minimum(B[j],B[k])
            #print('bj')
            #print(B[j])
            #print('bk')
            #print(B[k])
            #print('p')
            #print(power[i])
            B[j] = B[j] - power[index]
            B[k] = B[k] - power[index]
        #print(power)
        """
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = power[i]
            
        U = []
        for i in range(0, 3):
            temp = []
            for j in range(len(ev_power)):
                if phase[evNode[j]%55]-1 == i:
                    temp.append(ev_power[j])
            U.append(sum(temp))
            

        for i in range(3, len(A)):
            temp = []
            for j in range(len(ev_power)):
                if 3*(evNode[j]//55+1)+phase[evNode[j]%55]-1 == i:
                    temp.append(ev_power[j])
            U.append(sum(temp))
        """
            
        return power.tolist()

    def update(self, P, Q):

        connected = self.get_connected()
        value = []
        x = []
        
        if len(connected)>0:
            if self.params['value']=='edf':
                for c in connected:
                    value.append(self.arrival[c]+self.claimed_duration[c])
                #print(value)
            if self.params['value']=='llf':
                value = self.get_laxity(connected, scale=0.0)
                

            value = np.array(value)
            #value = np.random.randint(0, 100, len(connected))
            
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber']),P,Q))
            
            x = self.svf(connected, value, available, self.get_UB(connected), self.env['evNodeNumber'], self.env['loadPhase'])
                
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
        #T,A,_ = self.get_TAU(connected, P, Q, 1)
        #print('T')
        #print(T.tolist())
        #print('A')
        #print(A)
        #print('E')
        #print(np.dot(T,ev_power))
        self.update_remaining_demand(ev_power, self.slot_len_in_min)

        result = {'trans_load':self.get_trans_load(ev_power, P, Q).tolist(), 'ev_power':ev_power.tolist(), 'x':x, 'connected':connected.tolist(), 'remaining_demand':self.remaining_demand.tolist()}

        self.current_slot += 1
        
        return result
            
