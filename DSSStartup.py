#import win32com.client
import dss


def dssstartup(path):
    # 2. Define the com engine.
    #engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
    engine = dss.DSS
    # 3. Start the engine.
    #engine.Start("0")
    engine.Start(0)
    # 4. Command can be given via text as shown below
    engine.Text.Command = 'clear'
    # 5. Prepare the circuit
    circuit = engine.ActiveCircuit
    # 6. Then we can compile a DSS file
    engine.Text.Command = 'compile ' + path
    return engine
