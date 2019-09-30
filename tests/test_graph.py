import unittest

from aufbau.graph import Graph
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
            'build': {'clean'},
            'test': {'build'}
        }
        self.assertDictEqual(expected, self.graph._deps)


class TestGraph(unittest.TestCase):

    def test_unknown_dependencies(self):

        callable = lambda: False

        # Arrange
        graph = Graph()
        graph.register_target(callable, 'one')
        graph.register_target(callable, 'two')
        graph.register_dependency('one', 'nonexistent')
        graph.register_dependency('two', 'one')

        # Act
        unknowns = graph.find_unknown_dependencies()

        # Assert
        self.assertListEqual(unknowns, [
            ('one', 'nonexistent')
        ])