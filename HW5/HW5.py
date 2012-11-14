import sys
import random
import time
import pdb
from operator import itemgetter


#generates a random binary string of size x
def generateRandGraph(x):
    partition = (bin(random.randrange(0, 2 ** (x))))[2:]
    return partition.zfill(x)

#returns true if x dominates y
def dominates(x, y):
    if x['numerator'] <= y['numerator'] and x['denominator'] > y['denominator']:
        return True
    elif x['numerator'] < y['numerator'] and x['denominator'] >= y['denominator']:
        return True
    else:
        return False


def generateGraph(size, chance):
    data = {}
    for i in range(0, (size + 1)):
        data[str(i)] = []
    for node1 in range(0, size):
        for node2 in range(1, size):
            if((random.randrange(0, chance) == 0) and node1 != node2):
                data[str(node1)].append(node2)
                data[str(node2)].append(node1)
    return data


#appends the domination level to each cut in the population
def findDomLevel(population):
    domList, pop, dominatesRef, dominatedRef = [], [], [], []
    row0, row = [], 1
    for cuts in range(0, len(population)):
        dominatesRef.append([])
        dominatedRef.append([])
        population[cuts]['reference'] = cuts
        for challenger in range(0, len(population)):
            if dominates(population[cuts], population[challenger]):
                dominatesRef[cuts].append(population[challenger])
            elif dominates(population[challenger], population[cuts]):
                dominatedRef[cuts].append(population[challenger])

    for element in range(0, len(dominatedRef)):
        if not dominatedRef[element]:
            population[element]['DomLevel'] = 0
            row0.append(population[element])
        else:
            pop.append(population[element])

    domList.append(row0)
    while pop:
        rowi = []
        rowi.append(pop.pop())
        for element in range(len(pop) - 1):
            for k in range(len(rowi) - 1):
                if dominates(rowi[k], pop[element]):
                    break
                elif dominates(pop[element], rowi[k]):
                    pop.append(rowi.pop(k))
        domList.append(rowi)

    for level in range(1, len(domList)):
        for k in domList[level]:
            population[k['reference']]['DomLevel'] = level
    return


#returns the number of subgraphs
def isConnected(test, data):
    explore, subgraphs = [], 0
    while(test):
        explore.append(test.pop())
        while(explore):
            for i in data[str(explore[0])]:
                if int(i) in test:
                    explore.append(int(i))
                    test.remove(int(i))
            explore.pop(0)
        subgraphs = subgraphs + 1
    return subgraphs


#Takes in the data, and a test binary string and returns the highest negated fitness
def checkFitness(fitFunction, data, test, penalty):
    #smallest partition
    partition = str(test).count('1')
    numCuts, retvalList = 0, []

    #find the lowest number of cuts
    for num in range(1, len(test) + 1):
        for pos in range(len(data[str(num)])):
            if test[num - 1] != test[int(data[str(num)][pos]) - 1]:
                numCuts += 1

    if partition <= 0:
        retvalList.append(-100000)
    elif partition >= len(test):
        retvalList.append(-100000)
    elif partition <= (len(test) / 2):
        partition = partition
        retvalList.append((float(numCuts / 2) / partition) * (-1))
    else:
        partition = len(test) - partition
        retvalList.append((float(numCuts / 2) / partition) * (-1))
    retvalList.append(numCuts / 2)
    retvalList.append(partition)
    if numCuts == 0:
        retvalList[1] = 100000

    if(fitFunction == 'subgraphs'):
        test1, test2, subgraphs, numCuts = [], [], 0, 0
        for i in range(1, len(test) + 1):
            if(test[i - 1] == '1'):
                test1.append(i)
            else:
                test2.append(i)
        subgraphs = isConnected(test1, data)
        subgraphs = subgraphs + isConnected(test2, data)
    else:
        return retvalList
    retvalList[0] = (retvalList[0] - ((subgraphs - 2) * (penalty)))
    return retvalList

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


