"""Run all tests.

"""
import os
import sys
import unittest

os.system('source ../env/bin/activate')
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'test'))

loader = unittest.TestLoader()
suite = loader.discover('test')
unittest.TextTestRunner().run(suite)
