import numpy as np


def getTransCurrent(DSSCircuit):
    transCurrent=[]
    lIndex = DSSCircuit.Lines.First
    eCurrents = DSSCircuit.ActiveCktElement.Currents[0:6]
    transCurrent.append(np.sqrt(np.square(eCurrents[0::2])+np.square(eCurrents[1::2])))

    # get transformers' power transfers
    tIndex = DSSCircuit.Transformers.First
    transCounter = 0
    while tIndex != 0:
        eCurrents = DSSCircuit.ActiveCktElement.Currents[0:6]
        transCurrent.append(np.sqrt(np.square(eCurrents[0::2])+np.square(eCurrents[1::2])))
        transCounter += 1
        tIndex = DSSCircuit.Transformers.Next

    return transCurrent

