#!/usr/bin/env python

import os
import sys


file_name = 'data/Usair_weight.txt'
# contains all data
universe = list()



def find_file(file_name):
    cwd = os.getcwd()

    # path
    if not os.path.isdir(cwd) and \
       not os.path.isabs(cwd) and \
       not os.path.exists(cwd):
        sys.exit()
    else:
        return os.path.join(cwd, file_name)


# read file
def read_file(path):
    f = open(path, 'r')

    for each_line in f:
        arr = each_line.split()
        _link = [arr[0], arr[1]]
        universe.append(_link)

    f.close()



# main
path = find_file(file_name)
read_file(path)
print(universe)
