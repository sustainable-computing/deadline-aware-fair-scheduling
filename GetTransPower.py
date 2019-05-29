def getTransPower(DSSCircuit):
    transPowerTransfer=[]
    lIndex = DSSCircuit.Lines.First
    EPowers = DSSCircuit.ActiveCktElement.Powers
    transPowerTransfer.append(EPowers[0:6])

    # get transformers' power transfers
    tIndex = DSSCircuit.Transformers.First
    transCounter = 0
    while tIndex != 0:
        EPowers = DSSCircuit.ActiveCktElement.Powers
        transPowerTransfer.append(EPowers[0:6])
        transCounter += 1
        tIndex = DSSCircuit.Transformers.Next
    return transPowerTransfer

