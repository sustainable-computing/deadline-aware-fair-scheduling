import DSSStartup
import scipy.io as spio
import env

epsilon = 1.0

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
