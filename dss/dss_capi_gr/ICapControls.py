'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Iterable

class ICapControls(Iterable):
    __slots__ = []

    def Reset(self):
        self._lib.CapControls_Reset()

    @property
    def CTratio(self):
        '''Transducer ratio from pirmary current to control current.'''
        return self._lib.CapControls_Get_CTratio()

    @CTratio.setter
    def CTratio(self, Value):
        self._lib.CapControls_Set_CTratio(Value)
        self.CheckForError()

    @property
    def Capacitor(self):
        '''Name of the Capacitor that is controlled.'''
        return self._get_string(self._lib.CapControls_Get_Capacitor())

    @Capacitor.setter
    def Capacitor(self, Value):
        if type(Value) is not bytes:
            Value = Value.encode(self._api_util.codec)

        self._lib.CapControls_Set_Capacitor(Value)
        self.CheckForError()

    @property
    def DeadTime(self):
        return self._lib.CapControls_Get_DeadTime()

    @DeadTime.setter
    def DeadTime(self, Value):
        self._lib.CapControls_Set_DeadTime(Value)
        self.CheckForError()

    @property
    def Delay(self):
        '''Time delay [s] to switch on after arming.  Control may reset before actually switching.'''
        return self._lib.CapControls_Get_Delay()

    @Delay.setter
    def Delay(self, Value):
        self._lib.CapControls_Set_Delay(Value)
        self.CheckForError()

    @property
    def DelayOff(self):
        '''Time delay [s] before swithcing off a step. Control may reset before actually switching.'''
        return self._lib.CapControls_Get_DelayOff()

    @DelayOff.setter
    def DelayOff(self, Value):
        self._lib.CapControls_Set_DelayOff(Value)
        self.CheckForError()

    @property
    def Mode(self):
        '''Type of automatic controller.'''
        return self._lib.CapControls_Get_Mode()

    @Mode.setter
    def Mode(self, Value):
        self._lib.CapControls_Set_Mode(Value)
        self.CheckForError()

    @property
    def MonitoredObj(self):
        '''Full name of the element that PT and CT are connected to.'''
        return self._get_string(self._lib.CapControls_Get_MonitoredObj())

    @MonitoredObj.setter
    def MonitoredObj(self, Value):
        if type(Value) is not bytes:
            Value = Value.encode(self._api_util.codec)

        self._lib.CapControls_Set_MonitoredObj(Value)
        self.CheckForError()

    @property
    def MonitoredTerm(self):
        '''Terminal number on the element that PT and CT are connected to.'''
        return self._lib.CapControls_Get_MonitoredTerm()

    @MonitoredTerm.setter
    def MonitoredTerm(self, Value):
        self._lib.CapControls_Set_MonitoredTerm(Value)
        self.CheckForError()

    @property
    def OFFSetting(self):
        '''Threshold to switch off a step. See Mode for units.'''
        return self._lib.CapControls_Get_OFFSetting()

    @OFFSetting.setter
    def OFFSetting(self, Value):
        self._lib.CapControls_Set_OFFSetting(Value)
        self.CheckForError()

    @property
    def ONSetting(self):
        '''Threshold to arm or switch on a step.  See Mode for units.'''
        return self._lib.CapControls_Get_ONSetting()

    @ONSetting.setter
    def ONSetting(self, Value):
        self._lib.CapControls_Set_ONSetting(Value)
        self.CheckForError()

    @property
    def PTratio(self):
        '''Transducer ratio from primary feeder to control voltage.'''
        return self._lib.CapControls_Get_PTratio()

    @PTratio.setter
    def PTratio(self, Value):
        self._lib.CapControls_Set_PTratio(Value)
        self.CheckForError()

    @property
    def UseVoltOverride(self):
        '''Enables Vmin and Vmax to override the control Mode'''
        return self._lib.CapControls_Get_UseVoltOverride() != 0

    @UseVoltOverride.setter
    def UseVoltOverride(self, Value):
        self._lib.CapControls_Set_UseVoltOverride(Value)
        self.CheckForError()

    @property
    def Vmax(self):
        '''With VoltOverride, swtich off whenever PT voltage exceeds this level.'''
        return self._lib.CapControls_Get_Vmax()

    @Vmax.setter
    def Vmax(self, Value):
        self._lib.CapControls_Set_Vmax(Value)
        self.CheckForError()

    @property
    def Vmin(self):
        '''With VoltOverride, switch ON whenever PT voltage drops below this level.'''
        return self._lib.CapControls_Get_Vmin()

    @Vmin.setter
    def Vmin(self, Value):
        self._lib.CapControls_Set_Vmin(Value)
        self.CheckForError()