#choses the parents according to the config file, returns a list of cuts
def getParents(parentSelection, k, population, numParents):
    retval = []
    if(parentSelection == 'fitness proportional'):
        fitnessProportion = 0
        survive = []
        for cuts in population:
            fitnessProportion = fitnessProportion + cuts['fitness']
        for cuts in population:
            survive.append((cuts['cut'], cuts['fitness'] / fitnessProportion))
        parents = sorted(survive, key=itemgetter(1))[:numParents]
        for i in parents:
            retval.append(i[0])
        return retval

    elif(parentSelection == 'k-Tournament Selection without replacement'):
        #findDomLevel(population)
        while (len(retval) < numParents):
            tournament = []
            while (len(tournament) < k):
                #fill tourament
                chalenger = random.randrange(0, len(population) - 1)
                if(population[chalenger] not in tournament):
                    tournament.append(population[chalenger])
            #pick top one
            ordered = sorted(tournament, key=itemgetter('DomLevel'), reverse=True)
            retval.append(ordered[0]['cut'])
        return retval

    elif(parentSelection == 'k-Tournament Selection with replacement'):
        #findDomLevel(population)
        while (len(retval) < numParents):
            tournament = []
            while (len(tournament) < k):
                #fill tourament
                chalenger = random.randrange(0, len(population) - 1)
                tournament.append(population[chalenger])
            #pick top one
            ordered = sorted(tournament, key=itemgetter('DomLevel'), reverse=True)
            retval.append(ordered[0]['cut'])
        return retval

    elif(parentSelection == 'uniform random'):
        while (len(retval) < numParents):
            chalenger = random.randrange(0, len(population) - 1)
            if(population[chalenger] not in retval):
                retval.append(population[chalenger]['cut'])
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


def mutateGraph(size, chance, data):
    for node1 in range(0, size):
        for node2 in range(1, size):
            trigger = (random.randrange(0, chance) == 0)
            if(trigger and node1 != node2 and (node2 not in data[node1])):
                data[str(node1)].append(node2)
                data[str(node2)].append(node1)
            elif(trigger and node1 != node2 and (node2 in data[node1])):
                data[str(node1)].remove(node2)
                data[str(node2)].remove(node1)
    return data


#returns a recombined version of x and y according to the recombination variable
def recombine(recombination, n, x, y):
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


def recombineGraph(size, chance, data1, data2):
    retval = data1
    for node1 in range(0, size):
        for node2 in range(1, size):
            trigger = (random.randrange(0, chance) == 0)
            if(trigger and node1 != node2):
                if((node2 in data1[node1]) and (node2 not in data2[node1])):
                    if(bool(random.getrandbits(1))):
                        retval[str(node1)].remove(node2)
                    else:
                        retval[str(node1)].append(node1)
    return retval
"""
            and (node2 not in data[node1])):
                data[str(node1)].append(node2)
                data[str(node2)].append(node1)
            elif(trigger == True and node1 != node2 and (node2 in data[node1])):
                data[str(node1)].remove(node2)
                data[str(node2)].remove(node1)
"""


