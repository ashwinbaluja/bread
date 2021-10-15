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
G.add_edge(b.Edge(bn, an))
G.add_edge(b.Edge(an, cn))
G.add_edge(b.Edge(bn, dn))
G.add_edge(b.Edge(an, dn))
G.add_edge(b.Edge(dn, en))

print("\n".join([str(x)[1:-1] for x in G.adjacency]))

print(max([len(x) for x in G.get_paths_to(G[1], G[5])]))
