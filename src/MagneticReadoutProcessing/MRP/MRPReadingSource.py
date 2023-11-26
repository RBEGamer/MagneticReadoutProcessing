from abc import ABC, abstractmethod
from MRP import MRPHal, MRPReading


class MRPReadingSourceException(Exception):
    def __init__(self, message="MRPReadingSource thrown"):
        self.message = message
        super().__init__(self.message)


class MRPReadingSource(ABC):

    @abstractmethod
    def __init__(self, _hal: MRPHal.MRPHal):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def perform_measurement(self, _measurement_points: int, _average_readings_per_datapoint: int) -> [MRPReading.MRPReading]:
        pass

