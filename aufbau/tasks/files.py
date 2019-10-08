import aufbau.tasks
import os
import shutil


class MakeDirs(aufbau.tasks.Task):
    """
    Ensure that a directory exists in the filesystem.
    """
    def run(self, path):
        os.makedirs(self.context.abspath(path), exist_ok=True)


class CleanDirs(MakeDirs):
    """
    Cleans out a directory.
    """
    def run(self, path):
        fullpath = self.context.abspath(path)
        shutil.rmtree(fullpath, ignore_errors=True)
        super(CleanDirs, self).run(fullpath)


class WriteFile(aufbau.tasks.Task):
    """
    Writes a file, line by line, to a given location.
    """
    def run(self, path, lines):
        lines = [line + '\n' for line in lines]
        with open(self.context.abspath(path), 'w') as f:
            f.writelines(lines)

