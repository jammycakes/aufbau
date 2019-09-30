class Graph:

    def __init__(self):
        self._targets = dict()
        self._deps = dict()

    def register_target(self, callable, name):
        self._targets[name] = callable

    def register_dependency(self, target, dependency):
        self._deps[target] = self._deps[target] if target in self._deps else []
        self._deps[target].append(dependency)

graph = Graph()