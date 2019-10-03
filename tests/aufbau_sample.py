from aufbau import target, depends_on, graph

@target
def clean():
    pass

@target
@depends_on(clean)
def build():
    pass

@target
@depends_on('build')
def test():
    pass

