import unittest

from aufbau.graph import Graph, GraphError
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

    def test_create_dag(self):
        callable = lambda: False

        # Arrange
        graph = Graph()
        graph.register_target(callable, 'one')
        graph.register_target(callable, 'two')
        graph.register_target(callable, 'three')
        graph.register_target(callable, 'four')
        graph.register_dependency('two', 'one')
        graph.register_dependency('three', 'one')
        graph.register_dependency('four', 'two')
        graph.register_dependency('four', 'three')

        # Act
        graph.build()

        # Assert
        one = graph._dag['one']
        two = graph._dag['two']
        three = graph._dag['three']
        four = graph._dag['four']
        self.assertListEqual([], one.deps)
        self.assertListEqual([one], two.deps)
        self.assertListEqual([one], three.deps)
        self.assertSetEqual({two, three}, set(four.deps))

    def test_circular_references(self):
        callable = lambda: False

        # Arrange
        graph = Graph()
        graph.register_target(callable, 'one')
        graph.register_target(callable, 'two')
        graph.register_target(callable, 'three')
        graph.register_target(callable, 'four')
        graph.register_dependency('two', 'one')
        graph.register_dependency('three', 'one')
        graph.register_dependency('four', 'two')
        graph.register_dependency('four', 'three')
        graph.register_dependency('two', 'four')

        # Assert
        self.assertRaises(GraphError, lambda: graph.build())
