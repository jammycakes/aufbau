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
            'build': ['clean'],
            'test': ['build']
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

class TestWalk(unittest.TestCase):

    def setUp(self):
        callable = lambda: False

        # Arrange
        graph = Graph()
        graph.register_target(callable, 'zero')
        graph.register_target(callable, 'one')
        graph.register_target(callable, 'two')
        graph.register_target(callable, 'three')
        graph.register_target(callable, 'four')
        graph.register_target(callable, 'five')
        graph.register_target(callable, 'six')
        graph.register_dependency('zero', 'one')
        graph.register_dependency('zero', 'three')
        graph.register_dependency('one', 'two')
        graph.register_dependency('one', 'three')
        graph.register_dependency('two', 'three')
        graph.register_dependency('two', 'four')
        graph.register_dependency('two', 'five')
        graph.register_dependency('three', 'four')
        graph.register_dependency('three', 'five')
        graph.register_dependency('four', 'five')
        graph.register_dependency('two', 'six')
        graph.build()
        self.graph = graph

    def _getNodeNames(self, *initialNodeNames):
        return [node.name for node in self.graph.walk(*initialNodeNames)]

    def testBaseDependency(self):
        nodes = self._getNodeNames('six')
        self.assertListEqual(['six'], nodes)

    def testOtherBaseDependency(self):
        nodes = self._getNodeNames('five')
        self.assertListEqual(['five'], nodes)

    def testFourDependencies(self):
        nodes = self._getNodeNames('four')
        self.assertListEqual(['five', 'four'], nodes)

    def testThreeDependencies(self):
        nodes = self._getNodeNames('three')
        self.assertListEqual(['five', 'four', 'three'], nodes)

    def testTwoDependencies(self):
        nodes = self._getNodeNames('two')
        # Order should be 2, 3, 4, 5 with 6 somewhere before 2
        six_index = nodes.index('six')
        self.assertLessEqual(six_index, 3)
        nodes.remove('six')
        self.assertListEqual(['five', 'four', 'three', 'two'], nodes)

    def testOneDependencies(self):
        nodes = self._getNodeNames('one')
        # Order should be 1, 2, 3, 4, 5 with 6 somewhere after 2
        six_index = nodes.index('six')
        self.assertLessEqual(six_index, 3)
        nodes.remove('six')
        self.assertListEqual(['five', 'four', 'three', 'two', 'one'], nodes)

    def testZeroDependencies(self):
        nodes = self._getNodeNames('zero')
        # Order should be 0, 1, 2, 3, 4, 5 with 6 somewhere after 2
        six_index = nodes.index('six')
        self.assertLessEqual(six_index, 3)
        nodes.remove('six')
        self.assertListEqual(['five', 'four', 'three', 'two', 'one', 'zero'], nodes)

    def testThreeAndSixDependencies(self):
        nodes = self._getNodeNames('three', 'six')
        # Order should be 3, 4, 5 with 6 anywhere
        six_index = nodes.index('six')
        self.assertGreater(six_index, -1)
        nodes.remove('six')
        self.assertListEqual(['five', 'four', 'three'], nodes)

class TestWalkOrder(unittest.TestCase):
    """
    Tasks should be called in the order in which they are invoked.
    Their dependencies should be called in the order in which they were registered.
    """

    def register_targets(self):
        callable = lambda: False
        graph = Graph()
        graph.register_target(callable, 'six')
        graph.register_target(callable, 'five')
        graph.register_target(callable, 'four')
        graph.register_target(callable, 'three')
        graph.register_target(callable, 'two')
        graph.register_target(callable, 'one')
        return graph

    def testOrderOne(self):
        graph = self.register_targets()
        graph.register_dependency('five', 'six')
        graph.register_dependency('three', 'four')
        graph.register_dependency('one', 'two')
        graph.register_dependency('one', 'four')
        graph.build()

        node_names = [node.name for node in graph.walk('one', 'three', 'five')]
        self.assertListEqual(['two', 'four', 'one', 'three', 'six', 'five'], node_names)

    def testOrderOne(self):
        graph = self.register_targets()
        graph.register_dependency('five', 'six')
        graph.register_dependency('three', 'four')
        graph.register_dependency('one', 'four')
        graph.register_dependency('one', 'two')
        graph.build()

        node_names = [node.name for node in graph.walk('one', 'three', 'five')]
        self.assertListEqual(['four', 'two', 'one', 'three', 'six', 'five'], node_names)
