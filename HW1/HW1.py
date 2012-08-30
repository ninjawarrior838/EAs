import sys
import random
import time


def generateGraph(x):
    partition = (bin(random.randrange(0, 2 ** (x))))[2:]
    return partition.zfill(x)


def checkFitness(data, test):
    #smallest partition
    partition = str(test).count('1')
    numCuts = 0

    for num in range(1, len(test) + 1):
        for pos in range(len(data[str(num)])):
            if test[num - 1] != test[int(data[str(num)][pos]) - 1]:
                numCuts += 1

    if partition <= 0:
        return 100000
    elif partition >= len(test):
        return 100000
    elif partition <= (len(test) / 2):
        partition = partition
    else:
        partition = len(test) - partition
    return float(numCuts / 2) / partition


def getTime():
    return int(round(time.time() * 1000))


def timer(x):
    return ((int(round(time.time() * 1000))) - x)


def main():
    # check for the last comand line argument
    if len(sys.argv) >= 2:
        cfg = (sys.argv[-1])
    else:
        cfg = ('default.cfg')
    config = open(cfg, 'r')

    logFile = config.readline().strip()
    log = open(logFile, 'w')
    log.write("Result Log\n\n")

    answerFile = config.readline().strip()
    dataFile = config.readline().strip()
    log.write("Using data file: " + dataFile)

    # check if a seed is provided, if 0, seed random from time in miliseconds
    seedT = config.readline().strip()
    if (seedT) == '0':
        seed = getTime()
        log.write("\nUsing seed of: \t" + str(seed))
        random.seed(seed)
    else:
        log.write("\nUsing seed of: \t")
        log.write(str(seedT))
        random.seed(int(float(seedT)))

    #some initial parsing on the dat file
    runs = int(float(config.readline().strip()))
    evals = int(float(config.readline().strip()))

    #make a dictionary of edges
    data = {}
    dFile = open(dataFile, 'r')
    verticies = int(float(dFile.readline().strip()))
    edges = int(float(dFile.readline().strip()))
    for i in range(1, (verticies + 1)):
        data[str(i)] = []
    for lines in range(edges):
        temp = dFile.readline().strip().split()
        data[(temp[0])].append(temp[1])
        data[(temp[1])].append(temp[0])
    dFile.close()

    #Run the program the correct number of times logging as it goes
    bestCut = int
    bestFit = 100000.0
    for run in range(1, runs + 1):
        log.write('\n\nRun: ' + str(run + 1))
        localBestFit = 100000.0
        localBestCut = int
        t = getTime()

        for checks in range(evals):
            test = generateGraph(verticies)
            fitness = checkFitness(data, test)
            if fitness < localBestFit:
                localBestFit = fitness
                localBestCut = test
                log.write('\n' + str(checks) + '\t' + str(localBestFit))
                if localBestFit < bestFit:
                    bestFit = localBestFit
                    bestCut = localBestCut
        print 'run: ', str(run), 'done in ', str(timer(t)), 'm seconds'

    answer = open(answerFile, 'w')
    answer.write(str(bestCut) + '\n' + str(bestFit))
    print ('Done!')

if __name__ == '__main__':
    main()
