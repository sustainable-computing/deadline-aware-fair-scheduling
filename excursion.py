import numpy as np
import utility as util

file_name = 'risk_taker_500.txt'

result_path = 'result/'+file_name
env_path = 'env/'+file_name

result = util.load_dict(result_path)
env = util.load_dict(env_path)

def excursion_for_single_time_slot(trans_load, trans=[0], time=(1/6.0)):
    rating = np.array(env['transRating'])
    load = np.array(trans_load)
    
    total = 0
    for i in trans:
        diff = 3*rating[3*i] - load[3*i] - load[3*i+1] - load[3*i+2]
        if diff <= 0.0:
            total -= diff
    #print(total)
    return total*time
    
algos = {'Central', 'GPA', 'SGPA', 'LLF', 'EDF'}
output = {}

for algo in algos:
    total = 0.0
    #print(algo)
    for i in range(0,144):
        #print(i)
        total += excursion_for_single_time_slot(result[algo][i]['trans_load'])
    output[algo] = total
print(output)
