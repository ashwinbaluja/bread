import networkx as nx
from ._context import ctx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from networkx.drawing.nx_pydot import graphviz_layout


class Graph:
    def __init__(self, context=None):
        if context == None:
            self.context = ctx
        else:
            self.context = context
        self._generategraph()

    def _generategraph(self):
        G = nx.DiGraph()
        counter = 0
        variables = []

        for i in self.context.record:
            if "init" in i.__name__:
                G.add_node(i.__name__, color=(1, 0, 0), chron=counter)
                variables.append(i.__name__)
            else:
                G.add_node(i.__name__, color=(0, .3, 1), chron=counter)
            counter += 1
        #connections by function inputs and outputs
        colors = {}
        l = len(self.context.record)
        root = self.context.record[-1].__name__

        G.nodes[root]['color']=[0,1,0]
        for i in range(l):
            lookfor = self.context.record[l - i - 1].inputs
            print(lookfor)
            found = []
            for j in range(l-i - 1, 0, -1):
                for v in lookfor:
                    if v not in found and v == self.context.record[j-1].output:
                        color = hex(hash(v.name))[3:9]
                        colors[color] = v.name
                        G.add_edge(self.context.record[j-1].__name__, self.context.record[l - i - 1].__name__, color=hex(hash(v.name))[3:9], name=v.name)
                        found.append(v)
                        if len(found) == len(lookfor):
                            continue
        unsortedtiers = {} 

        #tiers by depth
        #a = nx.shortest_path_length(G.reverse(copy=False),root)
        for node in [x for x in G.nodes if x != root]:

            paths = nx.all_simple_paths(G, node, root)
            length = max([len(x) for x in paths])
            if length in unsortedtiers:
                unsortedtiers[length].append(node)
            else:
                unsortedtiers[length] = [node]

        unsortedtiers[0] = [root]
        tiers = {} 
        maxdepth = max([x for x in unsortedtiers])
        for i in range(maxdepth + 1):
            if i in unsortedtiers:
                tiers[i] = unsortedtiers[i]
            else:
                tiers[i] = []
        #attemps to keep chains of functions ontop of eachother

        print(tiers)

        for i in [x for x in tiers][:-1]:
            for ind in range(len(tiers[i])):
                x = tiers[i][ind]
                if x == None:
                    continue
                successors = [succ for succ in G.predecessors(x)]
                print(x, successors)
                #print(x, [succ for succ in G.successors(x)])
                succIndex = [tiers[i + 1].index(succ) for succ in successors if succ in tiers[i+1]]

                sharedSuccIndex = [tiers[i].index(succ) for succ in successors if succ in tiers[i]]

                if len(sharedSuccIndex) > 0 and (sharedSuccIndex != ind + 1 or sharedSuccIndex != ind - 1):
                    print(sharedSuccIndex, ind, x)

                    if not ind + 1 >= len(tiers[i]):
                        c = tiers[i][ind+1]
                        tiers[i][ind+1] = tiers[i][sharedSuccIndex[0]]
                        tiers[i][sharedSuccIndex[0]] = c

                    else:
                        c = tiers[i][ind-1]
                        tiers[i][ind-1] = tiers[i][sharedSuccIndex[0]]
                        tiers[i][sharedSuccIndex[0]] = c

                if succIndex != ind and len(succIndex) > 0:
                    if not ind >= len(tiers[i+1]):
                        c = tiers[i+1][ind]
                        tiers[i+1][ind] = tiers[i+1][succIndex[0]] 
                        tiers[i+1][succIndex[0]] = c
                    else:
                        tiers[i+1] += [None] * (ind-len(tiers[i+1]) + 1)
                        c = tiers[i+1][ind]
                        tiers[i+1][ind] = tiers[i+1][succIndex[0]] 
                        tiers[i+1][succIndex[0]] = c

        #positions in tiers

        for i in [x for x in tiers][:-1]:
            print(i)
            for ind in range(len(tiers[i])):
                x = tiers[i][ind]
                for j in range(0, i):
                    #print(j, i)
                    pass



        G.remove_nodes_from(list(nx.isolates(G)))

        pos = {}
        maxwidth = max([len(tiers[x]) for x in tiers])
        maxdepth = len(tiers)
        for i in tiers:
            for x in range(len(tiers[i])):
                #x +  + ((x - len(tiers[i])) * i/len(tiers))
                #pos[tiers[i][x]] = (maxwidth / (len(tiers[i]) + 1) + x - (len(tiers[i])/maxwidth), i)#+ (x/(i + 1)))
                if tiers[i][x] is not None:
                    pos[tiers[i][x]] = (x, i)
                    #pos[tiers[i][x]] = (x, i + (x % 2 * .1))#+ (x/(i + 1)))
                    #pos[tiers[i][x]] = (x, G.nodes[tiers[i][x]]['chron'])

        for i in tiers:
            print(tiers[i])

        nodecolors = nx.get_node_attributes(G,'color')
        plt.rcParams["figure.figsize"] = (10,10)
        nodecolorlist = [nodecolors[x] for x in nodecolors]

        edgecolors = nx.get_edge_attributes(G,'color')
        
        edgecolorlist = ["#" + str(edgecolors[x]) for x in edgecolors]

        #pos = graphviz_layout(G, prog="dot")
        #pos = nx.drawing.layout.spring_layout(G, iterations=1000)
        #pos = nx.drawing.layout.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos=pos, node_shape="s", node_color = nodecolorlist)
        nx.draw_networkx_edge_labels(G, pos=pos, clip_on=False, label_pos=.4, font_size=7, edge_labels=nx.get_edge_attributes(G, "name"))
        nx.draw_networkx_labels(G, pos=pos, font_size=10)
        nx.draw_networkx_edges(G, pos=pos, arrowsize=15, arrowstyle="fancy",edge_color=edgecolorlist)

        patches = [] 
        for i in colors:
            patches.append(mpatches.Patch(color = "#" + str(i), label=colors[i]))
        plt.legend(handles=patches)
        plt.savefig("simple_path2.png", bbox_inches='tight', dpi=400) # save as png