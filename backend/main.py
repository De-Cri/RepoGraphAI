from parser import parse_file
from scanner import scan_repo
from graph_builder import build_graph

if __name__ == "__main__":
    files = scan_repo(".")
    all_functions={}
    for file in files:
        if file.suffix == ".py":
            funcs = parse_file(file)
            all_functions.update(funcs)
    #print(all_functions)
    graph = build_graph(all_functions)
    print("Nodes:", graph.nodes())
    print("Edges:", graph.edges())
    
    