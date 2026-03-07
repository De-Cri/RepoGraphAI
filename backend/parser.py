import ast

def parse_file(file_path):
    with open(file_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            calls = []
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name):
                    calls.append(subnode.func.id)
            functions[func_name] = {
                "file": str(file_path),
                "calls": calls
            }
    return functions