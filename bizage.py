import streamlit as st
import graphviz as gv
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import numpy as np

# Configuração inicial
st.set_page_config(layout="wide")
st.title("📊 MMPGProduções - Construtor de Fluxogramas Profissionais")

# Estado da sessão
if 'fluxos' not in st.session_state:
    st.session_state.fluxos = {
        'Principal': {'elements': [], 'connections': [], 'color': '#4CAF50'},
        'Secundário': {'elements': [], 'connections': [], 'color': '#2196F3'}
    }
    st.session_state.fluxo_atual = 'Principal'
    st.session_state.titulo = "Fluxograma MMPGProduções"
    st.session_state.contador_elementos = 1

# Cores para degradê
COR_INICIAL = (50, 205, 50)  # Verde claro
COR_FINAL = (0, 100, 0)       # Verde escuro

def add_element(fluxo, element_type, element_text):
    """Adiciona um novo elemento ao fluxograma"""
    element_number = st.session_state.contador_elementos
    st.session_state.fluxos[fluxo]['elements'].append({
        'type': element_type,
        'text': f"{element_number}. {element_text}",
        'id': len(st.session_state.fluxos[fluxo]['elements']),
        'number': element_number
    })
    st.session_state.contador_elementos += 1

def criar_degrade(largura, altura):
    """Cria uma imagem com degradê radial do verde claro ao escuro"""
    img = Image.new('RGB', (largura, altura))
    draw = ImageDraw.Draw(img)
    
    centro_x, centro_y = largura // 2, altura // 2
    raio_max = max(centro_x, centro_y)
    
    for y in range(altura):
        for x in range(largura):
            # Calcula a distância do centro
            distancia = np.sqrt((x - centro_x)**2 + (y - centro_y)**2)
            ratio = min(distancia / raio_max, 1.0)
            
            # Interpola as cores
            r = int(COR_INICIAL[0] + (COR_FINAL[0] - COR_INICIAL[0]) * ratio)
            g = int(COR_INICIAL[1] + (COR_FINAL[1] - COR_INICIAL[1]) * ratio)
            b = int(COR_INICIAL[2] + (COR_FINAL[2] - COR_INICIAL[2]) * ratio)
            
            draw.point((x, y), fill=(r, g, b))
    
    return img

def adicionar_logo(img):
    """Adiciona a logo MMPGProduções com degradê"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Configurações do texto
    texto = "MMPGProduções"
    try:
        fonte = ImageFont.truetype("arial.ttf", 36)
    except:
        fonte = ImageFont.load_default()
    
    # Posição no canto inferior esquerdo
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pos = (20, height - text_height - 20)
    
    # Cria máscara para o texto
    mask = Image.new('L', (text_width + 10, text_height + 10))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((5, 5), texto, font=fonte, fill=255)
    
    # Cria degradê para o texto
    degrade_texto = criar_degrade(text_width + 10, text_height + 10)
    
    # Aplica o texto com degradê
    img.paste(degrade_texto, pos, mask)
    
    return img

def adicionar_data_hora(img):
    """Adiciona data e hora no canto inferior direito"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        fonte = ImageFont.truetype("arial.ttf", 14)
    except:
        fonte = ImageFont.load_default()
    
    draw.text((width - 200, height - 30), data_hora, fill="black", font=fonte)
    return img

def renderizar_fluxograma(fluxo):
    """Renderiza o fluxograma usando Graphviz"""
    graph = gv.Digraph()
    graph.attr('graph', label=st.session_state.titulo, labelloc='t', fontsize='20')
    
    # Adiciona elementos
    for element in st.session_state.fluxos[fluxo]['elements']:
        if element['type'] == 'Processo':
            graph.node(str(element['id']), label=element['text'], shape='box', 
                      style='filled', fillcolor='lightgray')
        elif element['type'] == 'Decisão':
            graph.node(str(element['id']), label=element['text'], shape='diamond', 
                      style='filled', fillcolor='lightblue')
        elif element['type'] == 'Início/Fim':
            graph.node(str(element['id']), label=element['text'], shape='ellipse', 
                      style='filled', fillcolor='lightgreen')
    
    # Adiciona conexões
    for conn in st.session_state.fluxos[fluxo]['connections']:
        graph.edge(str(conn['from']), str(conn['to']), label=conn.get('label', ''))
    
    return graph

