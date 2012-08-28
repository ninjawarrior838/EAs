import sys
import random
import time


def main():
    if len(sys.argv) >= 2:  # check for the last comand line argument
        cfg = (sys.argv[-1])
    else:
        cfg = ('default.cfg')
    config = open(cfg, 'r')  # open config file
    log = open(config.readline().strip(), 'w')  # First line is the log file to use
    answerFile = open(config.readline().strip(), 'w')  # Second line is the answer file
    dataFile = config.readline().strip()  # Third line is the .dat file to use
    # check if a seed is provided, if 0, seed random from time in miliseconds
    seedT = config.readline().strip()
    if (seedT) == '0':
        seed = int(round(time.time() * 1000))
        random.seed(seed)
    else:
        random.seed(int(float(seedT)))
    runs = int(float(config.readline().strip()))
    evals = int(float(config.readline().strip()))


def generateGraph():
    return


if __name__ == '__main__':
    main()
