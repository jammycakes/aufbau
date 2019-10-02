import sys
from aufbau.builder import Builder

def main():
    builder = Builder(sys.argv)
    builder.run()
