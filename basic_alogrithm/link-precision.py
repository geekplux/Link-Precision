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
    _edges = nx.non_edges(_G)
    for e in _edges:
        unknown.append(e)




def compute_auc(compute):
    auc = 0
    test_preds = compute(G, test)
    unknown_preds = compute(G, unknown)
    for u, v, test_pred in test_preds:
        print(u, v, test_pred)
        # for m, w, unknown_pred in unknown_preds:
        #     if test_pred > unknown_pred:
        #         auc += 1.0
        #     elif test_pred == unknown_pred:
        #         auc += 0.5

    return auc




def compute_precision(s, s_w):
    pass








def draw(sample_list, data_list):
    _data_list_copy = copy.deepcopy(data_list)
    for i, u in enumerate(_data_list_copy):
        if i in sample_list:
            u.append({'test': 1})

    _G = nx.Graph()
    _G.add_edges_from(_known_copy)


    etrain = [(u,v) for (u,v,d) in _G.edges(data=True) if 'test' not in d]
    etest = [(u,v) for (u,v,d) in _G.edges(data=True) if 'test' in d and d['test'] == 1]

    pos = nx.spring_layout(_G) # positions for all nodes
    nx.draw_networkx_nodes(_G, pos, node_size = 200)
    # edges
    nx.draw_networkx_edges(_G, pos, edgelist = etrain, width = 2)
    nx.draw_networkx_edges(_G, pos, edgelist = etest, width = 2, alpha = 0.5, edge_color = 'b', style = 'dashed')

    nx.draw_networkx_labels(_G, pos, font_size = 10, font_family = 'sans-serif')

    plt.axis('off')
    plt.savefig("graph.png") # save as png
    plt.show() # display




def draw_auc(x, y1, y2, y3):
    plot1 = pl.plot(x, y1, 'r', label='CN') # use pylab to plot x and y
    plot2 = pl.plot(x, y2, 'b', label='RA')
    plot3 = pl.plot(x, y3, 'y', label='PA')


    pl.title('Plot of AUC vs. random rate') # give plot a title
    pl.xlabel('random rate') # make axis labels
    pl.ylabel('AUC')
    pl.legend()

    pl.xlim(5, 20)# set axis limits
    pl.ylim(0, 20)


    pl.show()# show the plot on the screen












def show_auc_graph():
    index_list = list()
    auc_by_jc_list = list()
    auc_by_ra_list = list()
    auc_by_pa_list = list()

    i = 5
    while i <= 5:
        # get random slice of known list
        sample_list = sampling(i, known)

        # clear train, test, unknown
        train.clear()
        test.clear()

        divide(sample_list, train, test)
        generate_graph(G, train)
        get_unknown_edges(G)

        auc_by_jc = compute_auc(nx.jaccard_coefficient)
        auc_by_ra = compute_auc(nx.resource_allocation_index)
        auc_by_pa = compute_auc(nx.preferential_attachment)

        auc_by_jc_list.append(auc_by_jc)
        auc_by_ra_list.append(auc_by_ra)
        auc_by_pa_list.append(auc_by_pa)
        index_list.append(i)

        i += 5

    draw_auc(index_list, auc_by_jc_list, auc_by_ra_list, auc_by_pa_list)



def show_precision_graph(l):
    pass







# main
file_name = 'data/Usair_weight.txt'

G = nx.Graph()

universe = list() # contains all data
known = list() # contains known data
unknown = list()
train = list()
test = list()


path = find_file(file_name)
known = read_file(path)
# universe = generate_universe(known)

show_auc_graph()
# show_precision_graph(20)
# show_precision_graph(50)
# show_precision_graph(100)


#
# generate graph from origin known data
#
# sample_list = sampling(20)
# draw(sample_list)
