import streamlit as st
import graphviz as gv

# Configuração inicial
st.set_page_config(layout="wide")
st.title("📊 Construtor de Fluxogramas Acadêmicos Avançado")

# Estado da sessão
if 'fluxos' not in st.session_state:
    st.session_state.fluxos = {
        'Principal': {'elements': [], 'connections': [], 'color': '#4CAF50'},
        'Secundário': {'elements': [], 'connections': [], 'color': '#2196F3'}
    }
    st.session_state.fluxo_atual = 'Principal'

# Funções auxiliares
def add_element(fluxo, element_type, element_text):
    st.session_state.fluxos[fluxo]['elements'].append({
        'type': element_type,
        'text': element_text,
        'id': len(st.session_state.fluxos[fluxo]['elements'])
    })

def add_connection(fluxo, from_id, to_id, connection_text, line_type):
    st.session_state.fluxos[fluxo]['connections'].append({
        'from': from_id,
        'to': to_id,
        'text': connection_text,
        'line_type': line_type
    })

def delete_element(fluxo, element_id):
    st.session_state.fluxos[fluxo]['elements'] = [e for e in st.session_state.fluxos[fluxo]['elements'] if e['id'] != element_id]
    st.session_state.fluxos[fluxo]['connections'] = [
        c for c in st.session_state.fluxos[fluxo]['connections'] 
        if c['from'] != element_id and c['to'] != element_id
    ]

# Layout principal
col1, col2 = st.columns([1, 3])

with col1:
    st.header("⚙️ Controle")
    
    # Seleção de fluxo
    st.session_state.fluxo_atual = st.radio(
        "Fluxo ativo:",
        options=list(st.session_state.fluxos.keys()),
        horizontal=True
    )
    
    # Configurações do fluxo
    with st.expander("🎨 Configurações do Fluxo"):
        st.session_state.fluxos[st.session_state.fluxo_atual]['color'] = st.color_picker(
            f"Cor do {st.session_state.fluxo_atual.lower()}:",
            st.session_state.fluxos[st.session_state.fluxo_atual]['color']
        )
    
    # Adicionar elemento
    with st.expander("➕ Adicionar Elemento"):
        element_type = st.selectbox(
            "Tipo:",
            options=["Início", "Atividade", "Decisão", "Documento", "Término"],
            key="elem_type"
        )
        element_text = st.text_input("Texto:", key="elem_text")
        if st.button("Adicionar"):
            if element_text:
                add_element(st.session_state.fluxo_atual, element_type, element_text)
                st.success(f"Elemento adicionado ao fluxo {st.session_state.fluxo_atual}!")
            else:
                st.warning("Digite um texto para o elemento")
    
    # Conectar elementos
    with st.expander("🔗 Conectar Elementos"):
        current_fluxo = st.session_state.fluxos[st.session_state.fluxo_atual]
        if len(current_fluxo['elements']) > 1:
            element_options = {e['id']: f"{e['id']}: {e['text']}" 
                            for e in current_fluxo['elements']}
            
            from_id = st.selectbox(
                "De:",
                options=list(element_options.keys()),
                format_func=lambda x: element_options[x],
                key="from_id"
            )
            
            to_id = st.selectbox(
                "Para:",
                options=list(element_options.keys()),
                format_func=lambda x: element_options[x],
                key="to_id"
            )
            
            connection_text = st.text_input("Descrição:", key="conn_text")
            line_type = st.radio("Tipo de linha:", ["Sólida", "Tracejada"], horizontal=True)
            
            if st.button("Conectar"):
                if from_id != to_id:
                    add_connection(
                        st.session_state.fluxo_atual,
                        from_id,
                        to_id,
                        connection_text,
                        line_type
                    )
                    st.success("Conexão criada!")
                else:
                    st.error("Não pode conectar ao mesmo elemento")
        else:
            st.warning("Adicione pelo menos 2 elementos")
    
    # Gerenciamento
    with st.expander("🗑️ Gerenciar Elementos"):
        current_fluxo = st.session_state.fluxos[st.session_state.fluxo_atual]
        if current_fluxo['elements']:
            element_to_delete = st.selectbox(
                "Elemento para remover:",
                options=[f"{e['id']}: {e['text']}" for e in current_fluxo['elements']],
                key="del_element"
            )
            if st.button("Remover"):
                delete_element(
                    st.session_state.fluxo_atual,
                    int(element_to_delete.split(":")[0])
                )
                st.success("Elemento removido!")
                st.experimental_rerun()
        else:
            st.warning("Nenhum elemento para remover")
        
        if st.button("🧹 Limpar Fluxo Atual"):
            current_fluxo['elements'] = []
            current_fluxo['connections'] = []
            st.success("Fluxo limpo!")
            st.experimental_rerun()

