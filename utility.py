import numpy as np
import scipy.io as spio
import DSSStartup

eps = 1e-5
inf = 1e8

def log(x):
    return np.array([-inf if e<=0.0 else np.log(e) for e in x])
    
def reciprocal(x):
    return np.array([inf if e<=0.0 else 1.0/e for e in x])
    
def f(x):
    shift = 500
    return np.array([0.0 if e<=-shift else e+shift for e in x])
    
def save_dict(file_name, dict_):
    f = open(file_name, 'w')
    f.write(str(dict_))
    f.close()
    
def load_dict(file_name):
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    return eval(data)

def load(argv):
    dss_path = 'master33Full.dss'
    mat_path = 'PQ1DayF20.mat'
    env_path = 'env/default_env.txt'
    for i in range(1,len(argv)):
        name = argv[i]
        if '.dss' in name:
            dss_path = name
        elif '.mat' in name:
            mat_path = name
        elif '.txt' in name:
            env_path = name
    return (DSSStartup.dssstartup(dss_path), spio.loadmat(mat_path, squeeze_me=True), load_dict(env_path))


