import ast
from typing import List, Dict


def extract_functions(source: str) -> List[Dict]:
    """Extrai funções top-level de um código-fonte Python e retorna uma lista com
    dicionários contendo: name, args (lista), docstring e source_code.
    """
    tree = ast.parse(source)
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            try:
                source_segment = ast.get_source_segment(source, node) or ''
            except Exception:
                source_segment = ''
            functions.append({
                'name': node.name,
                'args': [a.arg for a in node.args.args],
                'docstring': ast.get_docstring(node),
                'source': source_segment
            })
    return functions


def file_path_to_module(path: str) -> str:
    """Converte um caminho relativo (ex: examples/add.py) para import path (examples.add).
    Se estiver na raiz (add.py) retorna apenas 'add'."""
    import os
    path = path.replace('\\', '/')
    if path.endswith('.py'):
        path = path[:-3]
    parts = [p for p in path.split('/') if p and p != '.']
    return '.'.join(parts)