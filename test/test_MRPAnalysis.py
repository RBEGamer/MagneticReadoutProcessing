import math

import numpy as np
import pytest
import unittest
import random
from MagneticReadoutProcessing import MRPConfig
from MagneticReadoutProcessing import MRPReading
from MagneticReadoutProcessing import MRPAnalysis
import configparser
import os
class TestMPRAnalysis(unittest.TestCase):

    # PREPARE A INITIAL CONFIGURATION FILE
    # CALLED BEFORE EACH SUB-TESTCASE
    def setUp(self) -> None:
        # USE DEFAULT CONFIG
        self.config = MRPConfig.MRPConfig(None)
        self.config.load_defaults()

        self.reading_A = MRPReading.MRPReading(self.config)
        self.reading_B = MRPReading.MRPReading(self.config)
        self.assertIsNotNone(self.reading_A)
        self.assertIsNotNone(self.reading_B)

        self.reading_A.sensor_id = 0
        self.reading_B.sensor_id = 1

        n_phi = self.config.MEASUREMENT_HORIZONTAL_RESOLUTION
        n_theta = self.config.MEASUREMENT_VERTICAL_RESOLUTION
        # CREATE A POLAR COORDINATE GRID TO ITERATE OVER
        theta, phi = np.mgrid[0.0:0.5 * np.pi:n_theta * 1j, 0.0:2.0 * np.pi:n_phi * 1j]

        ii = 0
        jj = 0
        for j in phi[0, :]:
            ii = ii + 1
            for i in theta[:, 0]:
                jj = jj + 1
                self.reading_A.insert_reading(random.uniform(0, 1)*10.0, j, i, ii, jj, random.uniform(0, 1) * 10.0 + 25.0)
                self.reading_B.insert_reading(random.uniform(0, 1)*10.0, j, i, ii, jj, random.uniform(0, 1) * 10.0 + 25.0)
    # JUST USED FOR PREPERATION


    def test_calibration_analysis_zero(self):
        # IF A CALIBRATION READING IS APPLIED ON THE SAME READING THE RESULT SHOULD BE ZERO
        # reading_A is the calibration reading
        # and will be applied directly onto reading_A
        # so the result should be zero for all entries
        MRPAnalysis.MRPAnalysis.apply_calibration_data_inplace(self.reading_A, self.reading_A)
        self.assertIsNotNone(self.reading_A)

        # CHECK FOR VALUES ZERO
        result = self.reading_A.to_numpy_polar()
        for r in result:
            self.assertEqual(r[2], 0.0)


    def test_calibration_analysis_real(self):
        result_original = self.reading_B.to_numpy_polar()
        MRPAnalysis.MRPAnalysis.apply_calibration_data_inplace(self.reading_A, self.reading_B)
        self.assertIsNotNone(self.reading_B)

        # CHECK FOR VALUES ZERO
        result_A = self.reading_A.to_numpy_polar()
        result_B = self.reading_B.to_numpy_polar()

        # CHECK triangle inequality
        for idx, a in enumerate(result_A):
            b = result_B[idx]
            orig = result_original[idx]

            self.assertAlmostEqual(orig[2], b[2] + a[2])

    def test_merge_analysis(self):
        pass

if __name__ == '__main__':
    unittest.main()