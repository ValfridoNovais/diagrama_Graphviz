import os
import time
from graphviz import Digraph


def build_tree(root_path, max_depth=2, exclude_dirs=None, progress_interval=100, page_size=None):
    start_time = time.time()
    processed = 0
    exclude_dirs = set(exclude_dirs or [])

    # Define engine e configura página se especificado
    # Permite escolher formato vetorial ('svg' ou 'pdf') ou raster ('png')
    kwargs = {'engine': 'sfdp', 'format': 'svg'}
    dot = Digraph('Estrutura', **kwargs)
    # Orientação L-R e configuração de layout
    dot.graph_attr.update({'rankdir': 'LR', 'ratio': 'expand', 'nodesep': '0.5', 'ranksep': '0.75'})
    dot.node_attr.update({'shape': 'folder', 'fontsize': '10'})

    # Configuração de página (ex: 'A1', 'A2')
    if page_size:
        # size em polegadas (largura,altura) e ajuste de página
        sizes = {
            'A1': '23.4,33.1!',
            'A2': '16.5,23.4!'
        }
        if page_size in sizes:
            dot.graph_attr.update({'size': sizes[page_size], 'page': sizes[page_size]})

    for dirpath, dirs, files in os.walk(root_path):
        rel = os.path.relpath(dirpath, root_path)
        depth = 0 if rel == '.' else rel.count(os.sep) + 1
        if depth > max_depth:
            dirs.clear()
            continue
        folder_name = os.path.basename(dirpath)
        if folder_name in exclude_dirs:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        parent_id = rel.replace(os.sep, '_') if rel != '.' else 'root'
        label = (os.path.basename(root_path) + '/') if rel == '.' else (folder_name + '/')
        dot.node(parent_id, label)
        processed += 1

        for d in dirs:
            child_rel = os.path.join(rel, d).replace(os.sep, '_')
            dot.node(child_rel, d + '/')
            dot.edge(parent_id, child_rel)
            processed += 1

        for f in files:
            file_rel = os.path.join(rel, f).replace(os.sep, '_')
            dot.node(file_rel, f, shape='note')
            dot.edge(parent_id, file_rel)
            processed += 1

        if processed % progress_interval == 0:
            elapsed = time.time() - start_time
            print(f'⏳ Processados {processed} nós em {elapsed:.2f}s')

    total_time = time.time() - start_time
    print(f'✅ Construção completa: {processed} nós em {total_time:.2f}s')
    return dot

if __name__ == '__main__':
    import sys
    # Argumentos: raiz, profundidade, intervalo, excluídos (CSV), página (A1/A2)
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    excludes = sys.argv[4].split(',') if len(sys.argv) > 4 else []
    page_size = sys.argv[5] if len(sys.argv) > 5 else None

    dot = build_tree(root, max_depth=max_depth, exclude_dirs=excludes, progress_interval=interval, page_size=page_size)
    render_start = time.time()
    output = dot.render(filename='estrutura_python', cleanup=True)
    render_time = time.time() - render_start

    print(f'🎉 Diagrama gerado: {output}')
    print(f'Tempo de renderização: {render_time:.2f}s')
