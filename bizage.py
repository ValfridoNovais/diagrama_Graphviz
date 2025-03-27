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
        'Principal': {
            'elements': [], 
            'connections': [], 
            'color': '#4CAF50',
            'sections': {
                'Seção 1': {'elements': [], 'color': '#E3F2FD'},
                'Seção 2': {'elements': [], 'color': '#E8F5E9'},
                'Seção 3': {'elements': [], 'color': '#FFF3E0'},
                'Seção 4': {'elements': [], 'color': '#F3E5F5'},
                'Seção 5': {'elements': [], 'color': '#E0F7FA'}
            }
        }
    }
    st.session_state.fluxo_atual = 'Principal'
    st.session_state.titulo = "Fluxograma MMPGProduções"
    st.session_state.contador_elementos = 1

# Cores para degradê
COR_INICIAL = (50, 205, 50)  # Verde claro
COR_FINAL = (0, 100, 0)       # Verde escuro

def add_element(fluxo, element_type, element_text, section, element_color):
    """Adiciona um novo elemento ao fluxograma na seção especificada"""
    element_number = st.session_state.contador_elementos
    new_element = {
        'type': element_type,
        'text': f"{element_number}. {element_text}",
        'id': len([e for sec in st.session_state.fluxos[fluxo]['sections'].values() for e in sec['elements']]),
        'number': element_number,
        'section': section,
        'color': element_color
    }
    st.session_state.fluxos[fluxo]['sections'][section]['elements'].append(new_element)
    st.session_state.contador_elementos += 1

def criar_degrade(largura, altura):
    """Cria uma imagem com degradê radial do verde claro ao escuro"""
    img = Image.new('RGB', (largura, altura))
    draw = ImageDraw.Draw(img)
    
    centro_x, centro_y = largura // 2, altura // 2
    raio_max = max(centro_x, centro_y)
    
    for y in range(altura):
        for x in range(largura):
            distancia = np.sqrt((x - centro_x)**2 + (y - centro_y)**2)
            ratio = min(distancia / raio_max, 1.0)
            
            r = int(COR_INICIAL[0] + (COR_FINAL[0] - COR_INICIAL[0]) * ratio)
            g = int(COR_INICIAL[1] + (COR_FINAL[1] - COR_INICIAL[1]) * ratio)
            b = int(COR_INICIAL[2] + (COR_FINAL[2] - COR_INICIAL[2]) * ratio)
            
            draw.point((x, y), fill=(r, g, b))
    
    return img

