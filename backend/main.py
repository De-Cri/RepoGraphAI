from parser import parse_file
from scanner import scan_repo


if __name__ == "__main__":
    files = scan_repo(".")
    print(files)
    all_functions={}
    for file in files:
        if file.suffix == ".py":
            funcs = parse_file(file)
            all_functions.update(funcs)
    print(all_functions)