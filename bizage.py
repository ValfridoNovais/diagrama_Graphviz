import streamlit as st
import graphviz as gv

# Título do aplicativo
st.title("📊 Construtor de Fluxogramas Acadêmicos")

# Inicializar o estado da sessão para armazenar elementos e conexões
if 'elements' not in st.session_state:
    st.session_state.elements = []
if 'connections' not in st.session_state:
    st.session_state.connections = []

# Função para adicionar elementos
def add_element(element_type, element_text, element_color):
    st.session_state.elements.append({
        'type': element_type,
        'text': element_text,
        'color': element_color
    })

# Função para adicionar conexões
def add_connection(from_idx, to_idx, connection_text):
    st.session_state.connections.append({
        'from': from_idx,
        'to': to_idx,
        'text': connection_text
    })

# Barra lateral para adicionar elementos
with st.sidebar:
    st.header("🔧 Ferramentas")
    
    element_type = st.selectbox(
        "Tipo de elemento:",
        options=["Início", "Atividade", "Decisão", "Documento", "Término"]
    )
    
    element_text = st.text_input("Texto do elemento:")
    element_color = st.color_picker("Cor do elemento:", "#4CAF50")
    
    if st.button("Adicionar elemento"):
        if element_text:
            add_element(element_type, element_text, element_color)
            st.success(f"Elemento '{element_text}' adicionado!")
        else:
            st.warning("Por favor, insira um texto para o elemento")

# Barra lateral para conectar elementos
with st.sidebar:
    st.header("🔗 Conectar Elementos")
    
    if len(st.session_state.elements) > 1:
        element_options = [f"{i}: {elem['text']}" for i, elem in enumerate(st.session_state.elements)]
        
        from_idx = st.selectbox(
            "De:",
            options=element_options,
            format_func=lambda x: x.split(": ")[1]
        )
        
        to_idx = st.selectbox(
            "Para:",
            options=element_options,
            format_func=lambda x: x.split(": ")[1]
        )
        
        connection_text = st.text_input("Texto da conexão:")
        
        if st.button("Conectar elementos"):
            from_idx = int(from_idx.split(":")[0])
            to_idx = int(to_idx.split(":")[0])
            add_connection(from_idx, to_idx, connection_text)
            st.success("Conexão adicionada!")
    else:
        st.warning("Adicione pelo menos 2 elementos para criar conexões")

# Renderizar o fluxograma
graph = gv.Digraph()
graph.attr('node', style='filled')

# Adicionar elementos ao gráfico
for i, element in enumerate(st.session_state.elements):
    node_attrs = {'fillcolor': element['color']}
    
    if element['type'] == "Início":
        node_attrs['shape'] = 'ellipse'
    elif element['type'] == "Atividade":
        node_attrs['shape'] = 'box'
    elif element['type'] == "Decisão":
        node_attrs['shape'] = 'diamond'
    elif element['type'] == "Documento":
        node_attrs['shape'] = 'note'
    elif element['type'] == "Término":
        node_attrs['shape'] = 'ellipse'
        node_attrs['peripheries'] = '2'
    
    graph.node(str(i), label=element['text'], **node_attrs)

# Adicionar conexões ao gráfico
for connection in st.session_state.connections:
    graph.edge(
        str(connection['from']),
        str(connection['to']),
        label=connection['text']
    )

# Mostrar o gráfico
st.graphviz_chart(graph)

# Mostrar elementos e conexões (para debug)
with st.expander("🔍 Estado Atual (Debug)"):
    st.write("Elementos:", st.session_state.elements)
    st.write("Conexões:", st.session_state.connections)

# Botão para limpar tudo
if st.button("🧹 Limpar Fluxograma"):
    st.session_state.elements = []
    st.session_state.connections = []
    st.experimental_rerun()