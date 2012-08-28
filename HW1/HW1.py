import sys
import random
import time


def generateGraph():
    return


def main():
    if len(sys.argv) >= 2:  # check for the last comand line argument
        cfg = (sys.argv[-1])
    else:
        cfg = ('default.cfg')
    config = open(cfg, 'r')  # open config file
    log = open(config.readline(), 'w')  # First line is the log file to use
    answerFile = open(config.readline(), 'w')  # Second line is the answer file
    dataFile = config.readline()  # Third line is the .dat file to use
    # check if a seed is provided, if 0, seed random from time in miliseconds
    seedT = config.readline()
    print seedT
    if (seedT) == 0:
        seed = int(round(time.time() * 1000))
        random.seed(seed)
    else:
        random.seed(seedT)
    #for x in range(10):
    print seed
