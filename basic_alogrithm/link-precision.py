#!/usr/bin/env python

import os
import sys
import random
import networkx as nx
import copy
import matplotlib.pyplot as plt
import pprint


file_name = 'data/Usair_weight.txt'

G = nx.Graph()
tG = nx.Graph()
pG = nx.Graph()

# contains all data
universe = list()
train_list = list()
test_list = list()

pp = pprint.PrettyPrinter(indent=4)







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


def generate_graph():
    G.add_edges_from(universe)
    # tG.add_edges_from(train_list)
    # pG.add_edges_from(test_list)









def compute_auc(s, s_w):
    test_score = list()
    _auc_score = 0.0
    for u, v, p in s:
        for _u, _v in test_list:
            if u == _u and v == _v:
                test_score.append([u, v, p])

    for u, v, p in s_w:
        for _u, _v, _p in test_score:
            if p > _p:
                _auc_score += 0.0
            elif p < _p:
                _auc_score += 1.0
            else:
                _auc_score += 0.5


    _auc = _auc_score / (len(train_list) * len(test_list))

    return _auc


def compute_precision(s, s_w):
    pass











def jaccard_coefficient():
    _G = copy.deepcopy(G)
    jc = nx.jaccard_coefficient(_G)
    _G.remove_edges_from(test_list)
    jc_without_test_set = nx.jaccard_coefficient(_G)

    return (jc, jc_without_test_set)


def resource_allocation():
    _G = copy.deepcopy(G)
    ra = nx.resource_allocation_index(_G)
    _G.remove_edges_from(test_list)
    ra_without_test_set = nx.resource_allocation_index(_G)

    return (ra, ra_without_test_set)


def preferential_attachment():
    _G = copy.deepcopy(G)
    pa = nx.preferential_attachment(_G)
    _G.remove_edges_from(test_list)
    pa_without_test_set = nx.preferential_attachment(_G)

    return (pa, pa_without_test_set)













def draw(sample_list):
    _universe_copy = copy.deepcopy(universe)
    for i, u in enumerate(_universe_copy):
        if i in sample_list:
            u.append({'test': 1})

    _G.add_edges_from(_universe_copy)


    etrain=[(u,v) for (u,v,d) in _G.edges(data=True) if 'test' not in d]
    etest=[(u,v) for (u,v,d) in _G.edges(data=True) if 'test' in d and d['test']==1]

    pos=nx.spring_layout(_G) # positions for all nodes
    nx.draw_networkx_nodes(_G, pos, node_size=200)
    # edges
    nx.draw_networkx_edges(_G, pos, edgelist=etrain, width=2)
    nx.draw_networkx_edges(_G, pos, edgelist=etest, width=2, alpha=0.5, edge_color='b', style='dashed')

    nx.draw_networkx_labels(_G, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')
    plt.savefig("graph.png") # save as png
    plt.show() # display








# main
path = find_file(file_name)
read_file(path)


sample_list = sampling(20)
divide(sample_list)
generate_graph()
ja = jaccard_coefficient()
auc_by_ja = compute_auc(ja[0], ja[1]) # ja[1] is ja score without test set
ra = resource_allocation()
auc_by_ra = compute_auc(ra[0], ra[1]) # ra[1] is ra score without test set
pa = preferential_attachment()
auc_by_pa = compute_auc(pa[0], pa[1]) # pa[1] is pa score without test set
print(auc_by_ja, auc_by_ra, auc_by_pa)

# draw(sample_list)
