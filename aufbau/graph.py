import os

class GraphError(Exception):
    pass

class Graph:
    """
    A dependency graph of the targets in the build script.
    """

    def __init__(self):
        self._targets = dict()
        self._deps = dict()
        self._dag = dict()

    def register_target(self, callable, name):
        self._targets[name] = callable

    def register_dependency(self, target, dependency):
        self._deps[target] = self._deps[target] if target in self._deps else set()
        self._deps[target].add(dependency)

    def find_unknown_dependencies(self):
        return [
            (target, dep)
            for target in self._targets
            for dep in self._deps.get(target, [])
            if dep not in self._targets
        ]

    def build(self):
        unknowns = self.find_unknown_dependencies()
        if unknowns:
            raise GraphError(
                os.linesep.join([
                    'Dependency {0} of target {1} was not found.'.format(*unknown)
                    for unknown in unknowns
                ])
            )

        unsorted = set(self._targets)
        while unsorted:
            success = False
            for name in unsorted.copy():
                dep_names = self._deps.get(name, set())
                deps = [self._dag[dep] for dep in dep_names if dep in self._dag]
                if len(deps) == len(dep_names):
                    action = self._targets[name]
                    node = Node(name, action, deps)
                    self._dag[name] = node
                    unsorted.remove(name)
                    success = True
            if not success:
                raise GraphError('Cyclic dependencies were found in the list of tasks.')

    def walk(self, target):
        first_node = self._dag.get(target, False)
        if not first_node:
            raise GraphError('The specified target {0} has not been defined.'.format(target))

        # Now do a topological sort of the selected node and all its dependencies

        visited = set()
        stack = []

        def topological_sort(node):
            visited.add(node)
            for dep in node.deps:
                if not dep in visited:
                    topological_sort(dep)
            stack.insert(0, node)

        topological_sort(first_node)
        return stack

class Node:
    """
    Represents a target, together with its dependencies.
    """
    def __init__(self, name, action, deps):
        self.name = name
        self.action = action
        self.deps = deps


graph = Graph()