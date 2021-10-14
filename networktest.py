import bread as b 

G = b.Network()
"""
for i in range(1, 10, 2):
    node = b.Node(i)
    node2 = b.Node(i+1)
    G.add_node(node)
    G.add_node(node2)
    G.add_edge(b.Edge(node, node2))
    if i > 1:
        print(G[i-1], node)
        G.add_edge(b.Edge(G[i-1], node))
"""
an = b.Node(1)
bn = b.Node(2)
cn = b.Node(3)
dn = b.Node(4)

en = b.Node(5)

G.add_node(an)
G.add_node(bn)
G.add_node(cn)
G.add_node(dn)
G.add_node(en)


G.add_edge(b.Edge(an, bn))
G.add_edge(b.Edge(an, cn))

G.add_edge(b.Edge(bn, dn))

G.add_edge(b.Edge(an, dn))

print(G[4])

print(G.get_paths_to(G[1], G[4]))