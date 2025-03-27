import streamlit as st
import graphviz as gv
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
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

# Funções auxiliares
def criar_degrade(largura, altura):
    img = Image.new('RGB', (largura, altura))
    draw = ImageDraw.Draw(img)
    
    for y in range(altura):
        for x in range(largura):
            distancia = np.sqrt((x - largura/2)**2 + (y - altura/2)**2)
            max_dist = np.sqrt((largura/2)**2 + (altura/2)**2)
            ratio = distancia / max_dist
            r = int(34 + 221 * ratio)
            g = int(139 + 116 * ratio)
            b = int(34 + 221 * ratio)
            draw.point((x, y), fill=(r, g, b))
    
    return img

def add_element(fluxo, element_type, element_text):
    element_number = st.session_state.contador_elementos
    st.session_state.fluxos[fluxo]['elements'].append({
        'type': element_type,
        'text': f"{element_number}. {element_text}",
        'id': len(st.session_state.fluxos[fluxo]['elements']),
        'number': element_number
    })
    st.session_state.contador_elementos += 1

# (Manter as outras funções auxiliares anteriores)

# Layout principal
col1, col2 = st.columns([1, 3])

with col1:
    # Seção de título
    with st.expander("📝 Configurações do Documento"):
        st.session_state.titulo = st.text_input(
            "Título do trabalho:", 
            value=st.session_state.titulo
        )
        
    # (Manter o restante do painel de controle anterior)

with col2:
    # Exibir título centralizado
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.titulo}</h1>", 
                unsafe_allow_html=True)
    
    # (Manter a visualização do gráfico anterior)

# Função de exportação modificada
def exportar_com_logo(graph, export_format):
    try:
        graph.format = export_format.lower()
        pdf_bytes = graph.pipe()
        
        # Converter para imagem PIL
        img = Image.open(io.BytesIO(pdf_bytes))
        
        # Adicionar marca d'água com degrade
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Criar overlay com degrade
        overlay = criar_degrade(width, height)
        overlay = overlay.convert("RGBA")
        overlay.putalpha(128)
        
        # Combinar com a imagem original
        img = Image.alpha_composite(img.convert("RGBA"), overlay)
        
        # Adicionar texto da logo
        fonte = ImageFont.truetype("arial.ttf", 36)
        texto = "MMPGProduções"
        bbox = draw.textbbox((0,0), texto, font=fonte)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Posicionar no canto inferior esquerdo
        pos = (20, height - text_height - 20)
        
        # Adicionar texto com degrade
        mask = Image.new('L', (text_width, text_height))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.text((0,0), texto, font=fonte, fill=255)
        
        degrade = criar_degrade(text_width, text_height)
        img.paste(degrade, pos, mask)
        
        # Adicionar data/hora
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        draw.text((width-250, height-30), data_hora, fill=(0,0,0), font=ImageFont.truetype("arial.ttf", 14))
        
        # Converter para bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        
        return img_byte_arr.getvalue()
    
    except Exception as e:
        st.error(f"Erro na exportação: {str(e)}")
        return None

# (Atualizar a seção de exportação para usar a nova função)
