import sys
import random
import time
import copy
from math import sin, cos

class Tree:
    def __init__(self, cargo, left=None, right=None, level=0, value=0, fitness=0, fitP=0):
        self.cargo = cargo
        self.left = left
        self.right = right
        self.level = level
        self.value = value
        self.fitness = fitness
        self.fitP = fitP

    def __str__(self):
        return str(self.cargo)


def printTreeInorder(tree, level=0):
    if tree == None: return
    printTreeInorder(tree.left, level+1)
    print '   ' * level + str(tree.cargo)
    printTreeInorder(tree.right, level+1)


def outputTree(tree, answer):
    if tree == None: return
    if tree.cargo == 'sin' or tree.cargo == 'cos':
        answer.write('(' + str(tree.cargo) + '(')
        outputTree(tree.left, answer)
        answer.write(') )')
    elif tree.cargo == '**':
        answer.write('( power (')
        outputTree(tree.left, answer)
        answer.write(',')
        outputTree(tree.right, answer)
        answer.write(') )')
    else:
        answer.write('(')
        outputTree(tree.left, answer)
        answer.write(str(tree.cargo))
        outputTree(tree.right, answer)
        answer.write(')')

def evaluateTree(X, tree):
    if tree.left == None and tree.right == None:
        if tree.cargo == 'x':
            tree.value = X
        else:
            tree.value = float(tree.cargo)
        return

    evaluateTree(X, tree.left)
    evaluateTree(X, tree.right)
    if tree.cargo == '+':
        tree.value = tree.left.value + tree.right.value
    elif tree.cargo == '-':
        tree.value = tree.left.value - tree.right.value
    elif tree.cargo == '*':
        tree.value = tree.left.value * tree.right.value
    elif tree.cargo == '/':
        if tree.right.value == 0:
            tree.value = 0
        else:
            tree.value = tree.left.value / tree.right.value
    elif tree.cargo == '**':
        if tree.left.value < 0 and not float(tree.right.value).is_integer():
            tree.value = 0
        else:
            tree.value = tree.left.value ** tree.right.value
    elif tree.cargo == 'sin':
        tree.value = sin(tree.left.value)
    elif tree.cargo == 'cos':
        tree.value = cos(tree.left.value)
    return


def evaluateFitness(data, test):
    averageError = 0.0
    for value in data:
        evaluateTree(value[0], test)
        averageError += ((test.value - value[1]) ** 2)
    if averageError != 0:
        test.fitness = -averageError
    else:
        test.fitness = 0
    return


def getTerminal():
    if bool(random.getrandbits(1)):
        retval = 'x'
    else:
        retval = str(random.randrange(1, 5))
    return retval


def getNonTerminal():
    values = ['+', '-', '*', '/', 'sin', 'cos']
    index = random.randrange(0, len(values))
    return values[index]


def getInitialTree(maxDepth, tree):
    if tree.level == maxDepth:
        tree.right = Tree(getTerminal())
        tree.left = Tree(getTerminal())
        return

    tree.cargo = getNonTerminal()
    leftNode = Tree(getNonTerminal())
    rightNode = Tree(getNonTerminal())
    if tree.cargo != 'sin' or tree.cargo != 'cos':
        rightNode.level = tree.level + 1
        leftNode.level = tree.level + 1
        getInitialTree(maxDepth, rightNode)
        getInitialTree(maxDepth, leftNode)
        tree.right = rightNode
        tree.left = leftNode
    else:
        leftNode.level = tree.level + 1
        getInitialTree(maxDepth, leftNode)
        tree.left = leftNode

    return


#tree is the tree to be mutated passed by reference
def mutate(tree, maxDepth):
    if tree == None: return
    chance = 10
    if (random.randrange(0, chance) == 0):
        depth = tree.level
        numNewLevels = random.randrange(0, 2)
        if depth + numNewLevels <= maxDepth:
            getInitialTree((depth + numNewLevels), tree)
        else:
            mutate(tree, maxDepth)
    else:
        mutate(tree.left, maxDepth)
        mutate(tree.right, maxDepth)


def recombine(tree1, tree2):

    return


def getParents(population, numParents):
    retval, populationAverage= [], 0.0
    #fitness proportional selection
    for tree in population:
        populationAverage += tree.fitness
    for tree in population:
        tree.fitP = (tree.fitness / populationAverage)
    population.sort(key = lambda x: x.fitP)
    for i in range(numParents):
        retval.append(copy.deepcopy(population[i]))
    return retval


#returns the time in miliseconds
def getTime():
    return int(round(time.time() * 1000))


#returns the difference of the current time and x
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
    dFile = config.readline().strip()
    # check if a seed is provided, if 0, seed random from time in miliseconds
    seedT = config.readline().strip()
    if (seedT) == '0':
        seed = getTime()
        log.write("\nUsing seed of: \t" + str(seed))
        random.seed(seed)
        log.flush()
    else:
        log.write("\nUsing seed of: \t")
        log.write(str(seedT))
        random.seed(int(float(seedT)))
        log.flush()
    maxInitialDepth = int(config.readline().strip())
    maxDepth = int(config.readline().strip())
    runs = int(config.readline().strip())
    maxEvals = int(config.readline().strip())
    populationSize = int(config.readline().strip())
    numParents = int(config.readline().strip())
    children = int(config.readline().strip())

    #read data file
    dataFile = open(dFile, 'r')
    dataFile.readline().strip()
    numPairs = int(dataFile.readline().strip())
    dataFile.readline().strip()
    data = []
    for i in range(numPairs):
        temp = dataFile.readline().strip().split(',')
        temp[0] = float(temp[0])
        temp[1] = float(temp[1])
        data.append(temp)

    globalBestTree = Tree('*')
    globalBestTree.fitness = -100000000

    for run in range(runs):
        evals = 0
        population = []
        log.write('\n\nRun: ' + str(run + 1))

        #innitialisation
        for tree in range(populationSize):
            fred = Tree(getNonTerminal())
            getInitialTree(maxInitialDepth, fred)
            population.append(fred)
        for tree in population:
            evaluateFitness(data, tree)

        while evals <= maxEvals:
            newPopulation = []
            #parent selection
            parents = getParents(population, numParents)

            while len(newPopulation) < populationSize:
                fred = random.randrange(len(parents))
                bob = copy.deepcopy(parents[fred])
                mutate(bob, maxDepth)
                newPopulation.append(bob)

            #evaluate new fitnesses
            for tree in newPopulation:
                evaluateFitness(data, tree)
                evals += 1

            localBestTree, sumFit = population[0], 0
            for tree in population:
                sumFit += tree.fitness
                if tree.fitness > localBestTree.fitness:
                    localBestTree = tree
            averageFit = sumFit / len(population)
            if localBestTree.fitness > globalBestTree.fitness:
                globalBestTree = localBestTree

            #logging and output
            log.write('\n' + str(evals) + '\t' + str(averageFit) + '\t' + str(localBestTree.fitness))
            log.flush()
            answer = open(answerFile, 'w')
            answer.close()

            answer = open(answerFile, 'a+')
            answer.write(str(globalBestTree.fitness) + '\n')
            outputTree(globalBestTree, answer)
            answer.write('\n\n')
            answer.close()

            population = newPopulation

    return


if __name__ == '__main__':
    main()
