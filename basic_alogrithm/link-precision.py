#!/usr/bin/env python

import os
import sys
import random
import networkx as nx
import copy


file_name = 'data/Usair_weight.txt'

G = nx.Graph()
tG = nx.Graph()
pG = nx.Graph()

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


def draw(sample_list):
    _universe_copy = copy.deepcopy(universe)
    for i, u in enumerate(_universe_copy):
        if i in sample_list:
            u.append({'test': 1})

    G.add_edges_from(_universe_copy)

    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['test']==1]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['test']!=1]

    pos=nx.spring_layout(G) # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')

    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show() # display



def generate_graph():
    tG.add_edges_from(train_list)
    pG.add_edges_from(test_list)



# main
path = find_file(file_name)
read_file(path)
sample_list = sampling(20)
divide(sample_list)
generate_graph()
draw(sample_list)
