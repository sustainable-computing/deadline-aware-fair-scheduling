import os
import numpy as np
import scipy.io as spio
import utility as util
from tqdm import tqdm

dirName = 'base_load'

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

resolution = 10 # min

dirName+='/'+str(resolution)+'_min'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

resolution*=60

mat_path = 'PQ1DayF20.mat'
#resolution = 600 #sec

print('Loading .mat file...:')
mat = spio.loadmat(mat_path, squeeze_me=True)

temp = mat['P']
P = []
print('Loading P...:')
for i in tqdm(range(0,86400,resolution)):
    P.append(temp[:, i])
P = np.array(P).T

temp = mat['Q']
Q = []
print('Loading Q...:')
for i in tqdm(range(0,86400,resolution)):
    Q.append(temp[:, i])
Q = np.array(Q).T

resolution/=60
d = 60/resolution

for h in range(0,24):
    dict_ = {}

    s = int(h*d)
    f = int(s+d)


    dict_['P'] = P[:, s:f].tolist()
    dict_['Q'] = Q[:, s:f].tolist()

    save_file = dirName + '/h' + str(h) + '.txt'
    util.save_dict(save_file, dict_)
print('Saved successfully')



