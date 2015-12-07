#!/usr/bin/env python

import os
import sys
import random
import networkx as nx
import copy
import matplotlib.pyplot as plt
import pylab as pl
import pprint


file_name = 'data/Usair_weight.txt'

G = nx.Graph()
# tG = nx.Graph()
# pG = nx.Graph()

# contains all data
universe = list()
known = list()
unknown = list()
train = list()
test = list()

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
        known.append(_link)

    f.close()


def sampling(rate):
    l = len(known)
    n = int(l * rate * 0.01)
    _list = random.sample(range(0, l), n)

    return sorted(_list)


def divide(sample_list):
    for i, u in enumerate(known):
        if i not in sample_list:
            train.append(u)
        else:
            test.append(u)


def generate_graph():
    G.add_edges_from(known)
    # tG.add_edges_from(train)
    # pG.add_edges_from(test)




def get_universe(nodes):
    _node_list = list()
    _node_list_copy = list()

    for n in nodes:
        _node_list.append(n)
        _node_list_copy.append(n)

    i_node_list = iter(_node_list)
    i_node_list_copy = iter(_node_list_copy)

    for n in i_node_list:
        for m in i_node_list_copy:
            if n != m and ([n, m] not in universe or [m, n] not in universe):
                universe.append([n, m])




def get_unknown():
    i_u = iter(universe)

    for u in i_u:
        if ([u[0], u[1]] not in train or [u[1], u[0]] not in train) and \
           ([u[0], u[1]] not in test or [u[1], u[0]] not in test):
            unknown.append(u)




def compute_auc(s):
    _ja = s[0]
    _g_nodes = s[1]
    _g_edges = s[2]


    get_universe(_g_nodes)
    get_unknown()

    test_score_list = list()
    unknown_score_list = list()


    i_test = iter(test)
    i_unknow = iter(unknown)

    for u, v, p in _ja:
        for t in i_test:
            if [u, v] in t or [v, u] in t:
                test_score_list.append([u, v, p])
        for k in i_unknow:
            if [u, v] in k or [v, u] in k:
                unknown_score_list.append([u, v, p])


    _auc_score = 0.0

    i_test_score_list = iter(test_score_list)
    i_unknown_score_list = iter(unknown_score_list)
    for u, v, p in i_unknown_score_list:
        for _u, _v, _p in i_test_score_list:
            if p > _p:
                _auc_score += 0.0
            elif p < _p:
                _auc_score += 1.0
            else:
                _auc_score += 0.5


    _auc = _auc_score / (len(unknown) * len(test))

    return _auc


def compute_precision(s, s_w):
    pass











def jaccard_coefficient():
    _G = copy.deepcopy(G)
    _G.remove_edges_from(test)
    jc = nx.jaccard_coefficient(_G)

    return (jc, _G.nodes_iter(), _G.edges_iter())


def resource_allocation():
    _G = copy.deepcopy(G)
    _G.remove_edges_from(test)
    ra = nx.resource_allocation_index(_G)

    return (ra, _G.nodes_iter(), _G.edges_iter())


def preferential_attachment():
    _G = copy.deepcopy(G)
    _G.remove_edges_from(test)
    pa = nx.preferential_attachment(_G)

    return (pa, _G.nodes_iter(), _G.edges_iter())













def draw(sample_list):
    _known_copy = copy.deepcopy(known)
    for i, u in enumerate(_known_copy):
        if i in sample_list:
            u.append({'test': 1})

    _G = nx.Graph()
    _G.add_edges_from(_known_copy)


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
    auc_by_ja_list = list()
    auc_by_ra_list = list()
    auc_by_pa_list = list()
    i = 5
    while i <= 10:
        sample_list = sampling(i)
        train.clear()
        test.clear()
        divide(sample_list)
        generate_graph()

        ja = jaccard_coefficient()
        auc_by_ja = compute_auc(ja)
        ra = resource_allocation()
        auc_by_ra = compute_auc(ra)
        pa = preferential_attachment()
        auc_by_pa = compute_auc(pa)

        auc_by_ja_list.append(auc_by_ja)
        auc_by_ra_list.append(auc_by_ra)
        auc_by_pa_list.append(auc_by_pa)
        index_list.append(i)

        i += 5

    draw_auc(index_list, auc_by_ja_list, auc_by_ra_list, auc_by_pa_list)



def show_precision_graph(l):
    pass







# main
path = find_file(file_name)
read_file(path)

show_auc_graph()
# show_precision_graph(20)
# show_precision_graph(50)
# show_precision_graph(100)

# sample_list = sampling(20)
# draw(sample_list)
