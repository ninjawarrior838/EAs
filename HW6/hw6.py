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
    print tree.cargo,
    print_tree_inorder(tree.right)


def getTerminal():
    if bool(random.getrandbits(1)):
        retval = 'x'
    else:
        retval = str(random.randrange(0, 30))
    return retval


def getNonTerminal():
    retval = str
    values = ['+', '-', '*', '/', '**', 'sin', 'cos']
    index = random.randrange(0, len(values))
    return retval[index]


def getInitialTree(maxDepth, tree):
    if tree.level == maxDepth: return
    leftNode = Tree(getTerminal)
    rightNode = Tree(getTerminal)
    newTree = Tree(getNonTerminal(), leftNode, rightNode)
    newTree.level = newTree.level + 1
    getInitialTree(maxDepth, newTree)

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


    return


if __name__ == '__main__':
    main()