def exportar_fluxograma(graph, formato):
    """Exporta o fluxograma com logo e data/hora"""
    try:
        # Renderiza o gráfico no formato especificado
        graph.format = formato.lower()
        img_bytes = graph.pipe()
        
        # Converte para imagem PIL
        img = Image.open(io.BytesIO(img_bytes))
        
        # Adiciona marca d'água e informações
        img = adicionar_logo(img)
        img = adicionar_data_hora(img)
        
        # Converte de volta para bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG' if formato == 'png' else 'PDF')
        
        return img_byte_arr.getvalue()
    except Exception as e:
        st.error(f"Erro na exportação: {str(e)}")
        return None

# Layout principal
col1, col2 = st.columns([1, 3])

with col1:
    # Seção de título
    with st.expander("📝 Configurações do Documento"):
        st.session_state.titulo = st.text_input(
            "Título do trabalho:", 
            value=st.session_state.titulo
        )
    
    # Seção de adição de elementos
    with st.expander("➕ Adicionar Elemento"):
        tipo_elemento = st.selectbox(
            "Tipo de elemento:",
            ["Processo", "Decisão", "Início/Fim"],
            key="tipo_elemento"
        )
        texto_elemento = st.text_input(
            "Descrição do elemento:",
            key="texto_elemento"
        )
        if st.button("Adicionar Elemento"):
            if texto_elemento:
                add_element(st.session_state.fluxo_atual, tipo_elemento, texto_elemento)
    
    # Seção de conexões
    with st.expander("🔗 Criar Conexões"):
        if st.session_state.fluxos[st.session_state.fluxo_atual]['elements']:
            elemento_from = st.selectbox(
                "De:",
                [e['text'] for e in st.session_state.fluxos[st.session_state.fluxo_atual]['elements']],
                key="elemento_from"
            )
            elemento_to = st.selectbox(
                "Para:",
                [e['text'] for e in st.session_state.fluxos[st.session_state.fluxo_atual]['elements']],
                key="elemento_to"
            )
            label_conexao = st.text_input(
                "Rótulo da conexão (opcional):",
                key="label_conexao"
            )
            if st.button("Conectar Elementos"):
                id_from = next(e['id'] for e in st.session_state.fluxos[st.session_state.fluxo_atual]['elements'] 
                             if e['text'] == elemento_from)
                id_to = next(e['id'] for e in st.session_state.fluxos[st.session_state.fluxo_atual]['elements'] 
                           if e['text'] == elemento_to)
                st.session_state.fluxos[st.session_state.fluxo_atual]['connections'].append({
                    'from': id_from,
                    'to': id_to,
                    'label': label_conexao
                })
    
    # Seção de exportação
    with st.expander("💾 Exportar Fluxograma"):
        export_format = st.selectbox(
            "Formato de exportação:",
            ["PNG", "PDF"],
            key="export_format"
        )
        if st.button("Exportar Fluxograma"):
            graph = renderizar_fluxograma(st.session_state.fluxo_atual)
            export_data = exportar_fluxograma(graph, export_format)
            
            if export_data:
                st.success("Fluxograma exportado com sucesso!")
                st.download_button(
                    label="Baixar Fluxograma",
                    data=export_data,
                    file_name=f"fluxograma_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
                    mime="image/png" if export_format == "PNG" else "application/pdf"
                )

with col2:
    # Exibir título centralizado
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.titulo}</h1>", 
                unsafe_allow_html=True)
    
    # Visualização do fluxograma
    graph = renderizar_fluxograma(st.session_state.fluxo_atual)
    st.graphviz_chart(graph, use_container_width=True)
    
    # Lista de elementos numerados
    if st.session_state.fluxos[st.session_state.fluxo_atual]['elements']:
        st.subheader("Elementos do Fluxograma:")
        for element in st.session_state.fluxos[st.session_state.fluxo_atual]['elements']:
            st.write(f"**{element['text']}**")
