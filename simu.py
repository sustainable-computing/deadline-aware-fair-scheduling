import numpy as np
import utility as util
import DSSStartup
import sys

from tqdm import tqdm 

from algo import algo

from central_algo import central_algo
from gpa_algo import gpa_algo
from diag_algo import diag_algo
from admm_algo import admm_algo
from base_line_algo import base_line_algo
from base_load_algo import base_load_algo

simu_params = util.load_dict('simu_params.txt')
"""
simu_params = {
'env_path':'env/large.txt',

'save_path':'result/large.txt',

'base_load_path':'base_load/10_min/',

'slot_len':10,

'start_hr':0,

'end_hr':24,

'mode':'change',

'algo':{

'central':{'type':'central_algo', 'params':{'theta':0.8}},

'decentral':{'type':'decentral_algo', 'params':{'x':True, 'theta':0.8, 'step_factor':20, 'tol':0.05, 'max_iter':200}},

'llf':{'type':'base_line_algo', 'params':{'value':'llf'}},

'edf':{'type':'base_line_algo', 'params':{'value':'edf'}},

'base_load':{'type':'base_load_algo', 'params':{}}
}
}
"""
env = util.load_dict(simu_params['env_path'])

DSSObj = DSSStartup.dssstartup('master33Full.dss')

# Initial P and Q
bl_scale = 1.3
PQ_dict = util.load_dict(simu_params['base_load_path']+'h'+str(simu_params['start_hr'])+'.txt')
P = bl_scale*np.array(PQ_dict['P'])
Q = bl_scale*np.array(PQ_dict['Q'])

algo_list = {}
decentral_list = []
for key in simu_params['algo']:
    if simu_params['algo'][key]['type']=='decentral_algo':
        decentral_list.append(key)

    if key=='Central':
         obj = central_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])

    elif key=='GPA':
         obj = gpa_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])
         
    elif key=='SGPA':
         obj = diag_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])
         
    elif key=='admm':
         obj = admm_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])

    elif key=='Base Load':
         obj = base_load_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'])

    elif key=='LLF' or key=='EDF':
         obj = base_line_algo(DSSObj, env, P, Q, start_hr=simu_params['start_hr'], slot_len_in_min=simu_params['slot_len'], mode=simu_params['mode'], params=simu_params['algo'][key]['params'])

    algo_list[key] = obj

result = {}
decentral_flag = False
for key in algo_list:
    result[key] = {}
    if key in decentral_list:
        decentral_flag= True
#result['decentral'] = {}

n_slots = int(60 / simu_params['slot_len'])

for h in tqdm(range(simu_params['start_hr'], simu_params['end_hr'])):
    PQ_dict = util.load_dict(simu_params['base_load_path']+'h'+str(h)+'.txt')
    P = bl_scale*np.array(PQ_dict['P'])
    Q = bl_scale*np.array(PQ_dict['Q'])

    for t in range(0, n_slots):
        for key in algo_list:
            if key in decentral_list:
               continue

            index = h*n_slots + t
            result[key][index] = algo_list[key].update(P,Q)

            if key == 'Central' and decentral_flag==True:
                for dli in decentral_list:
                    result[dli][index] = algo_list[dli].update(P,Q, result['Central'][index])

"""
'decentral':{'type':'decentral_algo', 'params':{'x':True, 'theta':0.8, 'step_factor':200, 'tol':0.05, 'max_iter':200}},
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