def selectSurvivors(survivalSelection, population, numSurvive, k):
    retval = []
    if(survivalSelection == 'fitness proportional'):
        fitnessProportion = 0
        survive = []
        for cuts in population:
            fitnessProportion = fitnessProportion + cuts['fitness']
        for cuts in population:
            survive.append((cuts['cut'], cuts['fitness'] / fitnessProportion))
        parents = sorted(survive, key=itemgetter(1))[:numSurvive]
        for i in parents:
            retval.append(i[0])
        return retval

    elif(survivalSelection == 'k-Tournament Selection without replacement'):
        #findDomLevel(population)
        while (len(retval) < numSurvive):
            tournament = []
            while (len(tournament) < k):
                #fill tourament
                chalenger = random.randrange(0, len(population) - 1)
                if(population[chalenger] not in tournament):
                    tournament.append(population[chalenger])
            #pick top one
            ordered = sorted(tournament, key=itemgetter('DomLevel'), reverse=True)
            retval.append(ordered[0])
        return retval

    elif(survivalSelection == 'k-Tournament Selection with replacement'):
        #findDomLevel(population)
        while (len(retval) < numSurvive):
            tournament = []
            while (len(tournament) < k):
                #fill tourament
                chalenger = random.randrange(0, len(population) - 1)
                tournament.append(population[chalenger])
            #pick top one
            ordered = sorted(tournament, key=itemgetter('DomLevel'), reverse=True)
            retval.append(ordered[0])
        return retval

    elif(survivalSelection == 'uniform random'):
        while (len(retval) < numSurvive):
            chalenger = random.randrange(0, len(population) - 1)
            if(population[chalenger] not in retval):
                retval.append(population[chalenger])
        return retval

    elif(survivalSelection == 'truncation'):
        #findDomLevel(population)
        ordered = sorted(population, key=itemgetter('DomLevel'), reverse=True)
        return ordered[:numSurvive]


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

    numNodes = int(float(config.readline().strip()))
    #populaion
    popSize = int(float(config.readline().strip()))
    #graph sample size
    graphSampleSize = int(float(config.readline().strip()))
    #lambda
    numParents = int(float(config.readline().strip()))
    #mew
    numChlidren = int(float(config.readline().strip()))

    #parsing for different algorithm arguements
    fitFunction = config.readline().strip()
    penalty = float(config.readline().strip())
    initialisation = config.readline().strip()
    parentSelection = config.readline().strip()
    k = int(config.readline().strip())
    recombination = config.readline().strip()
    n = int(config.readline().strip())
    mutation = config.readline().strip()
    survivalStrategy = config.readline().strip()
    survivalSelection = config.readline().strip()
    numSurvive = popSize

    #Run the program the correct number of times, logging as it goes
    average = open(averageFile, 'w')
    best = open(bestFile, 'w')
    globalBest = -100000.0
    globalBestCut = int
    population = []

    for run in range(1, runs + 1):
        log.write('\n\nRun: ' + str(run))
        t = getTime()

        #reinitialize both cuts and graphs every run
        #initialize graphs first
        data, graphs = {}, []
        if(dataFile == 'none'):
            for i in range(0, popSize):
                data = generateGraph(numNodes, 10)
                data['fitness'] = 0.0
                data['timesUsed'] = 0
                graphs.append(data)
        else:
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

        #initialize cuts
        for i in range(0, popSize):
            combo, retvalList = {}, []
            cut = getInitial(initialisation, numNodes)
            combo['cut'] = cut
            #retvalList = checkFitness(fitFunction, data, cut, penalty)
            combo['fitness'] = 0.0
            combo['timesUsed'] = 0
            #combo['numerator'] = retvalList[1]
            #combo['denominator'] = retvalList[2]
            population.append(combo)

        #initialize fitness for both graphs and cuts
        for cut in population:
            for i in range(0, graphSampleSize):
                if(cut['timesUsed'] < 10):
                    testCut = cut
                    testGraphIndex = random.randrange(0, popSize)
                    while(graphs[testGraphIndex]['timesUsed'] >= 10):
                        testGraphIndex = random.randrange(0, popSize)
                    retvalList = checkFitness(fitFunction, graphs[testGraphIndex], testCut['cut'], penalty)
                    cut['fitness'] = cut['fitness'] + retvalList[0]
                    cut['timesUsed'] = cut['timesUsed'] + 1
                    graphs[testGraphIndex]['fitness'] = graphs[testGraphIndex]['fitness'] + (1 / retvalList[0])
                    graphs[testGraphIndex]['timesUsed'] = graphs[testGraphIndex]['timesUsed'] + 1

        #find the average fitness by dividing by the number of times used and reset times used
        for i in range(0, popSize):
            population[i]['fitness'] = population[i]['fitness'] / population[i]['timesUsed']
            population[i]['timesUsed'] = 0
            graphs[i]['fitness'] = graphs[i]['fitness'] / graphs[i]['timesUsed']
            graphs[i]['timesUsed'] = 0

        pdb.set_trace()
        for checks in range(evals):
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
                combo, retvalList = {}, []
                cut = oldPopulation.pop()
                combo['cut'] = cut
                #retvalList = checkFitness(fitFunction, data, cut, penalty)
                combo['fitness'] = retvalList[0]
                #combo['numerator'] = retvalList[1]
                #combo['denominator'] = retvalList[2]
                population.append(combo)
            for cuts in population:
                sumAverage = sumAverage + cuts['fitness']

            #Survival Selection
            population = selectSurvivors(survivalSelection, population, numSurvive, k)

            #put the answer in the answer file
            answer = open(answerFile, 'w')
            answer.close()

            ordered = sorted(population, key=itemgetter('fitness'))
            localBest = ordered[-1]['fitness']
            localBestCut = ordered[-1]['cut']
            log.write('\n' + str(checks) + '\t' + str(sumAverage / (numChlidren + numParents)) + '\t' + str(localBest))
            average.write(str(sumAverage / (numChlidren + numParents)) + '\n')
            best.write(str(localBest) + '\n')

            if (localBest > globalBest):
                globalBest = localBest
                globalBestCut = localBestCut

        average.write('\n\n')
        best.write('\n\n')
        average.flush()
        best.flush()
        print 'run: ', str(run), 'done in ', str(timer(t)), 'm seconds'

    log.close()
    average.close()
    best.close()

    print ('Done!')

if __name__ == '__main__':
    main()
