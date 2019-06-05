import DSSStartup
import scipy.io as spio
import numpy as np
import env

epsilon = 1.0

def log(x):
    return np.array([-1000.0 if x<=0.0 else np.log(x) for x in x])
    
def reciprocal(x):
    return np.array([1000.0 if x<=0.0 else 1.0/x for x in x])
    
def f(x):
    return np.array([0.0 if x<=-500 else x+500 for x in x])

def load(argv):
    dss_path = 'master33Full.dss'
    mat_path = 'secAggLoads.mat'
    env_path = 'default.npy'
    for i in range(1,len(argv)):
        name = argv[i]
        if '.dss' in name:
            dss_path = name
        elif '.mat' in name:
            mat_path = name
        elif '.npy' in name:
            env_path = name
    return (DSSStartup.dssstartup(dss_path), spio.loadmat(mat_path, squeeze_me=True), env.env(env_path))

