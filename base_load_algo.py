from algo import algo 
import utility as util
import numpy as np


class base_load_algo(algo):

    def update(self, P, Q):

        result = {'trans_load':self.get_trans_load(np.zeros(self.env['evNumber']), P, Q).tolist()}
        self.current_slot += 1

        return result
 
