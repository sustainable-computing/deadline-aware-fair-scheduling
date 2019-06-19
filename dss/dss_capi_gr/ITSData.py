'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Iterable

class ITSData(Iterable):
    '''Experimental API extension exposing TSData objects'''

    __slots__ = []

    @property
    def EmergAmps(self):
        '''Emergency ampere rating'''
        return self._lib.TSData_Get_EmergAmps()

    @EmergAmps.setter
    def EmergAmps(self, Value):
        self._lib.TSData_Set_EmergAmps(Value)
        self.CheckForError()

    @property
    def NormAmps(self):
        '''Normal Ampere rating'''
        return self._lib.TSData_Get_NormAmps()

    @NormAmps.setter
    def NormAmps(self, Value):
        self._lib.TSData_Set_NormAmps(Value)
        self.CheckForError()

    @property
    def Rdc(self):
        return self._lib.TSData_Get_Rdc()

    @Rdc.setter
    def Rdc(self, Value):
        self._lib.TSData_Set_Rdc(Value)
        self.CheckForError()

    @property
    def Rac(self):
        return self._lib.TSData_Get_Rac()

    @Rac.setter
    def Rac(self, Value):
        self._lib.TSData_Set_Rac(Value)
        self.CheckForError()

    @property
    def GMRac(self):
        return self._lib.TSData_Get_GMRac()

    @GMRac.setter
    def GMRac(self, Value):
        self._lib.TSData_Set_GMRac(Value)
        self.CheckForError()

    @property
    def GMRUnits(self):
        return self._lib.TSData_Get_GMRUnits()

    @GMRUnits.setter
    def GMRUnits(self, Value):
        self._lib.TSData_Set_GMRUnits(Value)
        self.CheckForError()

    @property
    def Radius(self):
        return self._lib.TSData_Get_Radius()

    @Radius.setter
    def Radius(self, Value):
        self._lib.TSData_Set_Radius(Value)
        self.CheckForError()

    @property
    def RadiusUnits(self):
        return self._lib.TSData_Get_RadiusUnits()

    @RadiusUnits.setter
    def RadiusUnits(self, Value):
        self._lib.TSData_Set_RadiusUnits(Value)
        self.CheckForError()

    @property
    def ResistanceUnits(self):
        return self._lib.TSData_Get_ResistanceUnits()

    @ResistanceUnits.setter
    def ResistanceUnits(self, Value):
        self._lib.TSData_Set_ResistanceUnits(Value)
        self.CheckForError()

    @property
    def Diameter(self):
        return self._lib.TSData_Get_Diameter()

    @Diameter.setter
    def Diameter(self, Value):
        self._lib.TSData_Set_Diameter(Value)
        self.CheckForError()

    @property
    def EpsR(self):
        return self._lib.TSData_Get_EpsR()

    @EpsR.setter
    def EpsR(self, Value):
        self._lib.TSData_Set_EpsR(Value)
        self.CheckForError()

    @property
    def InsLayer(self):
        return self._lib.TSData_Get_InsLayer()

    @InsLayer.setter
    def InsLayer(self, Value):
        self._lib.TSData_Set_InsLayer(Value)
        self.CheckForError()

    @property
    def DiaIns(self):
        return self._lib.TSData_Get_DiaIns()

    @DiaIns.setter
    def DiaIns(self, Value):
        self._lib.TSData_Set_DiaIns(Value)
        self.CheckForError()

    @property
    def DiaCable(self):
        return self._lib.TSData_Get_DiaCable()

    @DiaCable.setter
    def DiaCable(self, Value):
        self._lib.TSData_Set_DiaCable(Value)
        self.CheckForError()

    @property
    def DiaShield(self):
        return self._lib.TSData_Get_DiaShield()

    @DiaShield.setter
    def DiaShield(self, Value):
        self._lib.TSData_Set_DiaShield(Value)
        self.CheckForError()

    @property
    def TapeLayer(self):
        return self._lib.TSData_Get_TapeLayer()

    @TapeLayer.setter
    def TapeLayer(self, Value):
        self._lib.TSData_Set_TapeLayer(Value)
        self.CheckForError()

    @property
    def TapeLap(self):
        return self._lib.TSData_Get_TapeLap()

    @TapeLap.setter
    def TapeLap(self, Value):
        self._lib.TSData_Set_TapeLap(Value)
        self.CheckForError()
