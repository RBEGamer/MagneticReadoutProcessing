"""This class only includes static methods which are able to used in a user defined pipeline"""

import os
import re
from pathlib import Path

from import_MRP import __fix_import__
__fix_import__()


from MRP import MRPReading
from MRP import MRPSimulation
from MRP import MRPAnalysis
from MRP import MRPDataVisualization
import  UDPPFLogger
from UDPPFLogger import UDPFLogger as logger


class UDPPFunctionCollectionException(Exception):
    def __init__(self, message="UDPFFunctionCollectionException thrown"):
        self.message = message
        super().__init__(self.message)


class UDPPFunctionCollection:
    """This class only includes static methods which are able to used in a user defined pipeline"""


    @staticmethod
    def simulate_magnet(IP_count: int = 1, IP_random_polarisation: bool = False, IP_random_magnetisation: bool = False) -> [MRPReading.MRPReading]:
        ret: [MRPReading.MRPReading] = []

        for idx in range(IP_count):
            rnd = MRPSimulation.MRPSimulation.generate_reading(_randomize_magnetization=IP_random_polarisation, _add_random_polarisation=IP_random_magnetisation)
            rnd.set_additional_data("simulate_magnet", idx)
            ret.append(rnd)

        return ret

    @staticmethod
    def readings_passthrough(readings: [MRPReading.MRPReading]) -> [MRPReading.MRPReading]:
        """
        returns the input readings without any modification.
        implemented and used during development

        :param readings: input readings
        :type readings: [MRPReading.MRPReading]

        :returns: returns same readings as given in the readings input parameter
        :rtype: [MRPReading.MRPReading]
        """
        if readings is None or len(readings) <= 0:
            raise UDPPFunctionCollectionException("readings_passthrough: readings parameter empty")

        return readings

    @staticmethod
    def inspect_readings(readings_to_inspect: [MRPReading.MRPReading], IP_export_folder: str = "", IP_log_to_std: bool = True):
        """
        prints some information about a set of readings

        :param readings: readings to inspect
        :type readings: [MRPReading.MRPReading]

        :param IP_export_folder: if populated export report to folder
        :type IP_export_folder: str
        """
        if readings_to_inspect is None or len(readings_to_inspect) <= 0:
            raise UDPPFunctionCollectionException("inspect_readings: readings parameter empty")

        log: logger = UDPPFLogger.UDPFLogger()

        if len(IP_export_folder) > 0:
            if not str(IP_export_folder).startswith('/'):
                IP_export_folder = str(Path(IP_export_folder).resolve())
                # GET LOGGER

            log.run_log("inspect_readings: IP_export_folder parameter set to {}".format(IP_export_folder))

        for r in readings_to_inspect:
            # REPORT TEMPLATE
            report_text: str = """########## READING REPORT ##########
            NAME: %%NAME%%
            No Datapoints: %%NODP%%
            B [mT]: %%BV%%
            Temperature [°C]: %%TEMP%%
            CenterOfGravity [x y z] normalized: %%COG%%
            ######## END READING REPORT ########"""
            # REPLACE TEMPLATE WITH REPORT DATA
            report_text = report_text.replace("%%NAME%%", "{}".format(r.get_name()))
            report_text = report_text.replace("%%NODP%%", "{}".format(len(r.data)))



            report_text = report_text.replace("%%BV%%", "{}".format(MRPAnalysis.MRPAnalysis.calculate_mean(r, _temperature_axis=False)))
            report_text = report_text.replace("%%TEMP%%", "{}".format(MRPAnalysis.MRPAnalysis.calculate_mean(r, _temperature_axis=True)))


            cog = MRPAnalysis.MRPAnalysis.calculate_center_of_gravity(r)
            report_text = report_text.replace("%%COG%%", "[{} {} {}]".format(cog[0], cog[1], cog[2]))

            if IP_log_to_std:
                print(report_text)




            # EXPORT TO FILE
            if len(IP_export_folder) > 0:
                reading_name: str = r.get_name()
                reading_name = reading_name.replace("/", "").replace(".", "") + ".report.txt"
                reading_abs_filepath: str = str(Path(IP_export_folder).joinpath(Path(reading_name)))
                log.run_log("inspect_readings: report exported to {}".format(reading_abs_filepath))
                # CREATE FOLDER
                if not os.path.exists(IP_export_folder):
                    os.makedirs(IP_export_folder)
                # WRITE REPORT TEXT TO FILE
                with open(reading_abs_filepath, 'w') as f:
                    f.write(report_text)

    @staticmethod
    def plot_readings(readings_to_plot: [MRPReading.MRPReading], IP_plot_headline_prefix: str = "Plot", IP_export_folder: str = ""):
        """
        plots some information about a set of readings including mean, std_deviation and more

        :param readings_to_plot: readings to plot
        :type readings_to_plot: [MRPReading.MRPReading]

        :param IP_export_folder: if populated export report to folder
        :type IP_export_folder: str
        """
        if readings_to_plot is None or len(readings_to_plot) <= 0:
            raise UDPPFunctionCollectionException("readings_to_plot: readings parameter empty")

        log: logger = UDPPFLogger.UDPFLogger()

        exp_path = None
        if len(IP_export_folder) > 0:
            if not str(IP_export_folder).startswith('/'):
                IP_export_folder = str(Path(IP_export_folder).resolve())


                exp_path = IP_export_folder

                if not os.path.exists(exp_path):
                    os.makedirs(exp_path)
                # GET LOGGER
            log.run_log("readings_to_plot: IP_export_folder parameter set to {}".format(IP_export_folder))

        MRPDataVisualization.MRPDataVisualization.plot_error(readings_to_plot, IP_plot_headline_prefix , str(Path(exp_path).joinpath("error_plot_{}.png".format(str(IP_plot_headline_prefix).replace(" ", "").replace("/", "").replace(".", "")))))
        MRPDataVisualization.MRPDataVisualization.plot_scatter(readings_to_plot, IP_plot_headline_prefix,str(Path(exp_path).joinpath("scatter_plot_{}.png".format(str(IP_plot_headline_prefix).replace(" ", "").replace("/", "").replace(".", "")))))
        MRPDataVisualization.MRPDataVisualization.plot_temperature(readings_to_plot, IP_plot_headline_prefix,str(Path(exp_path).joinpath("temperature_plot_{}.png".format(str(IP_plot_headline_prefix).replace(" ","").replace("/","").replace(".", "")))))

    @staticmethod
    def concat_readings(set_a: [MRPReading.MRPReading], set_b: [MRPReading.MRPReading], IP_random_shuffle: bool = False) -> [MRPReading.MRPReading]:
        """
        Concat two readings array into one.
        Can be used for combining readings from two folders using the import_readings function

        :param set_a: first array of readings
        :type set_a: [MRPReading.MRPReading]

        :param set_b: second array of readings
        :type set_b: [MRPReading.MRPReading]

        :returns: both readings arrays combined
        :rtype: [MRPReading.MRPReading]
        """

        rd: [MRPReading.MRPReading] = []

        for a in set_a:
            rd.append(a)

        for b in set_b:
            rd.append(b)

        return rd

    @staticmethod
    def import_readings(IP_input_folder:str = "./", IP_file_regex: str = "(.)*.mag.json", IP_parse_idx_in_filename: bool = True) -> [MRPReading.MRPReading]:
        """
        Imports all readings found in the folder given from the input_folder.
        It restores all meta-data and datapoints.

        :param IP_input_folder: Folder with .mag.json readings ABS or REL-Paths are allowed
        :type IP_input_folder: str

        :param IP_file_regex: to only allow certain filenames using a regex string
        :type IP_file_regex: str

        :param IP_parse_idx_in_filename: parses string cIDX<YXZ> in filename and set <XYZ> as measurement id, this is used if manual set id from filename should be used
        :type IP_parse_idx_in_filename: bool

        :returns: Returns the imported readings as [MRPReading.MRPReading] instances
        :rtype: [MRPReading.MRPReading]
        """

        if IP_input_folder is None or len(IP_input_folder) <= 0:
            raise UDPPFunctionCollectionException("import_readings: input_folder parameter empty")
        # CHECK FOLDER EXISTS
        input_folder: str = IP_input_folder

        if not str(IP_input_folder).startswith('/'):
            input_folder = str(Path(IP_input_folder).resolve())
        # GET LOGGER
        log: logger = UDPPFLogger.UDPFLogger()
        log.run_log("import_readings: input_folder parameter set to {}".format(input_folder))

        # CHECK FOLDER EXISTS
        if not os.path.exists(input_folder):
            raise UDPPFunctionCollectionException("import_readings: input_folder parameter does not exist on the system".format(input_folder))



        # IMPORT READINGS
        readings_to_import: [str] = [f for f in os.listdir(input_folder) if re.match(r'{}'.format(IP_file_regex), f)]
        imported_results: [MRPReading.MRPReading] = []
        for rti in readings_to_import:
            log.run_log("import_readings: import reading {}".format(rti))
            reading: MRPReading.MRPReading = MRPReading.MRPReading()

            reading_abs_filepath: str = str(Path(input_folder).joinpath(Path(rti)))
            reading.load_from_file(reading_abs_filepath)


            if IP_parse_idx_in_filename:
                f: [str] = rti.split("cIDX")
                cIDX: str = ""
                if len(f) > 1:
                    for c in f[1]:
                        if c.isdigit():
                            cIDX = cIDX + str(c)

                if len(cIDX) > 0:
                    reading.measurement_config.id = cIDX
                    reading.set_additional_data("cIDX", cIDX)
                    reading.set_additional_data("IP_parse_idx_in_filename", "1")
                    reading.set_name("{}_cIDX{}".format(reading.get_name(), cIDX))

            imported_results.append(reading)

        return imported_results

    @staticmethod
    def apply_sensor_bias_offset(bias_readings: [MRPReading.MRPReading], readings_to_calibrate: [MRPReading.MRPReading]) -> [MRPReading.MRPReading]:
        if bias_readings is None or len(bias_readings) <= 0:
            raise UDPPFunctionCollectionException("apply_sensor_bias_offset: bias_readings parameter empty")

        if readings_to_calibrate is None or len(readings_to_calibrate) <= 0:
            raise UDPPFunctionCollectionException("apply_sensor_bias_offset: readings_to_calibrate parameter empty")

        # CALCULATE AVERAGE OF GIVEN BIAS READINGS
        mean_value: float = 0.0
        for br in bias_readings:
            v =MRPAnalysis.MRPAnalysis.calculate_mean(br)
            mean_value = mean_value + v
        mean_value = mean_value / len(bias_readings)
        print("apply_sensor_bias_offset calculated sensor bias".format(mean_value))

        # DEEP COPY READINGS
        new_readings: [MRPReading.MRPReading] = []

        for r in readings_to_calibrate:
            obj: dict = r.dump_to_dict()
            r: MRPReading.MRPReading = MRPReading.MRPReading()
            r.load_from_dict(obj)
            new_readings.append(r)

        # APPLY BIAS OFFSET
        MRPAnalysis.MRPAnalysis.apply_global_offset_inplace(new_readings, mean_value)



        return new_readings


