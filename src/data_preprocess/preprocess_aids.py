import sys

sys.path.append('..')
from utils import get_root_path, exec, get_file_base_id
import networkx as nx
from glob import glob
from collections import defaultdict
import random
from random import sample

random.seed(123)


def gen_aids():
    dirin = get_root_path() + '/data'
    file = dirin + '/AIDO99SD'
    dirout = dirin + '/AIDS'
    g = nx.Graph()
    line_i = 0
    gid = 0
    aids_old_ids = get_old_aids_id()
    charges = set()
    charge_gids = set()
    with open(file) as f:
        for line in f:
            if '$$$$' in line:
                print(gid)
                nx.write_gexf(g, dirout + '/{}.gexf'.format(gid))
                g = nx.Graph(gid=gid)
                line_i = 0
                gid += 1
            else:
                if gid == 40650:
                    print(line, end='')
                ls = line.rstrip().split()
                if len(ls) == 9:
                    nid = line_i - 4
                    ls = line.rstrip().split()
                    type = ls[3]
                    charge = int(ls[6])
                    # if charge != 0:
                    #     print(gid)
                    #     if (gid + 1) in aids_old_ids:
                    #         print('#####'*20)
                    if charge != 0:
                        charges.add((type, charge))
                        charge_gids.add(gid)
                    if charge == 1:
                        charge = 3
                    elif charge == 2:
                        charge = 2
                    elif charge == 3:
                        charge = 1
                    elif charge == 4:
                        raise RuntimeError('Cannot handle doublet radical')
                    elif charge == 5:
                        charge = -1
                    elif charge == 6:
                        charge = -2
                    elif charge == 7:
                        charge = -3
                    elif charge != 0:
                        raise RuntimeError(
                            'Unrecognized charge {}'.format(charge))
                    if type != 'H':
                        g.add_node(nid, type=type)
                elif len(ls) == 6:
                    ls = line.rstrip().split()
                    nid0 = int(ls[0]) - 1
                    nid1 = int(ls[1]) - 1
                    valence = int(ls[2])
                    if nid0 in g.nodes() and nid1 in g.nodes():
                        g.add_edge(nid0, nid1, valence=valence)
                line_i += 1
    print(len(charges), charges)
    print(len(charge_gids), charge_gids)


def get_old_aids_id():
    files = glob(get_root_path() + '/data/AIDS_old/data/*.gxl')
    return [get_file_base_id(file) for file in files]

def gen_aids10k():
    datadir = get_root_path() + '/data'
    dirin = datadir + '/AIDS'
    graphs = {}
    nodes_graphs = defaultdict(list)
    lesseq30 = set()
    disconnects = set()
    for file in glob(dirin + '/*.gexf'):
        gid = int(file.split('/')[-1].split('.')[0])
        g = nx.read_gexf(file)
        if not nx.is_connected(g):
            print('{} not connected'.format(gid))
            disconnects.add(gid)
            continue
        graphs[gid] = g
        nodes_graphs[g.number_of_nodes()].append(gid)
        if g.number_of_nodes() <= 30:
            lesseq30.add(gid)
    print(len(disconnects), disconnects)
    # exit(1)
    # print(nodes_graphs[222])
    # print(nodes_graphs[2])
    train_dir = '{}/AIDS10k/train'.format(datadir)
    test_dir = '{}/AIDS10k/test'.format(datadir)
    exec('mkdir -p {}'.format(train_dir))
    exec('mkdir -p {}'.format(test_dir))
    for num_node in range(5, 23):
        choose = sample(nodes_graphs[num_node], 1)[0]
        print('choose {} with {} nodes'.format(choose, num_node))
        nx.write_gexf(graphs[choose], test_dir + '/{}.gexf'.format(choose))
        lesseq30.remove(choose)
    for tid in sample(lesseq30, 10000):
        nx.write_gexf(graphs[tid], train_dir + '/{}.gexf'.format(tid))
    print('Done')


gen_aids10k()
