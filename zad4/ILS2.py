import time

from zad4.MSLS import MSLS
from zad4.solution import Solution
import numpy as np


class Node():
    """docstring for Node"""
    def __init__(self,lp,ids, inpath):
        self.lp = lp
        self.id = ids
        self.dsum = 0
        self.inpath = inpath
        self.nxt = self
        self.prv = self
        self.dprv = 0
        self.dnxt = 0
    def set_nxt_prev(self, pv, nx):
        self.nxt = nx
        self.prv = pv

    def calculate_dists(self, d):
        self.dprv = d[self.id-1, self.prv.id-1]
        self.dnxt = d[self.id-1, self.nxt.id-1]
        self.dsum = self.dprv + self.dnxt
   
    def update_dist(self):
        self.dsum = self.dprv + self.dnxt

    def fprint(self):
        k = self
        return [k.lp, k.id,k.prv.id, k.nxt.id, k.dprv, k.dnxt, k.dsum]

class ILS2(MSLS):

    def __init__(self, problem, time):
        super(ILS2, self).__init__(problem)
        self.time = time
        self.set_random()
        self.nodeD = {}
        self.path = self.build_path(self.nodes)
        self.longest = []
        
        self.unused = np.setdiff1d(np.arange(1, self.p.n + 1), self.nodes)
        self.unuseD = {}
        self.distances = []
        self.ni = int(np.ceil(self.p.n / 2))
        self.nmr_dst = int(0.2*self.ni)
        self.make_node_objects()
        self.sort_dists()


    def sort_dists(self):
        for d in self.p.distances:
            sd = np.argsort(d)
            self.distances.append(sd)
        # print(self.distances)

    def make_node_objects(self):
        for i in range(len(self.nodes)): 
            node = Node(i,self.nodes[i], 1)
            self.nodeD[self.nodes[i]] = node

        for i in range(len(self.unused)): 
            node = Node(i,self.unused[i], 0)
            self.unuseD[self.unused[i]] = node

        lk = 0
        for node in self.nodeD.values():
            node.set_nxt_prev(
                self.nodeD[self.nodes[lk-1]],
                self.nodeD[self.nodes[lk+1] if lk+1 <len(self.nodes) else self.nodes[0]])

            node.calculate_dists(self.p.distances)
            lk+=1
       
    def optimize(self):
        start_time = time.time() * 1000
        best_dist = 10**10
        best_nodes = None
        self.run_algorithm()
        # print([k.fprint() for k in self.unuseD.values()], "")
        # print([k.fprint() for k in self.nodeD.values()], "")

        while True:
            
            self.remove_longest()
            self.repair()
            self.update_old()

            self.run_algorithm()
            
            if best_dist > self.dist:
                best_dist = self.dist
                best_nodes = self.nodes
            current_time = time.time() * 1000
            if current_time - start_time > self.time - 10_000:
                break
        print("TotalTime:", current_time - start_time)
        self.path = self.build_path(best_nodes)
        self.dist = self.path_distance(self.path)
        print("Best Dist: ", best_dist)

    def remove_longest(self):
        to_remove = []

        srtD = self.nodeD.values()
        srtD = sorted(srtD, key = lambda x: x.dsum, reverse = True)
        # print([k.fprint() for k in srtD], "")

        to_remove = srtD[:int(self.nmr_dst/3)]
        # print([k.fprint() for k in to_remove], "\n\n")

        for node in to_remove:
            # print(node.fprint())
            self.remove_node(node.id)
        # print("")
        while len(self.nodeD.values()) > self.ni - int(self.nmr_dst):
            longest = max(self.nodeD.values(), key = lambda x: x.dsum)
            # print(longest.fprint())
            self.remove_node(longest.id)

    def remove_node(self,k):
        node = self.nodeD[k]
        node.prv.nxt = node.nxt
        node.nxt.prv = node.prv

        node.prv.dnxt = self.p.distances[node.prv.id-1, node.nxt.id-1]
        node.nxt.dprv = self.p.distances[node.prv.id-1, node.nxt.id-1]
        node.nxt.update_dist()
        node.prv.update_dist()
        
        node.inpath = 0
        self.unuseD[k] = node
        self.nodeD.pop(k)


    def repair(self):
        dists = []
        for node in self.nodeD.values():
            nx = node.nxt
            mn_dst = 10**10
            mn_nd = None
            for i in range(5):
                
                fc = self.distances[node.id-1][i]
                if fc not in self.unuseD: continue
                
                can = self.unuseD[fc]
                dst = self.p.distances[node.id-1][can.id-1] + \
                      self.p.distances[can.id-1][nx.id -1] - \
                      node.dnxt
                if dst < mn_dst:
                    mn_dst = dst
                    mn_nd = can
            
            if mn_nd is not None:
                dists.append((mn_nd, node, mn_dst))
        
    
        dists = sorted(dists, key = lambda x: x[2])
        # print(len(self.nodeD.values()), int(self.nmr_dst))

        kj = 0
        while len(self.nodeD.values()) < self.ni:
            k = dists[kj]
            if k[0].id in self.unuseD:
                self.add_to_path(k)
            kj+=1

    def add_to_path(self, k):

        ins,node,_ = k
        ins.inpath = 1
        ins.nxt = node.nxt
        ins.dnxt = self.p.distances[ins.id-1, node.nxt.id-1]
        ins.prv = node
        ins.dprv = self.p.distances[ins.id-1, node.id-1]
        node.nxt.prv = ins
        node.nxt.dprv = self.p.distances[node.nxt.id-1, ins.id-1]
        node.nxt = ins
        node.dnxt = self.p.distances[node.id-1, ins.id-1]

        node.nxt.update_dist()
        node.update_dist()
        ins.update_dist()

        self.nodeD[ins.id] = node
        self.unuseD.pop(ins.id)


    def update_old(self):
        self.nodes = []
        for node in self.nodeD.values():
            self.nodes.append(node.id)
        
        self.unused = []
        for node in self.unuseD.values():
            self.unused.append(node.id)

