'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Iterable

class ILineGeometries(Iterable):
    '''Experimental API extension exposing part of the LineGeometry objects'''

    __slots__ = []
    
    @property
    def Conductors(self):
        '''(read-only) Array of strings with names of all conductors in the active LineGeometry object'''
        return self._get_string_array(self._lib.LineGeometries_Get_Conductors)

    @property
    def EmergAmps(self):
        '''Emergency ampere rating'''
        return self._lib.LineGeometries_Get_EmergAmps()

    @EmergAmps.setter
    def EmergAmps(self, Value):
        self._lib.LineGeometries_Set_EmergAmps(Value)
        self.CheckForError()

    @property
    def NormAmps(self):
        '''Normal Ampere rating'''
        return self._lib.LineGeometries_Get_NormAmps()

    @NormAmps.setter
    def NormAmps(self, Value):
        self._lib.LineGeometries_Set_NormAmps(Value)
        self.CheckForError()

    @property
    def RhoEarth(self):
        return self._lib.LineGeometries_Get_RhoEarth()

    @RhoEarth.setter
    def RhoEarth(self, Value):
        self._lib.LineGeometries_Set_RhoEarth(Value)
        self.CheckForError()

    @property
    def Reduce(self):
        return self._lib.LineGeometries_Get_Reduce() != 0

    @Reduce.setter
    def Reduce(self, Value):
        self._lib.LineGeometries_Set_Reduce(Value)
        self.CheckForError()

    @property
    def Phases(self):
        '''Number of Phases'''
        return self._lib.LineGeometries_Get_Phases()

    @Phases.setter
    def Phases(self, Value):
        self._lib.LineGeometries_Set_Phases(Value)
        self.CheckForError()

    def Rmatrix(self, Frequency, Length, Units):
        '''(read-only) Resistance matrix, ohms'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Rmatrix, Frequency, Length, Units)

    def Xmatrix(self, Frequency, Length, Units):
        '''(read-only) Reactance matrix, ohms'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Xmatrix, Frequency, Length, Units)

    def Zmatrix(self, Frequency, Length, Units):
        '''(read-only) Complex impedance matrix, ohms'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Zmatrix, Frequency, Length, Units)

    def Cmatrix(self, Frequency, Length, Units):
        '''(read-only) Capacitance matrix, nF'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Cmatrix, Frequency, Length, Units)

    @property
    def Units(self):
        return self._get_int32_array(self._lib.LineGeometries_Get_Units)

    @Units.setter
    def Units(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_int32_array(Value)
        self._lib.LineGeometries_Set_Units(ValuePtr, ValueCount)
        self.CheckForError()

    @property
    def Xcoords(self):
        '''Get/Set the X (horizontal) coordinates of the conductors'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Xcoords)

    @Xcoords.setter
    def Xcoords(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_float64_array(Value)
        self._lib.LineGeometries_Set_Xcoords(ValuePtr, ValueCount)
        self.CheckForError()

    @property
    def Ycoords(self):
        '''Get/Set the Y (vertical/height) coordinates of the conductors'''
        return self._get_float64_array(self._lib.LineGeometries_Get_Ycoords)

    @Ycoords.setter
    def Ycoords(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_float64_array(Value)
        self._lib.LineGeometries_Set_Ycoords(ValuePtr, ValueCount)
        self.CheckForError()

