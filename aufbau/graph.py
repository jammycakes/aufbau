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



class Node:
    """
    Represents a target, together with its dependencies.
    """
    def __init__(self, name, action, deps):
        self.name = name
        self.action = action
        self.deps = deps


graph = Graph()