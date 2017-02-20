import unittest
import numpy as np
import ctypes

import pydaqmx

from .test_task import _test_for_test_device, test_device_name

class TestBuffer(unittest.TestCase):
    def test_device_list(self):
        """ Test that one can get the buffer size by sending None as data"""
        n = pydaqmx.get_sys_dev_names(None, 0)
        data = ctypes.create_string_buffer(n)
        pydaqmx.get_sys_dev_names(data, n)


class TestArray(unittest.TestCase):
    def setUp(self):    
        _test_for_test_device()
    def test_read_array(self):
        task = pydaqmx.Task()
        data = np.zeros(1000)
        read = pydaqmx.int32()
        task.create_ai_voltage_chan(test_device_name+"/ai0","", pydaqmx.VAL_RSE, -10.0, 10.0, pydaqmx.VAL_VOLTS, None)
        task.cfg_samp_clk_timing("", 100000.0, pydaqmx.VAL_RISING, pydaqmx.VAL_CONT_SAMPS, 1000)
        task.start_task()
        task.read_analog_f64(1000, 10.0, pydaqmx.VAL_GROUP_BY_SCAN_NUMBER, data, 1000, ctypes.byref(read), None)
        task.stop_task()

    def test_write_array(self):
        task = pydaqmx.Task()
        data = np.zeros(1000)
        written = pydaqmx.int32()
        task.create_ao_voltage_chan(test_device_name+"/ao0", "", -10.0, 10.0, pydaqmx.VAL_VOLTS, None)
        task.cfg_samp_clk_timing("", 100000.0, pydaqmx.VAL_RISING, pydaqmx.VAL_CONT_SAMPS, 1000)
        task.write_analog_f64(1000, 0 , 10.0, pydaqmx.VAL_GROUP_BY_SCAN_NUMBER, data, ctypes.byref(written), None)
        task.start_task()
        task.stop_task()

    def test_write_array_bis(self):
        task = pydaqmx.Task()
        data = np.zeros(1000)
        written = pydaqmx.int32()
        task.create_ao_voltage_chan(test_device_name+"/ao0", "", -10.0, 10.0, pydaqmx.VAL_VOLTS, None)
        task.cfg_samp_clk_timing("", 100000.0, pydaqmx.VAL_RISING, pydaqmx.VAL_CONT_SAMPS, 1000)
        task.write_analog_f64(1000, 0 , 10.0, pydaqmx.VAL_GROUP_BY_SCAN_NUMBER, list(data), ctypes.byref(written), None)
        task.start_task()
        task.stop_task()


