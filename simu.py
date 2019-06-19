import numpy as np
import utility as util
import DSSStartup
import sys

from tqdm import tqdm 

from algo import algo

from central_algo import central_algo
from decentral_algo import decentral_algo
from base_line_algo import base_line_algo
from base_load_algo import base_load_algo

simu_params = util.load_dict(sys.argv[1])

env = util.load_dict(simu_params['env_path'])

DSSObj = DSSStartup.dssstartup('master33Full.dss')

# Initial P and Q
PQ_dict = util.load_dict(simu_params['base_load_path']+'h'+str(simu_params['start_hr'])+'.txt')
P = np.array(PQ_dict['P'])
Q = np.array(PQ_dict['Q'])

algo_list = {}
for key in simu_params['algo']:
    if simu_params['algo'][key]['type']=='central_algo':
         obj = central_algo(DSSObj, env, P, Q, slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])
    elif simu_params['algo'][key]['type']=='decentral_algo':
         obj = decentral_algo(DSSObj, env, P, Q, slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])
    elif simu_params['algo'][key]['type']=='base_line_algo':
         obj = base_line_algo(DSSObj, env, P, Q, slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])
    elif simu_params['algo'][key]['type']=='base_load_algo':
         obj = base_load_algo(DSSObj, env, P, Q, slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])

    algo_list[key] = obj


result = {}
for key in algo_list:
    result[key] = {}
#result['decentral'] = {}

n_slots = int(60 / simu_params['slot_len'])

for h in tqdm(range(simu_params['start_hr'], simu_params['end_hr'])):
    PQ_dict = util.load_dict(simu_params['base_load_path']+'h'+str(h)+'.txt')
    P = np.array(PQ_dict['P'])
    Q = np.array(PQ_dict['Q'])

    for t in range(0, n_slots):
        for key in algo_list:
            if key == 'decentral':
                continue

            index = h*n_slots + t
            result[key][index] = algo_list[key].update(P,Q)

            if key == 'central':
                result['decentral'][index] = algo_list['decentral'].update(P,Q, result['central'][index])

"""
'decentral':{'type':'decentral_algo', 'params':{'theta':0.8, 'step_factor':25e4, 'tol':0.1, 'max_iter':1000}},
central_obj = central_algo(DSSObj, mat, env, start=1400, mode=mode, params={'theta':0.8})
result['central'] = {}

decentral_obj = decentral_algo(DSSObj, mat, env,start=1400, mode=mode, params={'theta':0.8, 'step_factor':5e10, 'tol':0.1, 'max_iter':1000})
result['decentral'] = {}

llf_obj = base_algo(DSSObj, mat, env,start=1400, mode=mode, params={'value':'llf'})
result['llf'] = {}

edf_obj = base_algo(DSSObj, mat, env,start=1400, mode=mode, params={'value':'edf'})
result['edf'] = {}

#base_load_obj = algo(DSSObj, mat, env)
result['base_load'] = {}

for t in tqdm(range(1400, 1439)):
    result['central'][t] = central_obj.update()
    result['decentral'][t] = decentral_obj.update(central_power=result['central'][t]['trans_load'])
    print(result['decentral'][t]['gamma'])
    print(result['decentral'][t]['n_iter'])
    result['llf'][t] = llf_obj.update()
    result['edf'][t] = edf_obj.update()
    result['base_load'][t] = {'trans_load':central_obj.get_trans_load(np.zeros(env['evNumber'])).tolist()}
"""
util.save_dict(simu_params['save_path'], result)
