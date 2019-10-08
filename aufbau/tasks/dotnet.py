import aufbau.tasks.process


class Dotnet(aufbau.tasks.process.Execute):
    """
    Runs an arbitrary dotnet command.
    """
    def __init__(self, ctx):
        super(Dotnet, self).__init__(ctx)
        self._sdk_options = []
        self._options = []

    def sdk_options(self, *options):
        self._sdk_options += options
        return self

    def options(self, *options):
        """
        Defines additional options to pass to the dotnet executable.
        :param options: Additional command line options to pass to the executable.
        :return:
        """
        self._options += options
        return self

    def run(self, command, *args):
        super(Dotnet, self).run('dotnet', *self._sdk_options, command, *self._options, *args)


class Build(Dotnet):
    """
    Runs dotnet build.
    """
    def run(self, project):
        super(Build, self).run('build', self.context.abspath(project))


class Test(Dotnet):
    """
    Runs dotnet test.
    """
    def run(self, project, **runsettings):
        runsettings_args = [
            "{0}={1}".format(key, runsettings[key]) for key in runsettings
        ]
        if runsettings_args:
            runsettings_args.insert(0, '--')
        super(Test, self).run('test', self.context.abspath(project), runsettings_args)


class Pack(Dotnet):
    """
    Runs dotnet pack.
    """
    def run(self, project, output_dir=None):
        if output_dir:
            self.options('-o', self.context.abspath(output_dir))
        super(Pack, self).run('pack', self.context.abspath(project))
