import streamlit as st
from graphviz import Digraph
import json
import os
from datetime import datetime
from fpdf import FPDF

# Diretório onde os bancos de dados serão salvos
DB_DIR = "./bancos_dados"
os.makedirs(DB_DIR, exist_ok=True)

# Função para criar pastas para cada banco de dados
def ensure_directories(db_name):
    db_path = os.path.join(DB_DIR, db_name)
    pdf_dir = os.path.join(db_path, "PDF")
    img_dir = os.path.join(db_path, "IMG")
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    return db_path, pdf_dir, img_dir

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

# Função para criar o diagrama ER com notação Chen
def create_chen_diagram(tables, relationships, db_name):
    diagram = Digraph('Diagrama ER', format='png')
    diagram.attr(bgcolor="white", style="filled", gradientangle="270")
    diagram.attr(label=f"Diagrama ER - {db_name}", fontsize="20", labelloc="t")
    
    # Adicionar entidades e seus atributos (elipses)
    for table, columns in tables.items():
        with diagram.subgraph(name=f"cluster_{table}") as sub:
            sub.attr(label=f"<<b>{table}</b>>", style="filled,rounded", color="lightblue", fontsize="14")
            for column in columns:
                sub.node(f"{table}_{column}", label=column, shape="ellipse", fontsize="10")
                sub.edge(table, f"{table}_{column}")

    # Adicionar relacionamentos
    for relationship in relationships:
        from_table = relationship["from"]
        to_table = relationship["to"]
        label = relationship.get("label", "")
        
        diagram.node(f"rel_{from_table}_{to_table}", label=label, shape="diamond", fontsize="12", style="filled", fillcolor="lightgrey")
        diagram.edge(from_table, f"rel_{from_table}_{to_table}", label="1")
        diagram.edge(f"rel_{from_table}_{to_table}", to_table, label="N")

    return diagram

# Função para gerar SQL
def generate_sql(tables, relationships):
    sql_statements = []
    for table, columns in tables.items():
        columns_sql = ",\n  ".join([f"{col} TEXT" for col in columns])
        sql_statements.append(f"CREATE TABLE {table} (\n  {columns_sql}\n);")

    for relationship in relationships:
        from_table = relationship["from"]
        to_table = relationship["to"]
        label = relationship.get("label", "")
        sql_statements.append(f"-- Relacionamento: {label}\nALTER TABLE {to_table} ADD FOREIGN KEY ({from_table}_id) REFERENCES {from_table}(id);")

    return "\n\n".join(sql_statements)

# Função para salvar o PDF
def save_pdf(pdf_path, db_name, sql_script, img_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Diagrama ER - {db_name}", ln=True, align='C')
    
    # SQL Script
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Script SQL:", ln=True)
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 10, sql_script)
    
    # Imagem do diagrama
    pdf.ln(10)
    if os.path.exists(img_path):
        pdf.image(img_path, x=10, y=pdf.get_y(), w=180)
    
    pdf.output(pdf_path)

# Interface Streamlit
st.title("Gerador de Diagramas ER - Notação Chen")

# Inicializar variáveis de sessão
if "current_db" not in st.session_state:
    st.session_state["current_db"] = None
if "tables" not in st.session_state:
    st.session_state["tables"] = {}
if "relationships" not in st.session_state:
    st.session_state["relationships"] = []

# Sidebar para ações
action = st.sidebar.selectbox(
    "Escolha uma ação",
    ["Criar Novo Banco de Dados", "Editar Banco de Dados", "Visualizar Diagramas e SQL"]
)

# Criar novo banco de dados
if action == "Criar Novo Banco de Dados":
    st.header("Criar Novo Banco de Dados")
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

# Visualizar diagramas e SQL
elif action == "Visualizar Diagramas e SQL":
    st.header("Visualizar Diagramas e SQL")
    db_list = list_databases()
    if db_list:
        selected_db = st.selectbox("Selecione um Banco de Dados", db_list)
        if st.button("Gerar Diagrama e SQL"):
            tables, relationships = load_database(selected_db)
            
            # Gerar diagrama
            diagram = create_chen_diagram(tables, relationships, selected_db)
            db_path, pdf_dir, img_dir = ensure_directories(selected_db)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = os.path.join(img_dir, f"{selected_db}_diagram_{timestamp}.png")
            pdf_path = os.path.join(pdf_dir, f"{selected_db}_diagram_{timestamp}.pdf")
            
            diagram.render(img_path, format="png")
            st.image(f"{img_path}.png", caption=f"Diagrama do Banco de Dados: {selected_db}", use_container_width=True)
            
            # Gerar SQL
            sql_script = generate_sql(tables, relationships)
            st.text_area("Script SQL Gerado", sql_script, height=200)
            
            # Salvar PDF
            save_pdf(pdf_path, selected_db, sql_script, f"{img_path}.png")
            
            # Download do SQL
            st.download_button("Baixar Script SQL", data=sql_script, file_name=f"{selected_db}.sql", mime="text/plain")
            st.download_button("Baixar PDF do Diagrama", data=open(pdf_path, "rb"), file_name=f"{selected_db}_diagram_{timestamp}.pdf", mime="application/pdf")
