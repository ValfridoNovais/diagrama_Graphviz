import streamlit as st
from graphviz import Digraph
import os

def create_diagram():
    # Criando o diagrama com fundo degradê
    diagram = Digraph('Esquema Conceitual Oficina Mecânica')
    
    # Configuração do estilo geral do diagrama
    diagram.attr(bgcolor="white:lightblue", style="filled", gradientangle="270")
    
    # Estilo de nó com fonte reduzida e sombra suave
    node_style = {
        'shape': 'box',
        'style': 'filled,rounded',
        'fillcolor': '#f9f9f9',
        'fontname': 'Arial',
        'fontsize': '10',
        'penwidth': '1.5',
        'color': '#cccccc'
    }
    
    # Entidades com estilo personalizado
    diagram.node('Cliente', 'Cliente\n(Código, Nome, Telefone, Endereço)', **node_style)
    diagram.node('Veículo', 'Veículo\n(Código, Placa, Modelo, Marca, Ano, Código Cliente)', **node_style)
    diagram.node('OS', 'Ordem de Serviço (OS)\n(Número, Data de Emissão, Data de Conclusão, Valor Total, Status, Código Veículo, Código Equipe)', **node_style)
    diagram.node('Mecânico', 'Mecânico\n(Código, Nome, Endereço, Especialidade)', **node_style)
    diagram.node('Equipe', 'Equipe\n(Código, Nome da Equipe)', **node_style)
    diagram.node('Serviço', 'Serviço\n(Código, Descrição, Valor por Referência de Mão de Obra)', **node_style)
    diagram.node('Peça', 'Peça\n(Código, Descrição, Valor Unitário)', **node_style)
    diagram.node('TabelaMO', 'Tabela de Referência de Mão de Obra\n(Código, Descrição, Valor Hora)', **node_style)
    
    # Relacionamentos
    diagram.edge('Cliente', 'Veículo', label='1:N', fontsize='9')
    diagram.edge('Veículo', 'OS', label='1:N', fontsize='9')
    diagram.edge('OS', 'Equipe', label='N:1', fontsize='9')
    diagram.edge('Equipe', 'Mecânico', label='1:N', fontsize='9')
    diagram.edge('OS', 'Serviço', label='1:N', fontsize='9')
    diagram.edge('OS', 'Peça', label='1:N', fontsize='9')
    diagram.edge('Serviço', 'TabelaMO', label='N:1', fontsize='9')
    
    # Salvar como arquivo PDF e imagem
    output_path = './diagram_files'
    os.makedirs(output_path, exist_ok=True)
    diagram_path = os.path.join(output_path, 'esquema_oficina_conceitual')
    diagram.render(diagram_path, format='png')  # Renderizar PNG
    diagram.render(diagram_path, format='pdf')  # Renderizar PDF
    return diagram_path + '.pdf', diagram_path + '.png'

# Interface no Streamlit
st.title("Esquema Conceitual da Oficina Mecânica")

# Gerar o diagrama
pdf_path, png_path = create_diagram()

# Exibir o diagrama no Streamlit
st.subheader("Diagrama Gerado")
st.image(png_path, caption="Esquema Conceitual da Oficina Mecânica", use_container_width=True)

# Botões para download
st.download_button(
    label="Baixar PDF",
    data=open(pdf_path, "rb").read(),
    file_name="esquema_oficina_conceitual.pdf",
    mime="application/pdf"
)

st.download_button(
    label="Baixar Imagem",
    data=open(png_path, "rb").read(),
    file_name="esquema_oficina_conceitual.png",
    mime="image/png"
)
