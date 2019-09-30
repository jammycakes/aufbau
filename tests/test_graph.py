import unittest

from tests import aufbau_sample

class TestSample(unittest.TestCase):

    def setUp(self):
        self.graph = aufbau_sample.graph

    def test_set_targets(self):
        expected = {
            'clean': aufbau_sample.clean,
            'build': aufbau_sample.build,
            'test': aufbau_sample.test
        }
        self.assertDictEqual(expected, self.graph._targets)

    def test_set_deps(self):
        expected = {
            'build': ['clean'],
            'test': ['build']
        }
        self.assertDictEqual(expected, self.graph._deps)
