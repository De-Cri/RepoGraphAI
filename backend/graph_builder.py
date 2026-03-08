import networkx as nx

def build_graph(functions):
    graph = nx.DiGraph()
    for func, data in functions.items():
        graph.add_node(func)
        for call in data["calls"]:
            graph.add_edge(func, call)
    return graph