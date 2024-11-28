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

# Função para criar o diagrama ER conforme as normas
def create_er_diagram(tables, relationships, db_name):
    diagram = Digraph('Diagrama ER', format='png')
    diagram.attr(bgcolor="white:lightblue", style="filled", gradientangle="270")
    
    # Adicionar título ao diagrama
    diagram.attr(
        label=f"Diagrama Entidade-Relacionamento\n{db_name}",
        labelloc="t",
        fontsize="26"
    )

    # Adicionar tabelas e colunas
    for table, columns in tables.items():
        # Adicionar retângulo para a tabela
        diagram.node(table, table, shape="box", style="filled", fillcolor="#f9f9f9", fontsize="14")
        
        # Adicionar elipses para cada coluna e conectá-las ao retângulo da tabela
        for column in columns:
            column_node = f"{table}_{column}"  # Identificador único para a coluna
            diagram.node(column_node, column, shape="ellipse", style="filled", fillcolor="#e3f2fd", fontsize="12")
            diagram.edge(table, column_node)  # Ligação entre tabela e coluna

    # Adicionar relacionamentos
    for relationship in relationships:
        # Criar losango para o relacionamento
        rel_label = relationship.get("label", "Relacionamento")
        rel_id = f"{relationship['from']}_to_{relationship['to']}"  # Identificador único para o losango
        diagram.node(rel_id, rel_label, shape="diamond", style="filled", fillcolor="#fff3e0", fontsize="12")
        
        # Conectar os losangos às tabelas relacionadas
        diagram.edge(relationship["from"], rel_id)
        diagram.edge(rel_id, relationship["to"])
    
    return diagram


# Função para gerar o SQL
def generate_sql(tables, relationships):
    sql_commands = []

    for table, columns in tables.items():
        column_definitions = [f"{column} TEXT" for column in columns]
        table_relationships = [
            r for r in relationships if r["from"] == table
        ]
        for rel in table_relationships:
            column_definitions.append(
                f"FOREIGN KEY ({rel['from']}_id) REFERENCES {rel['to']}({rel['from']}_id)"
            )

        sql = f"CREATE TABLE {table} (\n  " + ",\n  ".join(column_definitions) + "\n);"
        sql_commands.append(sql)

    return "\n\n".join(sql_commands)

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
        
        # Visualizar e editar tabelas
        st.subheader("Tabelas Existentes")
        for table, columns in st.session_state["tables"].items():
            st.write(f"**{table}**: {', '.join(columns)}")
            new_columns = st.text_area(f"Editar Colunas de {table}", "\n".join(columns)).split("\n")
            st.session_state["tables"][table] = [col.strip() for col in new_columns if col.strip()]

        # Adicionar nova tabela
        with st.form("add_table_form", clear_on_submit=True):
            st.write("Adicionar Nova Tabela:")
            table_name = st.text_input("Nome da Tabela")
            num_columns = st.number_input("Número de Colunas", min_value=1, step=1)
            submitted = st.form_submit_button("Adicionar Tabela")
            if submitted:
                if table_name and table_name not in st.session_state["tables"]:
                    st.session_state["tables"][table_name] = [f"Coluna {i+1}" for i in range(int(num_columns))]
                    st.success(f"Tabela '{table_name}' adicionada com sucesso!")
                else:
                    st.error("O nome da tabela é obrigatório ou já existe.")

        # Visualizar e editar relacionamentos
        st.subheader("Relacionamentos Existentes")
        if len(st.session_state["relationships"]) > 0:
            for idx, rel in enumerate(st.session_state["relationships"]):
                st.write(f"{idx+1}. {rel['from']} → {rel['to']} ({rel.get('label', 'Sem descrição')})")
        else:
            st.write("Nenhum relacionamento encontrado.")

        # Adicionar ou remover relacionamentos
        with st.form("edit_relationship_form", clear_on_submit=True):
            st.write("Adicionar Novo Relacionamento:")
            from_table = st.selectbox("Tabela de Origem", options=list(st.session_state["tables"].keys()), key="rel_from")
            to_table = st.selectbox("Tabela de Destino", options=list(st.session_state["tables"].keys()), key="rel_to")
            relationship_label = st.text_input("Descrição do Relacionamento (Opcional)")
            submitted_rel = st.form_submit_button("Adicionar Relacionamento")
            if submitted_rel:
                st.session_state["relationships"].append({"from": from_table, "to": to_table, "label": relationship_label})
                st.success("Relacionamento adicionado com sucesso!")

            if len(st.session_state["relationships"]) > 0:
                remove_idx = st.number_input(
                    "Digite o número do relacionamento para removê-lo",
                    min_value=1, max_value=len(st.session_state["relationships"]), step=1
                )
                remove_submitted = st.form_submit_button("Remover Relacionamento")
                if remove_submitted:
                    del st.session_state["relationships"][remove_idx - 1]
                    st.success("Relacionamento removido com sucesso!")

        # Salvar alterações no banco de dados
        if st.button("Salvar Alterações"):
            save_database(
                st.session_state["current_db"],
                st.session_state["tables"],
                st.session_state["relationships"]
            )
            st.success(f"Alterações salvas no banco de dados '{st.session_state['current_db']}'.")

# Visualizar diagramas e SQL
elif action == "Visualizar Diagramas":
    st.title("Visualizar Diagramas e SQL")
    db_list = list_databases()
    if db_list:
        selected_db = st.selectbox("Selecione um Banco de Dados", db_list)
        if st.button("Gerar Diagrama e SQL"):
            tables, relationships = load_database(selected_db)
            diagram = create_er_diagram(tables, relationships, selected_db)
            diagram_path = f"./{selected_db}_diagram"
            diagram.render(diagram_path, format="png")
            st.image(f"{diagram_path}.png", caption=f"Diagrama do Banco de Dados: {selected_db}", use_container_width=True)


            sql_script = generate_sql(tables, relationships)
            st.subheader("Comando SQL Gerado")
            st.code(sql_script, language="sql")
            with open(f"{selected_db}_script.sql", "w") as f:
                f.write(sql_script)
            with open(f"{selected_db}_script.sql", "rb") as sql_file:
                st.download_button("Baixar Script SQL", data=sql_file, file_name=f"{selected_db}_script.sql", mime="text/sql")
