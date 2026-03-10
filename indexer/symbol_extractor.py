import json
import re

def tokenize(s):
    parts = re.split(r"[^A-Za-z0-9]+", s)
    camel_parts = re.findall(r"[A-Z][^A-Z]*", s)
    return [p.lower() for p in parts + camel_parts if p]

def _matches(query_tokens, *parts):
    if not query_tokens:
        return True
    for part in parts:
        if not part:
            continue
        lower_part = part.lower()
        for q in query_tokens:
            if q in lower_part:
                return True
    return False

def _token_overlap(query_tokens, candidate_tokens):
    for q in query_tokens:
        for c in candidate_tokens:
            if c in q or q in c:
                return True
    return False


def symbol_extractor(query: str, parsed_json: str):
    tokens = set(tokenize(query)) if query else set()
    data = json.loads(parsed_json)
    files = data.get("parsed_repo", {}).get("files", {})

    symbol_map = {}

    for file_name, file_data in files.items():
        file_tokens = set(tokenize(file_name))
        file_match = _token_overlap(tokens, file_tokens)

        functions = file_data.get("functions", {})
        for function_name in functions.keys():
            if file_match or _matches(tokens, function_name):
                file_bucket = symbol_map.setdefault(file_name, {})
                file_bucket.setdefault("functions", []).append(function_name)

        classes = file_data.get("classes", {})
        for class_name, class_data in classes.items():
            methods = class_data.get("methods", {})
            for method_name in methods.keys():
                if file_match or _matches(tokens, method_name):
                    file_bucket = symbol_map.setdefault(file_name, {})
                    classes_bucket = file_bucket.setdefault("classes", {})
                    class_bucket = classes_bucket.setdefault(class_name, {})
                    class_bucket.setdefault("methods", []).append(method_name)

    ordered_map = {}
    for file_name in sorted(symbol_map.keys()):
        file_data = symbol_map[file_name]
        ordered_file = {}

        if "functions" in file_data:
            ordered_file["functions"] = sorted(set(file_data["functions"]))

        if "classes" in file_data:
            classes_ordered = {}
            for class_name in sorted(file_data["classes"].keys()):
                class_data = file_data["classes"][class_name]
                class_ordered = {}
                if "methods" in class_data:
                    class_ordered["methods"] = sorted(set(class_data["methods"]))
                if class_ordered:
                    classes_ordered[class_name] = class_ordered
            if classes_ordered:
                ordered_file["classes"] = classes_ordered

        if ordered_file:
            ordered_map[file_name] = ordered_file

    return ordered_map
