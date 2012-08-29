import sys
import random
import time


def generateGraph(x):
    dFile = open(x, 'r')
    verticies = int(float(dFile.readline().strip()))
    edges = int(float(dFile.readline().strip()))
    partition = (bin(random.randrange(0, 2**(verticies))))[2:]
    return partition.zfill(verticies)


def checkFitness(x, y, numEvals, test):
    answer = open(x, 'a')
    log = open(y, 'a')
    return


def getTime():
    return int(round(time.time() * 1000))


def timer(x):
    return ((int(round(time.time() * 1000))) -x)


def main():
    if len(sys.argv) >= 2:  # check for the last comand line argument
        cfg = (sys.argv[-1])
    else:
        cfg = ('default.cfg')
    config = open(cfg, 'r')

    logFile = config.readline().strip()
    log = open(logFile, 'w')

    answerFile = config.readline().strip()
    dataFile = config.readline().strip()
    log.write("Using data file: ")
    log.write(dataFile)

    # check if a seed is provided, if 0, seed random from time in miliseconds
    seedT = config.readline().strip()
    if (seedT) == '0':
        seed = getTime()
        log.write("\nUsing seed of: \t")
        log.write(str(seed))
        random.seed(seed)
    else:
        log.write("\nUsing seed of: \t")
        log.write(str(seedT))
        random.seed(int(float(seedT)))
    runs = int(float(config.readline().strip()))
    evals = int(float(config.readline().strip()))
        #need to make the dictionary of edges

    log.close()
    for run in range(runs):
        test = generateGraph(dataFile)

        checkFitness(answerFile, logFile, evals, test)


if __name__ == '__main__':
    main()
