'''
A compatibility layer for DSS C-API that mimics the official OpenDSS COM interface.

Copyright (c) 2016-2019 Paulo Meira
'''
from __future__ import absolute_import
from .._cffi_api_util import Base

class IParallel(Base):
    '''Parallel machine interface. Available only in OpenDSS v8+'''

    __slots__ = []

    def CreateActor(self):
        self._lib.Parallel_CreateActor()

    def Wait(self):
        self._lib.Parallel_Wait()

    @property
    def ActiveActor(self):
        '''
        (read) Gets the ID of the Active Actor
        (write) Sets the Active Actor
        '''
        return self._lib.Parallel_Get_ActiveActor()

    @ActiveActor.setter
    def ActiveActor(self, Value):
        self._lib.Parallel_Set_ActiveActor(Value)
        self.CheckForError()

    @property
    def ActiveParallel(self):
        '''
        (read) Sets ON/OFF (1/0) Parallel features of the Engine
        (write) Delivers if the Parallel features of the Engine are Active
        '''
        return self._lib.Parallel_Get_ActiveParallel()

    @ActiveParallel.setter
    def ActiveParallel(self, Value):
        self._lib.Parallel_Set_ActiveParallel(Value)
        self.CheckForError()

    @property
    def ActorCPU(self):
        '''
        (read) Gets the CPU of the Active Actor
        (write) Sets the CPU for the Active Actor
        '''
        return self._lib.Parallel_Get_ActorCPU()

    @ActorCPU.setter
    def ActorCPU(self, Value):
        self._lib.Parallel_Set_ActorCPU(Value)
        self.CheckForError()

    @property
    def ActorProgress(self):
        '''(read-only) Gets the progress of all existing actors in pct'''
        return self._get_int32_array(self._lib.Parallel_Get_ActorProgress)

    @property
    def ActorStatus(self):
        '''(read-only) Gets the status of each actor'''
        return self._get_int32_array(self._lib.Parallel_Get_ActorStatus)

    @property
    def ConcatenateReports(self):
        '''
        (read) Reads the values of the ConcatenateReports option (1=enabled, 0=disabled)
        (write) Enable/Disable (1/0) the ConcatenateReports option for extracting monitors data
        '''
        return self._lib.Parallel_Get_ConcatenateReports()

    @ConcatenateReports.setter
    def ConcatenateReports(self, Value):
        self._lib.Parallel_Set_ConcatenateReports(Value)
        self.CheckForError()

    @property
    def NumCPUs(self):
        '''(read-only) Delivers the number of CPUs on the current PC'''
        return self._lib.Parallel_Get_NumCPUs()

    @property
    def NumCores(self):
        '''(read-only) Delivers the number of Cores of the local PC'''
        return self._lib.Parallel_Get_NumCores()

    @property
    def NumOfActors(self):
        '''(read-only) Gets the number of Actors created'''
        return self._lib.Parallel_Get_NumOfActors()


