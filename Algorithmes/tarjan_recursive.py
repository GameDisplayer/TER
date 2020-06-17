import networkx as nx

#visited => Preorder
#root => lowlink
#component => scc_found
#cnt => i sometimes useless to increment
#stack => queue

def strongly_connected_components_recursive(G):
    def visit(v, cnt):
        root[v] = cnt
        visited[v] = cnt
        cnt += 1
        stack.append(v)
        print("v", v)
        print("root", root)
        print("visited", visited)
        print("cnt", cnt)
        print("stack:", stack)
        print("-----------------")
        for w in G[v]:
            print("w", w)
            if w not in visited:
                print("w not in visited", w)
                yield from visit(w, cnt)
            if w not in component:
                print("w not in component", w)
                print(component)
                root[v] = min(root[v], root[w])
                print("v", v, "root[v]",root[v])
        if root[v] == visited[v]: ##scc source
            print("v", v)
            component[v] = root[v]
            print("component", component)
            tmpc = {v}  # hold nodes in this component
            print("tmpc", tmpc)
            while stack[-1] != v:
                w = stack.pop()
                component[w] = root[v]
                tmpc.add(w)
            stack.remove(v)
            yield tmpc

    visited = {}
    component = {}
    root = {}
    cnt = 0
    stack = []
    for source in G:
        print("_________________")
        print("source:", source)
        print("Visited:", visited)
        print("Component:", component)
        print("root", root)
        print("cnt:", cnt)
        print("stack:", stack)
        print("_________________")
        if source not in visited:
            print("not")
            yield from visit(source, cnt)

G = nx.DiGraph()
G.add_edges_from([(1, 3), (2, 1), (3, 2), (3, 4), (4, 5),
                    (5, 6), (6, 7), (7, 8), (8, 5)])

lensccs = [len(c) for c in sorted(strongly_connected_components_recursive(G), key=len, reverse=True)]
sccs = [tuple(sorted(c)) for c in nx.strongly_connected_components_recursive(G)]
print(lensccs)
print(sccs)
print(strongly_connected_components_recursive(G))
