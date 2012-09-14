import sys
import random
import time
from operator import itemgetter


#generates a random binary string of size x
def generateRandGraph(x):
    partition = (bin(random.randrange(0, 2 ** (x))))[2:]
    return partition.zfill(x)


#Takes in the data, and a test binary string and returns the highest negated fitness
def checkFitness(data, test):
    #smallest partition
    partition = str(test).count('1')
    numCuts = 0

    #find the lowest number of cuts
    for num in range(1, len(test) + 1):
        for pos in range(len(data[str(num)])):
            if test[num - 1] != test[int(data[str(num)][pos]) - 1]:
                numCuts += 1

    if partition <= 0:
        return -100000
    elif partition >= len(test):
        return -100000
    elif partition <= (len(test) / 2):
        partition = partition
    else:
        partition = len(test) - partition
    return (float(numCuts / 2) / partition) * (-1)


#returns the time in miliseconds
def getTime():
    return int(round(time.time() * 1000))


#returns the difference of the current time and x
def timer(x):
    return ((int(round(time.time() * 1000))) - x)


#returns a random bitstring according to the initialisation rule and number of verticies
def getInitial(initialisation, verticies):
    if (initialisation == 'uniform random'):
        return generateRandGraph(verticies)


#choses the parents according to the config file
def getParents(parentSelection, k, population, numParents):
    if(parentSelection == 'fitness proportional'):
        fitnessProportion = 0
        survive = []
        retval = []
        for cuts in population:
            fitnessProportion = fitnessProportion + cuts['fitness']
        for cuts in population:
            survive.append((cuts['cut'], cuts['fitness'] / fitnessProportion))
        parents = sorted(survive, key=itemgetter(1), reverse=True)[:numParents]
        #parents = sorted(population, key=itemgetter('fitness'), reverse=True)
        for i in parents:
            retval.append(i[0])
        return retval


#returns a mutated version of the binary intager test input
def mutate(mutation, test):
    if (mutation == 'bit flip'):
        retval = list(str(test))
        for bit in range(0, len(retval)):
            if bool(random.getrandbits(1)) and retval[bit] == '0':
                retval[bit] = '1'
            elif bool(random.getrandbits(1)) and retval[bit] == '1':
                retval[bit] = '0'
            digits = [int(x) for x in retval]
    else:
        print ('error! mutation is not defined correctly')
    return ''.join([str(x) for x in digits])


#returns a recombined version of x and y according to the recombination variable
def recombine(recombination, x, y,):
    if(recombination == 'uniform crossover'):
        retval1 = list(str(x))
        retval2 = list(str(y))
        for bit in range(0, len(retval1)):
            if bool(random.getrandbits(1)):
                retval1[bit] = retval2[bit]
            digits = [int(x) for x in retval1]
    else:
        print ('error! recombination is not defined correctly')
    return ''.join([str(x) for x in digits])


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
    #populaion
    popSize = int(float(config.readline().strip()))
    #lambda
    numParents = int(float(config.readline().strip()))
    #mew
    numChlidren = int(float(config.readline().strip()))
    #survivor number
    numSurvivor = int(float(config.readline().strip()))

    #parsing for different algorithm arguements
    representation = config.readline().strip()
    initialisation = config.readline().strip()
    parentSelection = config.readline().strip()
    #if using k-Tournament Selection the next line should be k else nothing
    if (parentSelection == 'k-Tournament Selection without replacement'):
        k = config.readline().strip()
    else:
        k = 0
    recombination = config.readline().strip()
    mutation = config.readline().strip()
    survivalSelection = config.readline().strip()
    termination = int(config.readline().strip())
    if (termination == 0):
        termination = evals

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

    #primeing the main function with the initial values
    bestCut = int
    bestFit = -100000.0

    #Run the program the correct number of times, logging as it goes
    for run in range(1, runs + 1):
        population = []
        #create the initial population according to the initialisation
        for i in range(0, popSize):
            combo = {}
            cut = getInitial(initialisation, verticies)
            combo['cut'] = cut
            combo['fitness'] = checkFitness(data, cut)
            population.append(combo)
        log.write('\n\nRun: ' + str(run))
        t = getTime()

        #for checks in range(termination):

        #parent selection
        parents = []
        parents = getParents(parentSelection, k, population, numParents)
        print parents
        #recombination

        #mutation

        #survivor selection

        #termination
"""
        for checks in range(evals):
            fitness = checkFitness(data, initial)
            if fitness < localBestFit:
                localBestFit = fitness
                localBestCut = initial
                log.write('\n' + str(checks) + '\t' + str(localBestFit))
                if localBestFit < bestFit:
                    bestFit = localBestFit
                    bestCut = localBestCut
        print 'run: ', str(run), 'done in ', str(timer(t)), 'm seconds'

    answer = open(answerFile, 'w')
    answer.write(str(bestCut) + '\n' + str(bestFit))
    print ('Done!')
"""
if __name__ == '__main__':
    main()
