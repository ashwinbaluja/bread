class Node:
    def __init__(self, name, **kwargs):
        self.attr = {}
        self.pred = []
        self.succ = []
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
    def __init__(self, start, end): 
        self.start = start
        self.end = end

class Network:
    def __init__(self):
        self.edges = []
        self.nodes = {}
        pass

    def __getitem__(self, arg):
        return self.nodes[arg]
    
    def add_node(self, node):
        self.nodes[node["name"]] = node

    def add_edge(self, edge):
        edge.end.pred.append(edge.start)
        edge.start.succ.append(edge.end)

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