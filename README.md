# Gerador Dinâmico de Banco de Dados com Diagramas e SQL

## Descrição

Este programa permite criar, editar e visualizar bancos de dados de forma dinâmica. Ele gera diagramas de Entidade-Relacionamento (ER) e scripts SQL para criação do banco de dados. Desenvolvido em Python utilizando o Streamlit e Graphviz, o programa oferece uma interface interativa para gerenciamento de tabelas e seus relacionamentos.

---

## Funcionalidades

- **Criação de Bancos de Dados**: Permite criar novos bancos de dados com nome personalizado.
- **Edição de Bancos de Dados**: Adicione ou edite tabelas e seus respectivos relacionamentos.
- **Visualização de Diagramas**: Gera diagramas ER representando graficamente o banco de dados.
- **Geração de SQL**: Gera comandos SQL completos para a criação do banco de dados.
- **Download de Resultados**:
  - Baixe os diagramas gerados como imagens (PNG).
  - Baixe o script SQL em um arquivo (.sql).

---

## Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **Streamlit**: Para a criação da interface web interativa.
- **Graphviz**: Para geração dos diagramas ER.
- **JSON**: Para persistência de dados entre sessões.

---

## Requisitos

Antes de executar o programa, certifique-se de ter as seguintes dependências instaladas:

1. **Python**: Versão 3.8 ou superior.
2. **Bibliotecas Python**:
   - `streamlit`
   - `graphviz`
3. **Graphviz**:
   - Instale o Graphviz no sistema para geração de diagramas.

---

### Instalação das Dependências

bash
pip install streamlit graphviz

### Instalação do Graphviz

- **Windows**:  
  Baixe o instalador [Graphviz](https://graphviz.org/download/) e siga as instruções.

- **Linux**:  
  ```bash
  sudo apt install graphviz

- **macOS**:  
  ```bash
  brew install graphviz

# Como Usar

## Clone o repositório:

- **Clone**:
  ```bash
 git clone <URL do repositório>
 cd <nome do diretório clonado>
  

## Execute o programa:
- **Execução**:
 ```bash
 streamlit run app.py

## Acesse no navegador:
Normalmente, o Streamlit será iniciado em [http://localhost:8501](http://localhost:8501).

## Utilize a interface:
- **Criar Novo Banco de Dados:** Insira o nome do banco e adicione tabelas com colunas e relacionamentos.
- **Editar Banco de Dados:** Carregue um banco existente para modificações.
- **Visualizar Diagramas e SQL:** Gera e exibe o diagrama ER e o script SQL correspondente.

## Exporte os resultados:
- **Baixar Diagrama:** Clique no botão para salvar o diagrama como PNG.
- **Baixar Script SQL:** Salve o comando SQL gerado como um arquivo `.sql`.

## Estrutura do Código
- **app.py:** Contém toda a lógica do programa, incluindo a interface Streamlit, geração de diagramas, e criação de SQL.
- **bancos_dados/:** Diretório onde os bancos de dados são salvos em arquivos JSON.

## Funções Principais
- **save_database:** Salva as tabelas e relacionamentos no formato JSON.
- **load_database:** Carrega um banco de dados existente.
- **generate_sql:** Gera o script SQL para criar as tabelas e relacionamentos.
- **create_dynamic_diagram:** Gera o diagrama ER com Graphviz.

