#!/usr/bin/env python

import os
import sys
import random


file_name = 'data/Usair_weight.txt'

# contains all data
universe = list()
train_list = list()
test_list = list()


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


def sampling(rate):
    l = len(universe)
    n = int(l * rate * 0.01)
    _list = random.sample(range(0, l), n)

    return sorted(_list)


def divide(sample_list):
    for i, u in enumerate(universe):
        if i not in sample_list:
            train_list.append(u)
        else:
            test_list.append(u)




# main
path = find_file(file_name)
read_file(path)
sample_list = sampling(20)
divide(sample_list)
