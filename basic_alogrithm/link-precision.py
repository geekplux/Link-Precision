#!/usr/bin/env python

import os
import sys
import random
import networkx as nx
import copy
import matplotlib.pyplot as plt
import pylab as pl
import pprint

pp = pprint.PrettyPrinter(indent = 4)





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
    data_list = []

    for each_line in f:
        arr = each_line.split()
        _link = [arr[0], arr[1]]
        data_list.append(_link)

    f.close()
    return data_list


def sampling(rate, data_list):
    l = len(data_list)
    n = int(l * rate * 0.01)
    _sample_list = random.sample(range(0, l), n)

    return sorted(_sample_list)


def divide(sample_list, _train, _test):
    for i, u in enumerate(known):
        if i not in sample_list:
            _train.append(u)
        else:
            _test.append(u)


def generate_graph(_G, edges):
    return _G.add_edges_from(edges)


def get_unknown_edges(_G):
    _unknown = list()
    _edges = nx.non_edges(_G)
    for e in _edges:
        _unknown.append(e)

    return _unknown






def compute_auc(_G, compute, _test, _unknown):
    auc = 0
    _preds = compute(_G, _unknown)
    test_preds = list()
    unknown_preds = list()

    for u, v, p in _preds:
        if [u, v] in _test or [v, u] in _test:
            test_preds.append(p)
        else:
            unknown_preds.append(p)

    for tp in test_preds:
        for up in unknown_preds:
            if tp > up:
                auc += 1.0
            elif tp == up:
                auc += 0.5

    return (auc / (len(test_preds) * len(unknown_preds)))



def by_p(n):
    return n[2]

def compute_precision(_G, compute, _test, _unknown):
    non_preds = list() # contain test and unknown
    m = 0

    _preds = compute(_G, _unknown)

    for u, v, p in _preds:
        non_preds.append([u, v, p])


    sorted_preds = sorted(non_preds, key=by_p, reverse=True)
    l = int(L)
    top_L_preds = sorted_preds[0:l]

    for n in top_L_preds:
        if [n[0], n[1]] in _test or [n[1], n[0]] in _test:
            m += 1

    return m / l








def draw_pred(predict, x, y1, y2, y3):
    plot1 = pl.plot(x, y1, 'r', label='CN') # use pylab to plot x and y
    plot2 = pl.plot(x, y2, 'b', label='RA')
    plot3 = pl.plot(x, y3, 'y', label='PA')


    pl.title('Plot of ' + predict + ' vs. random rate') # give plot a title
    pl.xlabel('random rate') # make axis labels
    pl.ylabel(predict)
    pl.legend()

    pl.xlim(4, 20)# set axis limits
    pl.ylim(0, 1)


    pl.show()# show the plot on the screen









def show_graph(predict):
    index_list = list()
    pred_by_jc_list = list()
    pred_by_ra_list = list()
    pred_by_pa_list = list()

    G = nx.Graph()
    unknown = list()
    train = list()
    test = list()

    if predict == 'AUC':
        compute = compute_auc
    else:
        compute = compute_precision

    i = 4
    while i <= 20:
        # get random slice of known list
        sample_list = sampling(i, known)

        unknown.clear()
        train.clear()
        test.clear()
        G.clear()

        divide(sample_list, train, test)
        generate_graph(G, train)
        unknown = get_unknown_edges(G)

        pred_by_jc = compute(G, nx.jaccard_coefficient, test, unknown)
        pred_by_ra = compute(G, nx.resource_allocation_index, test, unknown)
        pred_by_pa = compute(G, nx.preferential_attachment, test, unknown)

        pred_by_jc_list.append(pred_by_jc)
        pred_by_ra_list.append(pred_by_ra)
        pred_by_pa_list.append(pred_by_pa)
        index_list.append(i)

        i += 2

    draw_pred(predict, index_list, pred_by_jc_list, pred_by_ra_list, pred_by_pa_list)








# main
file_name = 'data/Usair_weight.txt'


known = list() # contains known data

path = find_file(file_name)
known = read_file(path)

print('AUC or Precision?')
s = input()
if s == 'auc':
    show_graph('AUC')
else:
    print('please input L value:  ')
    L = input()
    show_graph('Precision')










# #
# # draw graph using known data
# #
# def draw(sample_list, data_list):
#     _data_list_copy = copy.deepcopy(data_list)
#     for i, u in enumerate(_data_list_copy):
#         if i in sample_list:
#             u.append({'test': 1})

#     _G = nx.Graph()
#     _G.add_edges_from(_known_copy)


#     etrain = [(u,v) for (u,v,d) in _G.edges(data=True) if 'test' not in d]
#     etest = [(u,v) for (u,v,d) in _G.edges(data=True) if 'test' in d and d['test'] == 1]

#     pos = nx.spring_layout(_G) # positions for all nodes
#     nx.draw_networkx_nodes(_G, pos, node_size = 200)
#     # edges
#     nx.draw_networkx_edges(_G, pos, edgelist = etrain, width = 2)
#     nx.draw_networkx_edges(_G, pos, edgelist = etest, width = 2, alpha = 0.5, edge_color = 'b', style = 'dashed')

#     nx.draw_networkx_labels(_G, pos, font_size = 10, font_family = 'sans-serif')

#     plt.axis('off')
#     plt.savefig("graph.png") # save as png
#     plt.show() # display


# #
# # generate graph from origin known data
# #
# sample_list = sampling(20)
# draw(sample_list)
