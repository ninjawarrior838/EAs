import sys

def parse( str ):
    config = open(str, 'r')
    datafile = config.readline()
    seedT = config.readline()
    evalNums = config.readline()
    runs = config.readline()
    print seedT
    return

if len(sys.argv) >= 2:
    parse(sys.argv[-1])
else:
    parse('default.cfg')

config = open('default.cfg', 'r')
#for line in config:
    #print line