# Área de visualização
with col2:
    st.header("📊 Visualização dos Fluxos")
    
    # Criar gráfico
    graph = gv.Digraph()
    graph.attr(compound='true')
    
    # Mapeamento de formas
    shape_map = {
        "Início": "ellipse",
        "Atividade": "box",
        "Decisão": "diamond",
        "Documento": "note",
        "Término": "ellipse"
    }
    
    # Adicionar elementos de ambos os fluxos
    for fluxo_name, fluxo_data in st.session_state.fluxos.items():
        with graph.subgraph(name=f'cluster_{fluxo_name}') as c:
            c.attr(label=fluxo_name, 
                  style='filled', 
                  color='lightgray',
                  fontcolor=fluxo_data['color'])
            
            for element in fluxo_data['elements']:
                c.node(
                    f"{fluxo_name}_{element['id']}",
                    label=element['text'],
                    shape=shape_map[element['type']],
                    fillcolor=fluxo_data['color'],
                    style='filled'
                )
    
    # Adicionar conexões
    for fluxo_name, fluxo_data in st.session_state.fluxos.items():
        for connection in fluxo_data['connections']:
            graph.edge(
                f"{fluxo_name}_{connection['from']}",
                f"{fluxo_name}_{connection['to']}",
                label=connection['text'],
                style='dashed' if connection['line_type'] == "Tracejada" else 'solid',
                color=fluxo_data['color'],
                fontcolor=fluxo_data['color']
            )
    
    # Exibir gráfico
    st.graphviz_chart(graph, use_container_width=True)
    
    # Exportação
    st.markdown("---")
    with st.expander("💾 Exportar Fluxograma"):
        export_format = st.selectbox("Formato:", ["PNG", "PDF", "SVG"])
        if st.button("Exportar"):
            try:
                graph.format = export_format.lower()
                pdf_bytes = graph.pipe()
                
                st.download_button(
                    label=f"Baixar como {export_format}",
                    data=pdf_bytes,
                    file_name=f"fluxograma.{export_format.lower()}",
                    mime=f"image/{export_format.lower()}" if export_format != "PDF" else "application/pdf"
                )
            except Exception as e:
                st.error(f"Erro na exportação: {e}")

# Legenda
with st.expander("📚 Legenda Completa"):
    col_leg1, col_leg2 = st.columns(2)
    
    with col_leg1:
        st.markdown("""
        ### Elementos
        | Símbolo | Significado |
        |---------|-------------|
        | ⬭ | Início do processo |
        | ▯ | Atividade/processo |
        | ⋄ | Decisão (sim/não) |
        | 📄 | Documento |
        | ⬬ | Término |
        """)
    
    with col_leg2:
        st.markdown("""
        ### Linhas
        | Tipo | Significado |
        |------|-------------|
        | ─── | Fluxo principal (sólido) |
        | - - - | Fluxo alternativo (tracejado) |
        | 🔵 | Fluxo Principal |
        | 🔶 | Fluxo Secundário |
        """)
