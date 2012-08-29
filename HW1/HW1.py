import sys
import random
import time


def generateGraph(x):
    partition = (bin(random.randrange(0, 2 ** (x))))[2:]
    return partition.zfill(x)


def checkFitness(x, y, numEvals, data, test):
    answer = open(x, 'a')
    log = open(y, 'a')
    #smallest partition
    partition = 0
    numCuts = 0

    for num in range(len(test)):
        if test[num] == '1':
            partition += 1
        for pos in range(len(test)):
            if(  str(num + 1 ) in data[str(pos + 1)] and test[num] != test[pos]):
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
    log.close()

    #print data
    #for run in range(runs):
        #test = generateGraph(verticies)

        #checkFitness(answerFile, logFile, evals, test)
    fitness = checkFitness(answerFile, logFile, evals, data, '10101100')  #best cut
    print fitness

if __name__ == '__main__':
    main()
