import sys
import random
import time
import copy

class Tree:
    def __init__(self, cargo, level=0, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right
        self.level = level

    def __str__(self):
        return str(self.cargo)


def print_tree_inorder(tree):
    if tree == None: return
    print_tree_inorder(tree.left)
    print str(tree.cargo),
    print_tree_inorder(tree.right)


def getTerminal():
    if bool(random.getrandbits(1)):
        retval = 'x'
    else:
        retval = str(random.randrange(0, 30))
    return retval


def getNonTerminal():
    values = ['+', '-', '*', '/', '**', 'sin', 'cos']
    index = random.randrange(0, len(values))
    return values[index]


def getInitialTree(maxDepth, tree):
    if tree.level == maxDepth:
        tree.right = Tree(getTerminal)
        tree.left = Tree(getTerminal)
        return

    tree.cargo = getNonTerminal()
    newTree = Tree(getNonTerminal())
    newTree.level = tree.level + 1
    getInitialTree(maxDepth, newTree)
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
    dataFile = config.readline().strip()
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

    fred = Tree('*')
    getInitialTree(4, fred)

    print_tree_inorder(fred)

    return


if __name__ == '__main__':
    main()
