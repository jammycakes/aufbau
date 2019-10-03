import subprocess
import aufbau.tasks


class Execute(aufbau.tasks.Task):
    """
    Call an executable process.
    """

    def run(self, executable, *args, **kwargs):
        found_prefix = [
            prefix
            for prefix in ['./', '~/', '.\\', '~\\']
            if executable.startswith(prefix)
        ]
        found_prefix = found_prefix[0] if found_prefix else False
        if found_prefix:
            executable = self.context.abspath(executable[len(found_prefix):])

        run_args = [executable] + list(args)
        result = subprocess.run(run_args, **kwargs)
        result.check_returncode()
