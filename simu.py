import numpy as np
import utility as util
import sys

from tqdm import tqdm 
from algo import algo
from central_algo import central_algo
from decentral_algo import decentral_algo
from base_algo import base_algo

DSSObj, mat, env = util.load(sys.argv)

result = {}
central_obj = central_algo(DSSObj, mat, env, params={'theta':0.8})
result['central'] = {}

decentral_obj = decentral_algo(DSSObj, mat, env, params={'theta':0.8, 'max_iter':200})
result['decentral'] = {}

llf_obj = base_algo(DSSObj, mat, env, params={'value':'llf'})
result['llf'] = {}

edf_obj = base_algo(DSSObj, mat, env, params={'value':'edf'})
result['edf'] = {}

#base_load_obj = algo(DSSObj, mat, env)
result['base_load'] = {}

for t in tqdm(range(0,1439)):
    result['central'][t] = central_obj.update()
    result['decentral'][t] = decentral_obj.update()
    result['llf'][t] = llf_obj.update()
    result['edf'][t] = edf_obj.update()
    result['base_load'][t] = {'trans_load':central_obj.get_trans_load(np.zeros(env['evNumber'])).tolist()}
    
util.save_dict('result/test.txt', result)
