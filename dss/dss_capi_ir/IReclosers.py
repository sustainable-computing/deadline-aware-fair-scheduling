'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Iterable

class IReclosers(Iterable):
    __slots__ = []

    def Close(self):
        self._lib.Reclosers_Close()

    def Open(self):
        self._lib.Reclosers_Open()

    @property
    def GroundInst(self):
        '''
        (read) Ground (3I0) instantaneous trip setting - curve multipler or actual amps.
        (write) Ground (3I0) trip instantaneous multiplier or actual amps
        '''
        return self._lib.Reclosers_Get_GroundInst()

    @GroundInst.setter
    def GroundInst(self, Value):
        self._lib.Reclosers_Set_GroundInst(Value)
        self.CheckForError()

    @property
    def GroundTrip(self):
        '''Ground (3I0) trip multiplier or actual amps'''
        return self._lib.Reclosers_Get_GroundTrip()

    @GroundTrip.setter
    def GroundTrip(self, Value):
        self._lib.Reclosers_Set_GroundTrip(Value)
        self.CheckForError()

    @property
    def MonitoredObj(self):
        '''
        (read) Full name of object this Recloser is monitoring.
        (write) Set monitored object by full name.
        '''
        return self._get_string(self._lib.Reclosers_Get_MonitoredObj())

    @MonitoredObj.setter
    def MonitoredObj(self, Value):
        if type(Value) is not bytes:
            Value = Value.encode(self._api_util.codec)

        self._lib.Reclosers_Set_MonitoredObj(Value)
        self.CheckForError()

    @property
    def MonitoredTerm(self):
        '''Terminal number of Monitored object for the Recloser '''
        return self._lib.Reclosers_Get_MonitoredTerm()

    @MonitoredTerm.setter
    def MonitoredTerm(self, Value):
        self._lib.Reclosers_Set_MonitoredTerm(Value)
        self.CheckForError()

    @property
    def NumFast(self):
        '''Number of fast shots'''
        return self._lib.Reclosers_Get_NumFast()

    @NumFast.setter
    def NumFast(self, Value):
        self._lib.Reclosers_Set_NumFast(Value)
        self.CheckForError()

    @property
    def PhaseInst(self):
        '''Phase instantaneous curve multipler or actual amps'''
        return self._lib.Reclosers_Get_PhaseInst()

    @PhaseInst.setter
    def PhaseInst(self, Value):
        self._lib.Reclosers_Set_PhaseInst(Value)
        self.CheckForError()

    @property
    def PhaseTrip(self):
        '''
        (read) Phase trip curve multiplier or actual amps
        (write) Phase Trip multiplier or actual amps
        '''
        return self._lib.Reclosers_Get_PhaseTrip()

    @PhaseTrip.setter
    def PhaseTrip(self, Value):
        self._lib.Reclosers_Set_PhaseTrip(Value)
        self.CheckForError()

    @property
    def RecloseIntervals(self):
        '''(read-only) Variant Array of Doubles: reclose intervals, s, between shots.'''
        return self._get_float64_array(self._lib.Reclosers_Get_RecloseIntervals)

    @property
    def Shots(self):
        '''Number of shots to lockout (fast + delayed)'''
        return self._lib.Reclosers_Get_Shots()

    @Shots.setter
    def Shots(self, Value):
        self._lib.Reclosers_Set_Shots(Value)
        self.CheckForError()

    @property
    def SwitchedObj(self):
        '''Full name of the circuit element that is being switched by the Recloser.'''
        return self._get_string(self._lib.Reclosers_Get_SwitchedObj())

    @SwitchedObj.setter
    def SwitchedObj(self, Value):
        if type(Value) is not bytes:
            Value = Value.encode(self._api_util.codec)

        self._lib.Reclosers_Set_SwitchedObj(Value)
        self.CheckForError()

    @property
    def SwitchedTerm(self):
        '''Terminal number of the controlled device being switched by the Recloser'''
        return self._lib.Reclosers_Get_SwitchedTerm()

    @SwitchedTerm.setter
    def SwitchedTerm(self, Value):
        self._lib.Reclosers_Set_SwitchedTerm(Value)
        self.CheckForError()

