'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Iterable

class IMeters(Iterable):
    __slots__ = []

    def CloseAllDIFiles(self):
        self._lib.Meters_CloseAllDIFiles()
        self.CheckForError()

    def DoReliabilityCalc(self, AssumeRestoration):
        self._lib.Meters_DoReliabilityCalc(AssumeRestoration)
        self.CheckForError()

    def OpenAllDIFiles(self):
        self._lib.Meters_OpenAllDIFiles()
        self.CheckForError()

    def Reset(self):
        self._lib.Meters_Reset()
        self.CheckForError()

    def ResetAll(self):
        self._lib.Meters_ResetAll()
        self.CheckForError()

    def Sample(self):
        self._lib.Meters_Sample()
        self.CheckForError()

    def SampleAll(self):
        self._lib.Meters_SampleAll()
        self.CheckForError()

    def Save(self):
        self._lib.Meters_Save()
        self.CheckForError()

    def SaveAll(self):
        self._lib.Meters_SaveAll()
        self.CheckForError()

    def SetActiveSection(self, SectIdx):
        self._lib.Meters_SetActiveSection(SectIdx)
        self.CheckForError()

    @property
    def AllBranchesInZone(self):
        '''(read-only) Wide string list of all branches in zone of the active energymeter object.'''
        return self._get_string_array(self.CheckForError(self._lib.Meters_Get_AllBranchesInZone))

    @property
    def AllEndElements(self):
        '''(read-only) Array of names of all zone end elements.'''
        return self._get_string_array(self.CheckForError(self._lib.Meters_Get_AllEndElements))

    @property
    def AllocFactors(self):
        '''Array of doubles: set the phase allocation factors for the active meter.'''
        self._lib.Meters_Get_AllocFactors_GR()
        return self._get_float64_gr_array()

    @AllocFactors.setter
    def AllocFactors(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_float64_array(Value)
        self._lib.Meters_Set_AllocFactors(ValuePtr, ValueCount)
        self.CheckForError()

    @property
    def AvgRepairTime(self):
        '''(read-only) Average Repair time in this section of the meter zone'''
        return self.CheckForError(self._lib.Meters_Get_AvgRepairTime())

    @property
    def CalcCurrent(self):
        '''Set the magnitude of the real part of the Calculated Current (normally determined by solution) for the Meter to force some behavior on Load Allocation'''
        self._lib.Meters_Get_CalcCurrent_GR()
        return self._get_float64_gr_array()

    @CalcCurrent.setter
    def CalcCurrent(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_float64_array(Value)
        self._lib.Meters_Set_CalcCurrent(ValuePtr, ValueCount)
        self.CheckForError()

    @property
    def CountBranches(self):
        '''(read-only) Number of branches in Active energymeter zone. (Same as sequencelist size)'''
        return self._lib.Meters_Get_CountBranches()

    @property
    def CountEndElements(self):
        '''(read-only) Number of zone end elements in the active meter zone.'''
        return self._lib.Meters_Get_CountEndElements()

    @property
    def CustInterrupts(self):
        '''(read-only) Total customer interruptions for this Meter zone based on reliability calcs.'''
        return self._lib.Meters_Get_CustInterrupts()

    @property
    def DIFilesAreOpen(self):
        '''(read-only) Global Flag in the DSS to indicate if Demand Interval (DI) files have been properly opened.'''
        return self._lib.Meters_Get_DIFilesAreOpen() != 0

    @property
    def FaultRateXRepairHrs(self):
        '''(read-only) Sum of Fault Rate time Repair Hrs in this section of the meter zone'''
        return self._lib.Meters_Get_FaultRateXRepairHrs()

    @property
    def MeteredElement(self):
        '''Set Name of metered element'''
        return self._get_string(self._lib.Meters_Get_MeteredElement())

    @MeteredElement.setter
    def MeteredElement(self, Value):
        if type(Value) is not bytes:
            Value = Value.encode(self._api_util.codec)

        self._lib.Meters_Set_MeteredElement(Value)
        self.CheckForError()

    @property
    def MeteredTerminal(self):
        '''set Number of Metered Terminal'''
        return self._lib.Meters_Get_MeteredTerminal()

    @MeteredTerminal.setter
    def MeteredTerminal(self, Value):
        self._lib.Meters_Set_MeteredTerminal(Value)
        self.CheckForError()

    @property
    def NumSectionBranches(self):
        '''(read-only) Number of branches (lines) in this section'''
        return self.CheckForError(self._lib.Meters_Get_NumSectionBranches())

    @property
    def NumSectionCustomers(self):
        '''(read-only) Number of Customers in the active section.'''
        return self._lib.Meters_Get_NumSectionCustomers()

    @property
    def NumSections(self):
        '''(read-only) Number of feeder sections in this meter's zone'''
        return self._lib.Meters_Get_NumSections()

    @property
    def OCPDeviceType(self):
        '''(read-only) Type of OCP device. 1=Fuse; 2=Recloser; 3=Relay'''
        return self.CheckForError(self._lib.Meters_Get_OCPDeviceType())

    @property
    def Peakcurrent(self):
        '''Array of doubles to set values of Peak Current property'''
        self._lib.Meters_Get_Peakcurrent_GR()
        return self._get_float64_gr_array()

    @Peakcurrent.setter
    def Peakcurrent(self, Value):
        Value, ValuePtr, ValueCount = self._prepare_float64_array(Value)
        self._lib.Meters_Set_Peakcurrent(ValuePtr, ValueCount)
        self.CheckForError()

    @property
    def RegisterNames(self):
        '''(read-only) Array of strings containing the names of the registers.'''
        return self._get_string_array(self._lib.Meters_Get_RegisterNames)

    @property
    def RegisterValues(self):
        '''(read-only) Array of all the values contained in the Meter registers for the active Meter.'''
        self._lib.Meters_Get_RegisterValues_GR()
        return self._get_float64_gr_array()

    @property
    def SAIDI(self):
        '''(read-only) SAIDI for this meter's zone. Execute DoReliabilityCalc first.'''
        return self._lib.Meters_Get_SAIDI()

    @property
    def SAIFI(self):
        '''(read-only) Returns SAIFI for this meter's Zone. Execute Reliability Calc method first.'''
        return self._lib.Meters_Get_SAIFI()

    @property
    def SAIFIKW(self):
        '''(read-only) SAIFI based on kW rather than number of customers. Get after reliability calcs.'''
        return self._lib.Meters_Get_SAIFIKW()

    @property
    def SectSeqIdx(self):
        '''(read-only) SequenceIndex of the branch at the head of this section'''
        return self._lib.Meters_Get_SectSeqIdx()

    @property
    def SectTotalCust(self):
        '''(read-only) Total Customers downline from this section'''
        return self._lib.Meters_Get_SectTotalCust()

    @property
    def SeqListSize(self):
        '''(read-only) Size of Sequence List'''
        return self._lib.Meters_Get_SeqListSize()

    @property
    def SequenceIndex(self):
        '''Get/set Index into Meter's SequenceList that contains branch pointers in lexical order. Earlier index guaranteed to be upline from later index. Sets PDelement active.'''
        return self._lib.Meters_Get_SequenceIndex()

    @SequenceIndex.setter
    def SequenceIndex(self, Value):
        self._lib.Meters_Set_SequenceIndex(Value)
        self.CheckForError()

    @property
    def SumBranchFltRates(self):
        '''(read-only) Sum of the branch fault rates in this section of the meter's zone'''
        return self._lib.Meters_Get_SumBranchFltRates()

    @property
    def TotalCustomers(self):
        '''(read-only) Total Number of customers in this zone (downline from the EnergyMeter)'''
        return self._lib.Meters_Get_TotalCustomers()

    @property
    def Totals(self):
        '''(read-only) Totals of all registers of all meters'''
        self._lib.Meters_Get_Totals_GR()
        return self._get_float64_gr_array()
