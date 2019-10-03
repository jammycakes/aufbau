import argparse
import os.path

class BuildError(Exception):
    pass

def locate_script(path):
    candidates = [path] if path else ['aufbaufile', 'aufbaufile.py']
    for candidate in candidates:
        fullpath = os.path.abspath(candidate)
        if os.path.isfile(fullpath):
            return fullpath
    return None

def load_script(path):
    if not path:
        raise BuildError('No build script (aufbaufile or aufbaufile.py) was found.')
    import importlib.util

    spec = importlib.util.spec_from_file_location('aufbaufile', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Builder(object):
    """
    The top level object that executes the build script.
    """

    def __init__(self, args):
        """
        Creates a new instance of the Builder class.
        :param args: The command line arguments, as provided by sys.argv.
        """

        parser = argparse.ArgumentParser(description='Builds an aufbau project.')
        parser.add_argument('--file', '-f', help='Path to the aufbau script.')
        parser.add_argument('target', nargs='*', help='One or more targets to be built.')
        args = parser.parse_args()

        self.script = locate_script(args.file)
        if self.script:
            self.root = os.path.dirname(self.script)
        self.target_names = args.target

    def run(self):
        load_script(self.script)
        from aufbau.graph import graph
        graph.build()
        self.targets = graph.walk(*self.target_names)
        for target in self.targets:
            print('Executing target: {0}'.format(target.name))
            target.action(self)
            print('Completed target: {0}'.format(target.name))
