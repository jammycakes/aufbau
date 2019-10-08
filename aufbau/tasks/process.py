import os
import os.path
import subprocess
import aufbau.tasks


class Execute(aufbau.tasks.Task):
    """
    Call an executable process.
    """
    def __init__(self, ctx):
        super(Execute, self).__init__(ctx)
        self._run_options = dict()

    def run_options(self, **kwargs):
        """
        Specifies the options to pass to subprocess.run in addition to the
        name of the executable and the command line arguments.
        :param kwargs:
        :return:
        """
        self._run_options.update(kwargs)

    def run(self, executable, *args):
        if executable.find(os.sep) >= 0 or executable.find(os.altsep) >= 0:
            executable = self.context.abspath(executable)

        run_args = [executable] + list(args)
        result = subprocess.run(run_args, **self._run_options)
        result.check_returncode()
