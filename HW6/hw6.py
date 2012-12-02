import sys
import random
import time
import pdb
import copy
from math import sin, cos

class Tree:
    def __init__(self, cargo, left=None, right=None, level=0, value=0):
        self.cargo = cargo
        self.left = left
        self.right = right
        self.level = level
        self.value = value

    def __str__(self):
        return str(self.cargo)


def printTreeInorder(tree, level=0):
    if tree == None: return
    printTreeInorder(tree.left, level+1)
    print '   ' * level + str(tree.cargo)
    printTreeInorder(tree.right, level+1)


def outputTree(tree):
    if tree == None: return
    if tree.cargo == 'sin' or tree.cargo == 'cos':
        print '(',
        print str(tree.cargo) + '(',
        outputTree(tree.left)
        print ') )',
    elif tree.cargo == '**':
        print '(',
        print 'power' + '(',
        outputTree(tree.left)
        print ',',
        outputTree(tree.right)
        print ') )',
    else:
        print '(',
        outputTree(tree.left)
        print str(tree.cargo),
        outputTree(tree.right)
        print ')',

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
        tree.value = tree.left.value / tree.right.value
    elif tree.cargo == '**':
        tree.value = tree.left.value ** tree.right.value
    elif tree.cargo == 'sin':
        tree.value = sin(tree.left.value)
    elif tree.cargo == 'cos':
        tree.value = cos(tree.left.value)
    return


def evaluateFitness(data, test):

    return


def getTerminal():
    if bool(random.getrandbits(1)):
        retval = 'x'
    else:
        retval = str(random.randrange(1, 30))
    return retval


def getNonTerminal():
    values = ['+', '-', '*', '/', '**', 'sin', 'cos']
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
    else:
        log.write("\nUsing seed of: \t")
        log.write(str(seedT))
        random.seed(int(float(seedT)))
    maxInitialDepth = int(config.readline().strip())
    maxDepth = int(config.readline().strip())
    runs = int(config.readline().strip())
    evals = int(config.readline().strip())
    populationSize = int(config.readline().strip())
    parents = int(config.readline().strip())
    children = int(config.readline().strip())

    #read data file
    dataFile = open(dFile, 'r')
    dataFile.readline().strip()
    numPairs = int(dataFile.readline().strip())
    dataFile.readline().strip()
    data = []
    for i in range(numPairs):
        temp = dataFile.readline().strip().split(', ')
        data.append(temp)

    fred = Tree(getNonTerminal())
    getInitialTree(maxInitialDepth, fred)

    printTreeInorder(fred)

    evaluateTree(1, fred)
    print fred.value
    outputTree(fred)
    return


if __name__ == '__main__':
    main()
