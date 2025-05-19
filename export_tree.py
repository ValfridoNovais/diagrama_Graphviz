import os
import time
from graphviz import Digraph

def build_tree(root_path, max_depth=2, exclude_dirs=None, progress_interval=100, page_size=None, font_size='10', output_format='svg', layout_engine='circo'):
    """
    Gera um diagrama de estrutura de pastas em layout circular usando o Graphviz 'circo'.
    """
    start_time = time.time()
    processed = 0
    exclude_dirs = set(exclude_dirs or [])

    # Cria grafo com engine circo para layout circular
    dot = Digraph('Estrutura', format=output_format, engine=layout_engine)
    dot.graph_attr.update({
        'nodesep': '0.5',    # espaçamento entre nós
        'ranksep': '0.75',   # espaçamento entre níveis (ainda válido para circo)
        'overlap': 'false',  # evita sobreposição de nós
        'splines': 'true'    # arestas curvas
    })
    dot.node_attr.update({
        'shape': 'folder',
        'fontsize': font_size,
        'margin': '0.1,0.05'
    })

    # Ajuste de página se necessário
    if page_size:
        sizes = {'A1': '23.4,33.1!', 'A2': '16.5,23.4!'}
        if page_size in sizes:
            dot.graph_attr.update({'size': sizes[page_size], 'page': sizes[page_size]})

    # Percorre diretórios e cria nós e arestas
    for dirpath, dirs, files in os.walk(root_path):
        rel = os.path.relpath(dirpath, root_path)
        depth = 0 if rel == '.' else rel.count(os.sep) + 1
        if depth > max_depth:
            dirs.clear()
            continue
        folder = os.path.basename(dirpath)
        if folder in exclude_dirs:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        parent_id = rel.replace(os.sep, '_') if rel != '.' else 'root'
        label = folder + '/' if rel != '.' else os.path.basename(root_path) + '/'
        dot.node(parent_id, label)
        processed += 1

        # Conecta subpastas radialmente
        for d in dirs:
            child_rel = os.path.join(rel, d).replace(os.sep, '_')
            dot.node(child_rel, d + '/')
            dot.edge(parent_id, child_rel)
            processed += 1

        # Conecta arquivos radialmente
        for f in files:
            file_id = os.path.join(rel, f).replace(os.sep, '_')
            dot.node(file_id, f, shape='note', fontsize=font_size)
            dot.edge(parent_id, file_id)
            processed += 1

        if processed % progress_interval == 0:
            elapsed = time.time() - start_time
            print(f'⏳ Processados {processed} nós em {elapsed:.2f}s')

    total_time = time.time() - start_time
    print(f'✅ Construção completa: {processed} nós em {total_time:.2f}s')
    return dot

if __name__ == '__main__':
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    excludes = sys.argv[4].split(',') if len(sys.argv) > 4 else []
    page_size = sys.argv[5] if len(sys.argv) > 5 else None
    font_size = sys.argv[6] if len(sys.argv) > 6 else '10'
    output_format = sys.argv[7] if len(sys.argv) > 7 else 'png'
    layout_engine = sys.argv[8] if len(sys.argv) > 8 else 'circo'

    dot = build_tree(
        root_path=root,
        max_depth=max_depth,
        exclude_dirs=excludes,
        progress_interval=interval,
        page_size=page_size,
        font_size=font_size,
        output_format=output_format,
        layout_engine=layout_engine
    )
    render_start = time.time()
    output = dot.render(filename='estrutura_python', cleanup=True)
    render_time = time.time() - render_start
    print(f'🎉 Diagrama gerado: {output}')
    print(f'Tempo de renderização: {render_time:.2f}s')
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    excludes = sys.argv[4].split(',') if len(sys.argv) > 4 else []
    page_size = sys.argv[5] if len(sys.argv) > 5 else None
    font_size = sys.argv[6] if len(sys.argv) > 6 else '10'
    output_format = sys.argv[7] if len(sys.argv) > 7 else 'svg'
    layout_engine = sys.argv[8] if len(sys.argv) > 8 else 'twopi'

    dot = build_tree(
        root_path=root,
        max_depth=max_depth,
        exclude_dirs=excludes,
        progress_interval=interval,
        page_size=page_size,
        font_size=font_size,
        output_format=output_format,
        layout_engine=layout_engine
    )
    render_start = time.time()
    output = dot.render(filename='estrutura_python', cleanup=True)
    render_time = time.time() - render_start
    print(f'🎉 Diagrama gerado: {output}')
    print(f'Tempo de renderização: {render_time:.2f}s')
