import sys
import random
import time
from operator import itemgetter


#generates a random binary string of size x
def generateRandGraph(x):
    partition = (bin(random.randrange(0, 2 ** (x))))[2:]
    return partition.zfill(x)


#Takes in the data, and a test binary string and returns the highest negated fitness
def checkFitness(fitFunction, data, test):
    if(fitFunction == 'origional'):
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
'''
    elif(fitFunction == 'subgraphs'):
        explored, explorable, reachable = [], [], []
        explored.zfill(len(test))
        for i in test:
            if(i == )
'''

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
        survive, retval = [], []
        for cuts in population:
            fitnessProportion = fitnessProportion + cuts['fitness']
        for cuts in population:
            survive.append((cuts['cut'], cuts['fitness'] / fitnessProportion))
        parents = sorted(survive, key=itemgetter(1))[:numParents]
        for i in parents:
            retval.append(i[0])
        return retval

    elif(parentSelection == 'k-Tournament Selection without replacement'):
        retval = []
        while (len(retval) < numParents):
            tournament = []
            while (len(tournament) < k):
                #fill tourament
                chalenger = random.randrange(0, len(population) - 1)
                tournament.append(population[chalenger])
            #pick top one
            ordered = sorted(tournament, key=itemgetter('fitness'))
            retval.append(ordered[0]['cut'])
        return retval


#returns a mutated version of the binary intager test input
def mutate(mutation, test):
    if (mutation == 'bit flip'):
        retval = list(str(test))
        for bit in range(0, len(retval)):
            flip = random.getrandbits(1)
            if flip and retval[bit] == '0':
                retval[bit] = '1'
            elif flip and retval[bit] == '1':
                retval[bit] = '0'
            digits = [int(x) for x in retval]
    else:
        print ('error! mutation is not defined correctly')
    return ''.join([str(x) for x in digits])


#returns a recombined version of x and y according to the recombination variable
def recombine(recombination, n, x, y,):
    if(recombination == 'uniform crossover'):
        val1 = list(str(x))
        val2 = list(str(y))
        retval = []
        for bit in range(0, len(val1)):
            if bool(random.getrandbits(1)):
                val1[bit], val2[bit] = val2[bit], val1[bit]
            digits1 = [int(x) for x in val1]
            digits2 = [int(x) for x in val2]

    elif (recombination == 'n-point crossover'):
        val1 = list(str(x))
        val2 = list(str(y))
        retval = []
        index = random.randrange(0, len(val1) - n)
        for bit in range(0, n):
            val1[index + bit], val2[index + bit] = val2[index + bit], val1[index + bit]
            digits1 = [int(x) for x in val1]
            digits2 = [int(x) for x in val2]
    else:
        print ('error! recombination is not defined correctly')
    retval.append(''.join([str(x) for x in digits1]))
    retval.append(''.join([str(x) for x in digits2]))
    return retval


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

    averageFile = config.readline().strip()
    bestFile = config.readline().strip()
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

    #parsing for different algorithm arguements
    fitFunction = config.readline().strip()
    representation = config.readline().strip()
    initialisation = config.readline().strip()
    parentSelection = config.readline().strip()
    k = int(config.readline().strip())
    recombination = config.readline().strip()
    n = int(config.readline().strip())
    mutation = config.readline().strip()
    survivalStrategy = config.readline().strip()
    #survivalSelection = config.readline().strip()
    #stop is the how many runs to stop after if there is no change in the best cut
    stop = int(config.readline().strip())

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

    #Run the program the correct number of times, logging as it goes
    average = open(averageFile, 'w')
    best = open(bestFile, 'w')
    globalBest = -100000.0
    globalBestCut = int
    for run in range(1, runs + 1):
    #reinitialise the population every run
        population = []
        for i in range(0, popSize):
            combo = {}
            cut = getInitial(initialisation, verticies)
            combo['cut'] = cut
            combo['fitness'] = checkFitness(fitFunction, data, cut)
            population.append(combo)

        #create the initial population according to the initialisation
        log.write('\n\nRun: ' + str(run))
        t = getTime()

        history, done = [], False
        for checks in range(evals):
            #termination conditon
            if (done):
                print 'early termination'
                break
            #parent selection
            parents, children = [], []
            parents = getParents(parentSelection, k, population, numParents)

            #recombination
            while (len(children) < (numChlidren / 2)):
                mom = random.randrange(0, len(parents) - 1)
                dad = random.randrange(0, len(parents) - 1)
                if (mom != dad):
                    children = children + recombine(recombination, n, parents[mom], parents[dad])

            #mutation
            mutantChildren = children[:]
            while (len(children) < numChlidren):
                mutantChild = mutantChildren.pop()
                mutantChild = mutate(mutation, mutantChild)
                children.append(mutantChild)

            if(survivalStrategy == 'plus'):
                oldPopulation = parents + children
            elif(survivalStrategy == 'comma'):
                oldPopulation = children
            else:
                print 'Error: no survival strategy selected'

            #evaluate new fitnesses
            population, sumAverage = [], 0
            while (len(oldPopulation) > 0):
                combo = {}
                cut = oldPopulation.pop()
                combo['cut'] = cut
                combo['fitness'] = checkFitness(fitFunction, data, cut)
                population.append(combo)
            for cuts in population:
                sumAverage = sumAverage + cuts['fitness']
            ordered = sorted(population, key=itemgetter('fitness'))
            localBest = ordered[-1]['fitness']
            localBestCut = ordered[-1]['cut']
            log.write('\n' + str(checks) + '\t' + str(sumAverage / (numChlidren + numParents)) + '\t' + str(localBest))
            average.write(str(sumAverage / (numChlidren + numParents)) + '\n')
            best.write(str(localBest) + '\n')

            #Survival Selection

            #Early termination if no change in n runs
            history.append(localBest)
            if (len(history) > stop):
                history.pop(0)
                compare = history[:]
                compare.sort()
                if (compare[-1] == compare[0]):
                    done = True

        average.write('\n\n')
        best.write('\n\n')
        average.flush()
        best.flush()
        if (localBest > globalBest):
            globalBest = localBest
            globalBestCut = localBestCut
        print 'run: ', str(run), 'done in ', str(timer(t)), 'm seconds'

    log.close()
    average.close()
    best.close()

    answer = open(answerFile, 'w')
    answer.write(str(globalBestCut) + '\n' + str(globalBest))

    print ('Done!')

if __name__ == '__main__':
    main()
