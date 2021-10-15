class Node:
    def __init__(self, name, **kwargs):
        self.attr = {}
        self.attr["name"] = name
        for i in kwargs:
            self.attr[i] = kwargs[i]

    def __str__(self):
        if "name" in self.attr:
            return "Node:" + str(self.attr["name"])
        else:
            return "Node:" + str(id(self))

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, arg):
        return self.attr[arg]

class Edge:
    def __init__(self, start, end, **kwargs): 
        self.attr = {}
        for i in kwargs:
            self.attr[i] = kwargs[i]
        self.start = start
        self.end = end

class Network:
    def __init__(self):
        self.nodeid = 0
        self.edges = []
        self.nodes = {}
        self.adjacency = []
        self.idmap = {}
        self.ridmap = {}
        pass

    def __getitem__(self, arg):
        return self.nodes[arg]
    
    def __str__(self):
        return "\n".join([str(x)[1:-1] for x in self.adjacency]).replace(",", "")

    def add_node(self, node):
        self.ridmap[self.nodeid] = node['name']
        self.idmap[node['name']] = self.nodeid
        self.nodeid += 1
        self.nodes[node['name']] = node
        self.update_adjacency()

    def add_edge(self, edge):
        self.adjacency[self.idmap[edge.start['name']]][self.idmap[edge.end['name']]] = 1

    def get_paths_to(self, start, end, path=None, temp=None):
        if path == None:
            path = []
        if temp == None:
            temp = []

        for i in start.succ: 
            print(start, i, start.succ, temp)
            z = [x for x in temp] 
            z.append(i)
            if i == end:
                path.append(z)
            else:
                self.get_paths_to(i, end, path, z)

        return path

    def update_adjacency(self):
        length = 1
        for i in self.adjacency: 
            i.append(0)
            length = len(i)

        self.adjacency.append([0] * length)

