import os
import os.path
import subprocess
import aufbau.tasks


class Execute(aufbau.tasks.Task):
    """
    Call an executable process.
    """

    def run(self, executable, *args, **kwargs):
        if executable.find(os.sep) >= 0 or executable.find(os.altsep) >= 0:
            executable = self.context.abspath(executable)

        run_args = [executable] + list(args)
        result = subprocess.run(run_args, **kwargs)
        result.check_returncode()