def adicionar_logo(img):
    """Adiciona a logo MMPGProduções com degradê"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    texto = "MMPGProduções"
    try:
        fonte = ImageFont.truetype("arial.ttf", 36)
    except:
        fonte = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pos = (20, height - text_height - 20)
    
    mask = Image.new('L', (text_width + 10, text_height + 10))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((5, 5), texto, font=fonte, fill=255)
    
    degrade_texto = criar_degrade(text_width + 10, text_height + 10)
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

def renderizar_fluxograma(fluxo, connection_style):
    """Renderiza o fluxograma usando Graphviz com seções e estilos personalizados"""
    graph = gv.Digraph()
    graph.attr('graph', label=st.session_state.titulo, labelloc='t', fontsize='20', rankdir='TB')
    
    # Adiciona clusters para cada seção
    for section_name, section_data in st.session_state.fluxos[fluxo]['sections'].items():
        with graph.subgraph(name=f'cluster_{section_name}') as c:
            c.attr(label=section_name, style='filled', color='lightgray', 
                  fillcolor=section_data['color'], fontsize='16', rank='same')
            
            # Adiciona elementos da seção
            for element in section_data['elements']:
                if element['type'] == 'Processo':
                    c.node(str(element['id']), label=element['text'], shape='box', 
                          style='filled', fillcolor=element['color'])
                elif element['type'] == 'Decisão':
                    c.node(str(element['id']), label=element['text'], shape='diamond', 
                          style='filled', fillcolor=element['color'])
                elif element['type'] == 'Início/Fim':
                    c.node(str(element['id']), label=element['text'], shape='ellipse', 
                          style='filled', fillcolor=element['color'])
    
    # Adiciona conexões com estilo configurável
    for conn in st.session_state.fluxos[fluxo]['connections']:
        graph.edge(str(conn['from']), str(conn['to']), 
                  label=conn.get('label', ''),
                  style=connection_style,
                  penwidth='2')
    
    return graph

def exportar_fluxograma(graph, formato):
    """Exporta o fluxograma com logo e data/hora"""
    try:
        graph.format = formato.lower()
        img_bytes = graph.pipe()
        
        img = Image.open(io.BytesIO(img_bytes))
        img = adicionar_logo(img)
        img = adicionar_data_hora(img)
        
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
        secao_elemento = st.selectbox(
            "Seção:",
            list(st.session_state.fluxos[st.session_state.fluxo_atual]['sections'].keys()),
            key="secao_elemento"
        )
        cor_elemento = st.color_picker(
            "Cor do elemento:",
            value="#FFFFFF",
            key="cor_elemento"
        )
        if st.button("Adicionar Elemento"):
            if texto_elemento:
                add_element(st.session_state.fluxo_atual, tipo_elemento, texto_elemento, secao_elemento, cor_elemento)
    
    # Seção de conexões
    with st.expander("🔗 Criar Conexões"):
        all_elements = [e for sec in st.session_state.fluxos[st.session_state.fluxo_atual]['sections'].values() for e in sec['elements']]
        
        if all_elements:
            elemento_from = st.selectbox(
                "De:",
                [e['text'] for e in all_elements],
                key="elemento_from"
            )
            elemento_to = st.selectbox(
                "Para:",
                [e['text'] for e in all_elements],
                key="elemento_to"
            )
            label_conexao = st.text_input(
                "Rótulo da conexão (opcional):",
                key="label_conexao"
            )
            connection_style = st.radio(
                "Estilo da linha:",
                ['solid', 'dashed'],
                key="connection_style"
            )
            if st.button("Conectar Elementos"):
                id_from = next(e['id'] for e in all_elements if e['text'] == elemento_from)
                id_to = next(e['id'] for e in all_elements if e['text'] == elemento_to)
                st.session_state.fluxos[st.session_state.fluxo_atual]['connections'].append({
                    'from': id_from,
                    'to': id_to,
                    'label': label_conexao
                })
    
    # Seção de gerenciamento de seções
    with st.expander("📌 Gerenciar Seções"):
        for i, (section_name, section_data) in enumerate(st.session_state.fluxos[st.session_state.fluxo_atual]['sections'].items()):
            new_name = st.text_input(
                f"Nome da Seção {i+1}:",
                value=section_name,
                key=f"section_name_{i}"
            )
            if new_name != section_name:
                st.session_state.fluxos[st.session_state.fluxo_atual]['sections'][new_name] = st.session_state.fluxos[st.session_state.fluxo_atual]['sections'].pop(section_name)
            
            st.session_state.fluxos[st.session_state.fluxo_atual]['sections'][new_name]['color'] = st.color_picker(
                f"Cor da Seção {i+1}:",
                value=section_data['color'],
                key=f"section_color_{i}"
            )
    
    # Seção de exportação
    with st.expander("💾 Exportar Fluxograma"):
        export_format = st.selectbox(
            "Formato de exportação:",
            ["PNG", "PDF"],
            key="export_format"
        )
        if st.button("Exportar Fluxograma"):
            connection_style = 'solid' if st.session_state.get('connection_style') == 'solid' else 'dashed'
            graph = renderizar_fluxograma(st.session_state.fluxo_atual, connection_style)
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
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.titulo}</h1>", unsafe_allow_html=True)
    
    connection_style = 'solid' if st.session_state.get('connection_style', 'solid') == 'solid' else 'dashed'
    graph = renderizar_fluxograma(st.session_state.fluxo_atual, connection_style)
    st.graphviz_chart(graph, use_container_width=True)
    
    # Lista de elementos por seção
    for section_name, section_data in st.session_state.fluxos[st.session_state.fluxo_atual]['sections'].items():
        if section_data['elements']:
            st.subheader(f"Seção: {section_name}")
            for element in section_data['elements']:
                st.markdown(f"<div style='background-color: {element['color']}; padding: 10px; border-radius: 5px; margin: 5px 0;'><b>{element['text']}</b></div>", 
                           unsafe_allow_html=True)
