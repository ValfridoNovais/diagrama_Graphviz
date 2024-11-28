import streamlit as st
from graphviz import Digraph
import json
import os

# Diretório onde os bancos de dados serão salvos
DB_DIR = "./bancos_dados"
os.makedirs(DB_DIR, exist_ok=True)

# Função para salvar o banco de dados
def save_database(db_name, tables, relationships):
    db_path = os.path.join(DB_DIR, f"{db_name}.json")
    with open(db_path, "w") as f:
        json.dump({"tables": tables, "relationships": relationships}, f)

# Função para carregar um banco de dados
def load_database(db_name):
    db_path = os.path.join(DB_DIR, f"{db_name}.json")
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            data = json.load(f)
            return data.get("tables", {}), data.get("relationships", [])
    return {}, []

# Função para listar todos os bancos de dados
def list_databases():
    return [f.replace(".json", "") for f in os.listdir(DB_DIR) if f.endswith(".json")]

# Função para criar o diagrama
def create_dynamic_diagram(tables, relationships, db_name):
    diagram = Digraph('Diagrama ER', format='png')
    diagram.attr(bgcolor="white:lightblue", style="filled", gradientangle="270")
    
    # Adicionar título ao diagrama
    diagram.attr(
        label=f"Diagrama Entidade-Relacionamento\n{db_name}",
        labelloc="t",
        fontsize="26"
    )

    # Adicionar tabelas ao diagrama
    for table, columns in tables.items():
        # Nome da tabela em negrito e colunas na mesma linha
        column_text = ", ".join(columns)
        diagram.node(
            table,
            f"< <b>{table}</b><br/>\n{column_text} >",
            shape="box",
            style="filled,rounded",
            fillcolor="#f9f9f9",
            fontsize="12"
        )

    # Adicionar relacionamentos
    for relationship in relationships:
        diagram.edge(relationship["from"], relationship["to"], label=relationship.get("label", ""), fontsize="10")
    
    return diagram

# Inicializar variáveis de sessão para tabelas e relacionamentos
if "current_db" not in st.session_state:
    st.session_state["current_db"] = None
if "tables" not in st.session_state:
    st.session_state["tables"] = {}
if "relationships" not in st.session_state:
    st.session_state["relationships"] = []

# Sidebar para selecionar a ação
st.sidebar.title("Gerenciamento de Bancos de Dados")
action = st.sidebar.selectbox(
    "Escolha uma ação",
    ["Criar Novo Banco de Dados", "Editar Banco de Dados", "Visualizar Diagramas"]
)

# Criar novo banco de dados
if action == "Criar Novo Banco de Dados":
    st.title("Criar Novo Banco de Dados")
    db_name = st.text_input("Nome do Banco de Dados")
    
    if db_name and st.button("Criar Banco de Dados"):
        if db_name not in list_databases():
            st.session_state["current_db"] = db_name
            st.session_state["tables"] = {}
            st.session_state["relationships"] = []
            save_database(db_name, {}, [])
            st.success(f"Banco de Dados '{db_name}' criado com sucesso!")
        else:
            st.error("Já existe um banco de dados com esse nome.")

# Editar banco de dados existente
elif action == "Editar Banco de Dados":
    st.title("Editar Banco de Dados")
    db_list = list_databases()
    if db_list:
        selected_db = st.selectbox("Selecione um Banco de Dados", db_list)
        if st.button("Carregar Banco de Dados"):
            st.session_state["current_db"] = selected_db
            tables, relationships = load_database(selected_db)
            st.session_state["tables"] = tables
            st.session_state["relationships"] = relationships
            st.success(f"Banco de Dados '{selected_db}' carregado com sucesso!")
    
    if st.session_state["current_db"]:
        st.write(f"**Banco de Dados Atual**: {st.session_state['current_db']}")
        
        # Formulário para adicionar uma nova tabela
        with st.form("add_table_form", clear_on_submit=True):
            table_name = st.text_input("Nome da Tabela")
            num_columns = st.number_input("Número de Colunas", min_value=1, step=1)
            submitted = st.form_submit_button("Adicionar Tabela")
            
            if submitted:
                if table_name and table_name not in st.session_state["tables"]:
                    st.session_state["tables"][table_name] = [f"Coluna {i+1}" for i in range(int(num_columns))]
                else:
                    st.error("O nome da tabela é obrigatório ou já existe.")

        # Mostrar tabelas existentes e permitir edição
        st.subheader("Tabelas Criadas")
        for table, columns in st.session_state["tables"].items():
            st.write(f"**{table}**: {', '.join(columns)}")
            new_columns = st.text_area(f"Editar Colunas de {table}", "\n".join(columns)).split("\n")
            st.session_state["tables"][table] = new_columns

        # Interface para adicionar relacionamentos
        st.subheader("Adicionar Relacionamentos")
        with st.form("add_relationship_form", clear_on_submit=True):
            from_table = st.selectbox("Tabela de Origem", options=list(st.session_state["tables"].keys()))
            to_table = st.selectbox("Tabela de Destino", options=list(st.session_state["tables"].keys()))
            relationship_label = st.text_input("Descrição do Relacionamento (Opcional)")
            relationship_submitted = st.form_submit_button("Adicionar Relacionamento")
            
            if relationship_submitted:
                st.session_state["relationships"].append({"from": from_table, "to": to_table, "label": relationship_label})

        # Salvar alterações no banco de dados
        if st.button("Salvar Alterações"):
            save_database(
                st.session_state["current_db"],
                st.session_state["tables"],
                st.session_state["relationships"]
            )
            st.success(f"Alterações salvas no banco de dados '{st.session_state['current_db']}'.")

# Visualizar diagramas
elif action == "Visualizar Diagramas":
    st.title("Visualizar Diagramas")
    db_list = list_databases()
    if db_list:
        selected_db = st.selectbox("Selecione um Banco de Dados", db_list)
        if st.button("Gerar Diagrama"):
            tables, relationships = load_database(selected_db)
            diagram = create_dynamic_diagram(tables, relationships, selected_db)
            diagram_path = f"./{selected_db}_diagram"
            diagram.render(diagram_path, format="png")
            st.image(f"{diagram_path}.png", caption=f"Diagrama do Banco de Dados: {selected_db}", use_container_width=True)
            with open(f"{diagram_path}.png", "rb") as img:
                st.download_button("Baixar Imagem", data=img, file_name=f"{selected_db}_diagram.png", mime="image/png")
