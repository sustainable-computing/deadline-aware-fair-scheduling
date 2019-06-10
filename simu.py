import numpy as np
import utility as util
import sys
from central_algo import central_algo
from decentral_algo import decentral_algo

DSSObj, mat, env = util.load(sys.argv)
central_obj = central_algo(DSSObj, mat, env)
decentral_obj = decentral_algo(DSSObj, mat, env)
for t in range(0,100):
    _,c = central_obj.update()
    print(c)
    _,d = decentral_obj.update()
    print(d)
