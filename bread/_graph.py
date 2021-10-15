from ._network import Network, Node, Edge
from ._context import ctx
import random
import math

def dot(v, M):
    result = []
    for i in range(len(M[0])): #this loops through columns of the matrix
        total = 0
        for j in range(len(v)): #this loops through vector coordinates & rows of matrix
            total += v[j] * M[j][i]
        result.append(total)
    return result

def dot_M(m1, m2):
    return [
        [sum(x * y for x, y in zip(m1_r, m2_c)) for m2_c in zip(*m2)] for m1_r in m1
    ]

class Graph:
    def __init__(self, context=None):
        if context == None:
            self.context = ctx
        else:
            self.context = context
        self._generategraph()

    def _generategraph(self):
        G = Network()
        counter = 0
        variables = []
        for i in self.context.record:
            if "init" in i.__name__:
                G.add_node(Node(i.__name__, color=(1, 0, 0), chron=counter))
                variables.append(i.__name__)
            else:
                G.add_node(Node(i.__name__, color=(0, .3, 1), chron=counter))
            counter += 1

        l = len(self.context.record)

        colors = {}

        for i in range(l):
            lookfor = self.context.record[l - i - 1].inputs
            found = []
            for j in range(l-i - 1, 0, -1):
                for v in lookfor:
                    if v not in found and v == self.context.record[j-1].output:
                        color = hex(hash(v.name))[3:9]
                        colors[color] = v.name
                        edge = Edge(G[self.context.record[j-1].__name__], G[self.context.record[l - i - 1].__name__], color=hex(hash(v.name))[3:9], name=v.name)
                        G.add_edge(edge)
                        found.append(v)
                        if len(found) == len(lookfor):
                            continue

        past = G.adjacency
        current = dot_M(past, past)
        counter = 1
        tiers = {0:[self.context.record[-1].__name__]}
        potentials = {}
        while past != current:
            tiers[counter] = []
            if past != None:
                for i in range(len(current)):
                    #for x in range(len(current[i])):
                    if current[i][-1] == 0 and past[i][-1] == 1:
                        potentials[i] = counter
                        
            past = current
            current = dot_M(current, G.adjacency)
            counter += 1

        for i in potentials:
            if potentials[i] not in tiers:
                tiers[potentials[i]] = []
            tiers[potentials[i]].append(G.ridmap[i])
        print(tiers)

        unsortedtiers = {} 