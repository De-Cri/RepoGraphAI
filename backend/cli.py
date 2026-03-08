import typer
from scanner import scan_repo
from parser import parse_file
from graph_builder import build_graph

app = typer.Typer()

@app.command()
def index(path: str):
    files = scan_repo(path)
    all_functions = {}
    for file in files:
        if file.suffix == ".py":
            funcs = parse_file(file)
            all_functions.update(funcs)
    graph = build_graph(all_functions)
    print("Nodi:", graph.nodes())
    print("Archi:", graph.edges())

if __name__ == "__main__":
    app()