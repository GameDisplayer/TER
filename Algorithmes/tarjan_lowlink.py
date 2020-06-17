import networkx as nx
#import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import write_dot

def strongly_connected_components(G):
    preorder = {}
    lowlink = {}
    scc_found = set()
    scc_queue = []
    i = 0     # Preorder counter
    for source in G:
        print("__________________________\n")
        print("Preorder", preorder)
        print("LowLink", lowlink)
        print("Scc_found", scc_found)
        print("Scc_queue", scc_queue)
        print("Source", source)
        print("_________________________\n")
        if source not in scc_found:
            queue = [source]
            while queue:
                print("queue", queue)
                v = queue[-1]
                if v not in preorder:
                    i = i + 1
                    preorder[v] = i
                    print("Adding ", i, " in preorder at place ",v , " resulting ",  preorder)
                done = True
                print("v", v , "G[v]", G[v])
                for w in G[v]:
                    #successors
                    if w not in preorder:
                        queue.append(w)
                        print("queue app", queue)
                        done = False
                        break
                if done:
                    #on a fait le tour des voisins
                    print("\nDone")
                    print("v", v)
                    print("Lowlink before:", lowlink)
                    print("Preorder:", preorder)
                    lowlink[v] = preorder[v]
                    print("Lowlink after", lowlink)
                    for w in G[v]: #successors of w
                        print("w", w)
                        if w not in scc_found:
                            print(w, "in scc :", scc_found ,"?", w in scc_found)
                            if preorder[w] > preorder[v]:
                                print("T")
                                lowlink[v] = min([lowlink[v], lowlink[w]])
                            else:
                                print("V")
                                lowlink[v] = min([lowlink[v], preorder[w]])
                            print("new lowlink", lowlink[v])
                    queue.pop()
                    #source du scc
                    if lowlink[v] == preorder[v]:
                        print("HEY WE FOUND A SCC")
                        scc = {v}
                        while scc_queue and preorder[scc_queue[-1]] > preorder[v]:
                            k = scc_queue.pop()
                            scc.add(k)
                        scc_found.update(scc)
                        print("scc_found updated", scc_found)
                        yield scc
                    else:
                        scc_queue.append(v)
                        print("scc_queue updated", scc_queue)
                    print("\n")

        else:
            print("Source else : ", source)

G = nx.DiGraph()
G.add_edges_from([(1, 3), (2, 1), (3, 2), (3, 4), (4, 5),
                    (5, 6), (6, 7), (7, 8), (8, 5)])

# pos = nx.drawing.layout.circular_layout(G)
#
# nx.draw(G, pos=pos, with_labels=True, font_size=15,
#         node_color='yellowgreen', node_size=1000)
# plt.show()
write_dot(G, "grid.dot")
#dot -Tpng graph.dot > graph.png

lensccs = [len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
sccs = [tuple(sorted(c)) for c in strongly_connected_components(G)]
print(lensccs)
print(sccs)
print(strongly_connected_components(G))
