import streamlit as st
import graphviz as gv
from PIL import Image
import io

# Título do aplicativo
st.title("📊 Construtor de Fluxogramas Acadêmicos")

# Explicação do aplicativo
st.markdown("""
Crie fluxogramas profissionais utilizando os símbolos padronizados para trabalhos acadêmicos.
Adicione elementos e conecte-os para formar seu diagrama de processos.
""")

# Legenda visual dos símbolos
with st.expander("📚 LEGENDA DOS SÍMBOLOS (Clique para expandir)"):
    st.image("https://i.imgur.com/7bFNk3a.png", caption="Símbolos de Fluxograma")
    st.markdown("""
    | Símbolo | Significado | Forma no Fluxograma |
    |---------|-------------|---------------------|
    | ⬭ | Início do processo | Elipse |
    | ▯ | Atividade/processo | Retângulo |
    | ⋄ | Decisão (sim/não) | Losango |
    | ⬙ | Conexão com entidade externa | Caixa 3D |
    | ⬩ | Anotação/explicação | Texto plano |
    | ⫴ | Paralelismo | Círculo duplo |
    | ⬬ | Término do processo | Elipse dupla |
    | ⬯ | Término com link para outro processo | Elipse dupla |
    | ⏱️ | Tempo/decurso | Círculo |
    | ✉️ | Envio de mensagem | Retângulo inclinado |
    | 📄 | Emissão de documento | Nota |
    """)

# Inicializar o estado da sessão
if 'elements' not in st.session_state:
    st.session_state.elements = []
if 'connections' not in st.session_state:
    st.session_state.connections = []

# Funções auxiliares
def add_element(element_type, element_text, element_color):
    st.session_state.elements.append({
        'type': element_type,
        'text': element_text,
        'color': element_color,
        'id': len(st.session_state.elements)  # ID único
    })

def add_connection(from_id, to_id, connection_text):
    st.session_state.connections.append({
        'from': from_id,
        'to': to_id,
        'text': connection_text
    })

def delete_element(element_id):
    st.session_state.elements = [e for e in st.session_state.elements if e['id'] != element_id]
    st.session_state.connections = [
        c for c in st.session_state.connections 
        if c['from'] != element_id and c['to'] != element_id
    ]

# Barra lateral para adicionar elementos
with st.sidebar:
    st.header("🔧 FERRAMENTAS")
    
    element_type = st.selectbox(
        "Tipo de elemento:",
        options=["Início", "Atividade", "Decisão", "Documento", "Término", 
                "Término com link", "Tempo", "Mensagem", "Anotação", 
                "Conexão externa", "Paralelismo"]
    )
    
    element_text = st.text_input("Texto do elemento:")
    element_color = st.color_picker("Cor do elemento:", "#4CAF50")
    
    if st.button("➕ Adicionar elemento"):
        if element_text:
            add_element(element_type, element_text, element_color)
            st.success(f"Elemento '{element_text}' adicionado!")
        else:
            st.warning("Por favor, insira um texto para o elemento")

# Barra lateral para conectar elementos
with st.sidebar:
    st.header("🔗 CONEXÕES")
    
    if len(st.session_state.elements) > 1:
        element_options = {e['id']: f"{e['id']}: {e['text']} ({e['type']})" 
                          for e in st.session_state.elements}
        
        from_id = st.selectbox(
            "De:",
            options=list(element_options.keys()),
            format_func=lambda x: element_options[x]
        )
        
        to_id = st.selectbox(
            "Para:",
            options=list(element_options.keys()),
            format_func=lambda x: element_options[x]
        )
        
        connection_text = st.text_input("Texto da conexão:")
        
        if st.button("🔗 Conectar elementos"):
            if from_id != to_id:
                add_connection(from_id, to_id, connection_text)
                st.success("Conexão adicionada!")
            else:
                st.error("Não é possível conectar um elemento a ele mesmo")
    else:
        st.warning("Adicione pelo menos 2 elementos para criar conexões")

# Barra lateral para gerenciamento
with st.sidebar:
    st.header("⚙️ GERENCIAMENTO")
    
    if st.session_state.elements:
        element_to_delete = st.selectbox(
            "Elemento para remover:",
            options=[f"{e['id']}: {e['text']}" for e in st.session_state.elements],
            key="delete_select"
        )
        
        if st.button("🗑️ Remover elemento"):
            delete_element(int(element_to_delete.split(":")[0]))
            st.success("Elemento removido!")
            st.experimental_rerun()
    
    if st.button("🧹 Limpar tudo"):
        st.session_state.elements = []
        st.session_state.connections = []
        st.success("Fluxograma limpo!")
        st.experimental_rerun()

# Renderizar o fluxograma
graph = gv.Digraph()
graph.attr('node', style='filled', fontname='Arial', fontsize='10')

# Mapeamento de tipos para formas
shape_map = {
    "Início": ("ellipse", "#4CAF50"),
    "Atividade": ("box", "#2196F3"),
    "Decisão": ("diamond", "#FF9800"),
    "Documento": ("note", "#9C27B0"),
    "Término": ("ellipse", "#F44336"),
    "Término com link": ("ellipse", "#F44336"),
    "Tempo": ("circle", "#00BCD4"),
    "Mensagem": ("tab", "#009688"),
    "Anotação": ("plaintext", "#607D8B"),
    "Conexão externa": ("box3d", "#795548"),
    "Paralelismo": ("doublecircle", "#673AB7")
}

# Adicionar elementos ao gráfico
for element in st.session_state.elements:
    shape, default_color = shape_map[element['type']]
    node_attrs = {
        'shape': shape,
        'fillcolor': element['color'] or default_color,
        'label': element['text']
    }
    
    if element['type'] in ["Término", "Término com link"]:
        node_attrs['peripheries'] = '2'
    
    graph.node(str(element['id']), **node_attrs)

# Adicionar conexões ao gráfico
for connection in st.session_state.connections:
    graph.edge(
        str(connection['from']),
        str(connection['to']),
        label=connection['text'],
        fontsize='10'
    )

# Mostrar o gráfico
st.header("📝 SEU FLUXOGRAMA")
if st.session_state.elements:
    st.graphviz_chart(graph)
else:
    st.info("Adicione elementos para começar seu fluxograma")

# Opções de exportação
with st.sidebar:
    st.header("💾 EXPORTAR")
    export_format = st.selectbox("Formato de exportação:", ["PNG", "PDF", "SVG"])
    
    if st.button("⬇️ Exportar fluxograma"):
        if st.session_state.elements:
            try:
                graph.format = export_format.lower()
                
                # Renderizar e obter os bytes diretamente
                pdf_bytes = graph.pipe(format=export_format.lower())
                
                # Criar botão de download
                st.download_button(
                    label=f"Baixar como {export_format}",
                    data=pdf_bytes,
                    file_name=f"fluxograma_academico.{export_format.lower()}",
                    mime=f"image/{export_format.lower()}" if export_format != "PDF" else "application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao exportar: {e}")
        else:
            st.warning("Adicione elementos antes de exportar")

# Seção de informações
with st.expander("ℹ️ INSTRUÇÕES DE USO"):
    st.markdown("""
    1. **Adicione elementos** usando o menu lateral
    2. **Conecte os elementos** selecionando origem e destino
    3. **Personalize** cores e textos
    4. **Exporte** seu fluxograma quando pronto
    5. **Remova elementos** individualmente quando necessário
    
    Dica: Comece pelo elemento "Início" e termine com "Término" para um fluxograma completo!
    """)