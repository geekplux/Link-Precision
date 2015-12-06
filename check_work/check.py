#!/usr/bin/env python

import os
import sys
import math
# import matplotlib


train_file = ''
test_file = ''
train_dict = dict()
test_dict = dict()
top_L_train_dict = dict()


def file_name(sets, num):
    return sets + '_' + num + '.txt'


def find_file_by(sets, num):
    cwd = os.getcwd()

    # path
    if not os.path.isdir(cwd) and \
       not os.path.isabs(cwd) and \
       not os.path.exists(cwd):
        sys.exit()
    else:
        return os.path.join(cwd, file_name(sets, num))


# read file
def read_file_from(path):
    f = open(path, 'r')

    file_dict = dict()

    for each_line in f:
        arr = each_line.split('\t')

        if int(arr[1]) > int(arr[2]):
            # two numbers swap
            arr[1],arr[2] = arr[2],arr[1]

        k = '-'.join([arr[1], arr[2]])

        if k in file_dict:
            file_dict[k]['time_stamp'].append(arr[0])
        else:
            file_dict[k] = dict()
            file_dict[k]['time_stamp'] = [arr[0]]

    f.close()

    return file_dict



def cal_time_interval():
    # key, value in train_dic
    for k, v in train_dict.items():
        length = len(v['time_stamp'])

        if length <= 1:
            continue
        else:
            v['interval'] = list()

        # value in train_dic['time_stamp']
        for val in v['time_stamp']:
            i = v['time_stamp'].index(val)

            # range of list
            if i == length - 1:
                break
            else:
                int_val1 = int(v['time_stamp'][i])
                int_val2 = int(v['time_stamp'][i + 1])
                # cal time interval
                sub = int_val2 - int_val1
                v['interval'].append(sub)




def cal_weight(alpha):
    cal_time_interval()

    for k, v in train_dict.items():
        # only once connect
        if 'interval' in v:
            # v['weight'] = reduce((lambda x, y: \
            #                       math.pow(x, float(alpha)) + math.pow(y, float(alpha))), \
            #                      v['interval'])
            v['weight'] = sum(map((lambda x: math.pow(x, float(alpha))),v['interval']))
        else:
            v['weight'] = 0


def sort_by_weight():
    return sorted(train_dict.items(), key=lambda x: \
                  x[1]['weight'], \
                  reverse=True)


def top_L(t, l):
    return t[0:int(l)]


def cal_matched_num():
    match_num = 0

    for v in top_L_train_dict:
        if v[0] in test_dict:
            match_num += 1

    return match_num




# MAIN
print('please input L value:  ')
L = input()
print('please input set num:  ')
num = input()

# read file
train_path = find_file_by('train', num)
test_path = find_file_by('test', num)
train_dict = read_file_from(train_path)
test_dict = read_file_from(test_path)

alpha = -2.000
while alpha <= 2.000:
    cal_weight(alpha)
    top_L_train_dict = top_L(sort_by_weight(), L)
    match_num = cal_matched_num()
    print(str(round(alpha, 3)) + ',  ' + str(int(match_num)/int(L)))
    alpha += 0.1

