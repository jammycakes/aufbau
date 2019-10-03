import sys
from aufbau.core.builder import Builder

def main():
    builder = Builder(sys.argv)
    builder.run()
