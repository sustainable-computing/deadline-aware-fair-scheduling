import numpy as np


def runPF(dssObj, p, q, evNode, evP):
    evExtraP = np.zeros(len(p))
    for e in range(0, len(evP)):
        evExtraP[evNode[e]] = evP[e]
    p = [sum(x) for x in zip(p, evExtraP)]
    dssCircuit = dssObj.ActiveCircuit
    dssText = dssObj.Text
    nNodes = 33

    for ind in range(2, nNodes +1, 1):
        for secInd in range(56 ,111):
            loadIdx = (ind - 2) * 55 + secInd - 55 - 1
            nodeNumber = ind * 1000 + secInd
            loadchangecommand = 'Edit Load.' + str(nodeNumber) + ' kW= ' + str(p[loadIdx]) + ' kvar= ' + str(q[loadIdx])
            dssText.Command = loadchangecommand

    dssText.Command = 'Set mode=snapshot'
    dssText.Command = 'solve'
    # DSSText.Command = 'show voltage'

    # getting bus voltages
    return dssCircuit



