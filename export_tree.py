import os
import time
from graphviz import Digraph


def build_tree(root_path, progress_interval=100):
    # Inicia temporizador
    start_time = time.time()
    processed = 0

    # Cria o grafo com orientação esquerda-direita
    # Usa engine otimizado para grandes grafos (sfdp é mais rápido que dot)
    dot = Digraph('Estrutura', format='png', engine='sfdp')
    # Ajusta atributos de grafo e nós corretamente via dicionários internos
    dot.graph_attr.update({'rankdir': 'LR'})
    dot.node_attr.update({'shape': 'folder'})

    # Percorre recursivamente as pastas
    for dirpath, dirs, files in os.walk(root_path):
        # Gera ID único baseado em caminho relativo
        rel = os.path.relpath(dirpath, root_path)
        parent_id = rel.replace(os.sep, '_') if rel != '.' else 'root'
        # Define rótulo: nome da pasta (root ganha nome da raiz)
        label = (os.path.basename(root_path) + '/') if rel == '.' else (os.path.basename(dirpath) + '/')
        dot.node(parent_id, label)
        processed += 1

        # Adiciona subpastas
        for d in dirs:
            child_rel = os.path.join(rel, d).replace(os.sep, '_')
            dot.node(child_rel, d + '/')
            dot.edge(parent_id, child_rel)
            processed += 1

        # Adiciona arquivos
        for f in files:
            file_rel = os.path.join(rel, f).replace(os.sep, '_')
            dot.node(file_rel, f, shape='note')
            dot.edge(parent_id, file_rel)
            processed += 1

        # Exibe progresso a cada X elementos processados
        if processed % progress_interval == 0:
            elapsed = time.time() - start_time
            print(f'⏳ Processados {processed} nós em {elapsed:.2f}s')

    # Progresso final da construção do grafo
    total_time = time.time() - start_time
    print(f'✅ Construção do grafo completa: {processed} nós em {total_time:.2f}s')
    return dot, total_time


if __name__ == '__main__':
    import sys
    # Raiz padrão: diretório atual ou argumento
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    # Intervalo de progresso opcional via segundo argumento
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    # Build do grafo
    dot, build_time = build_tree(root, progress_interval=interval)

    # Timer para renderização
    render_start = time.time()
    output_file = dot.render(filename='estrutura_python', cleanup=True)
    render_time = time.time() - render_start

    # Relatório final completo
    print(f'🎉 Diagrama gerado: {output_file}')
    print(f'Tempo de construção: {build_time:.2f}s, tempo de renderização: {render_time:.2f}s')
