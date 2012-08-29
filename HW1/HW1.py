import sys


def parse(str):
    config = open(str, 'r')
    datafile = config.readline()
    seedT = config.readline()
    evalNums = config.readline()
    runs = config.readline()
    return config, datafile, seedT, evalNums, runs


def main():
    if len(sys.argv) >= 2:
        cfg = parse(sys.argv[-1])
    else:
        cfg = parse('default.cfg')
