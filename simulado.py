import streamlit as st
import random
import json
from datetime import datetime
import os

# Lista de questões (40 no total, nível mais desafiador)
QUESTIONS = [
    # Parte 1: Mitos (10 questões mais desafiadoras)
    {"question": "Os mitos frequentemente surgem para explicar fenômenos naturais. Qual dos exemplos abaixo é mais provável de ser tema de um mito?", "options": ["A invenção do celular.", "O motivo de haver trovões e relâmpagos.", "A construção de uma escola.", "A criação de um videogame."], "correct": 1},
    {"question": "No mito grego, Prometeu roubou o fogo dos deuses para dá-lo aos humanos. Qual valor cultural esse mito pode transmitir?", "options": ["A importância de obedecer aos deuses.", "A coragem de desafiar regras para ajudar a humanidade.", "A necessidade de evitar o fogo.", "A ideia de que os humanos não precisam de ajuda."], "correct": 1},
    {"question": "Em um mito indígena brasileiro, o guaraná teria surgido dos olhos de uma criança. O que isso simboliza?", "options": ["A origem de uma planta importante para o povo.", "A criação de um rio.", "A invenção de uma dança.", "A construção de uma casa."], "correct": 0},
    {"question": "Por que os mitos frequentemente apresentam seres sobrenaturais, como deuses ou espíritos?", "options": ["Porque são histórias modernas.", "Para explicar coisas que os povos antigos não entendiam.", "Porque os povos antigos não acreditavam em ciência.", "Para ensinar matemática."], "correct": 1},
    {"question": "No mito do Curupira, ele protege a floresta e engana caçadores. Qual característica dele ajuda nessa função?", "options": ["Ele tem asas para voar.", "Seus pés são virados para trás, confundindo rastros.", "Ele canta músicas bonitas.", "Ele constrói casas na floresta."], "correct": 1},
    {"question": "Qual é a diferença entre um mito e uma lenda?", "options": ["Um mito explica a criação do mundo, enquanto uma lenda é sobre heróis ou fatos locais.", "Uma lenda explica a criação do mundo, enquanto um mito é sobre heróis.", "Um mito é verdadeiro, e uma lenda é falsa.", "Uma lenda é escrita, e um mito é falado."], "correct": 0},
    {"question": "No mito de Iara, ela atrai pescadores para o rio. Qual elemento da natureza esse mito está relacionado?", "options": ["As montanhas.", "As águas dos rios.", "O fogo.", "O vento."], "correct": 1},
    {"question": "Os mitos muitas vezes refletem os valores de um povo. No mito de Tupã, que criou o céu e a terra, qual valor pode ser destacado?", "options": ["A importância de cuidar da natureza.", "A necessidade de construir cidades.", "A valorização de jogos.", "A ideia de não trabalhar."], "correct": 0},
    {"question": "No mito africano de Anansi, a aranha, ele é conhecido por sua inteligência. Qual lição esse mito pode ensinar?", "options": ["Que a força é mais importante que a inteligência.", "Que a inteligência pode superar desafios.", "Que as aranhas são perigosas.", "Que não devemos ajudar os outros."], "correct": 1},
    {"question": "Qual dessas histórias NÃO seria considerada um mito?", "options": ["A criação do sol e da lua por um deus.", "A história de um rei que viveu há 100 anos e construiu um castelo.", "O surgimento do rio Amazonas a partir de lágrimas de uma deusa.", "A explicação de por que o jacaré tem a boca grande."], "correct": 1},

    # Parte 2: Ortografia – Uso de S, C, Ç, SS (20 questões mais desafiadoras)
    {"question": "Qual palavra está escrita corretamente e faz sentido na frase: 'Eu gosto de ___ no parque.'?", "options": ["dançar", "danssar", "dançar", "danççar"], "correct": 0},
    {"question": "Na frase 'A ___ está cheia de flores.', qual é a palavra correta?", "options": ["praça", "prassa", "praçsa", "prasa"], "correct": 0},
    {"question": "Qual palavra está escrita corretamente na frase: 'O ___ do sol", "options": ["nassi", "naçi", "nascer", "naçci"], "correct": 2},
    {"question": "Escolha a palavra correta para completar: 'Eu vi uma ___ na floresta.'?", "options": ["onssa", "onça", "onçsa", "onsa"], "correct": 1},
    {"question": "Qual é a escrita correta na frase: 'Eu gosto de tomar um suco com ___.'?", "options": ["assúcar", "açúcar", "açúçar", "assucar"], "correct": 1},
    {"question": "Na frase 'Eu escrevo com um ___ azul.', qual é a palavra correta?", "options": ["lápis", "lápiz", "lapis", "lapiz"], "correct": 0},
    {"question": "Escolha a palavra correta para: 'O ___ é um animal esperto.'?", "options": ["macaco", "makaco", "maçaco", "macako"], "correct": 0},
    {"question": "Qual é a palavra correta na frase: 'Eu gosto de música ___.'?", "options": ["clásica", "clássica", "cláçica", "clásika"], "correct": 1},
    {"question": "Na frase 'Eu vi um ___ na árvore.', qual é a palavra correta?", "options": ["pasaro", "pássaro", "paçaro", "passaru"], "correct": 1},
    {"question": "Qual é a escrita correta para: 'Eu ___ no Brasil.'?", "options": ["nassi", "nasci", "naçi", "naçci"], "correct": 1},
    {"question": "Escolha a palavra correta: 'Eu gosto de ___ com meus amigos.'?", "options": ["conversar", "converçar", "converssar", "converçar"], "correct": 0},
    {"question": "Qual palavra está correta na frase: 'Eu vi um ___ no zoológico.'?", "options": ["leon", "leão", "leãu", "leõa"], "correct": 1},
    {"question": "Na frase 'Eu gosto de ___ no rio.', qual é a palavra correta?", "options": ["pescar", "peçar", "pesscar", "peçcar"], "correct": 0},
    {"question": "Escolha a palavra correta: 'Eu vi uma ___ no céu.'?", "options": ["nuvem", "nuven", "nuvén", "nuvêm"], "correct": 0},
    {"question": "Qual é a escrita correta na frase: 'Eu ___ um livro.'?", "options": ["escrevi", "escreví", "eskrevi", "escrivi"], "correct": 0},
    {"question": "Na frase 'Eu gosto de ___ frutas.', qual é a palavra correta?", "options": ["commer", "comer", "komer", "comér"], "correct": 1},
    {"question": "Escolha a palavra correta: 'Eu vi um ___ na rua.'?", "options": ["carro", "caro", "karo", "karro"], "correct": 0},
    {"question": "Qual palavra está correta na frase: 'Eu gosto de ___ histórias.'?", "options": ["contar", "kontar", "conntar", "contarr"], "correct": 0},
    {"question": "Na frase 'Eu ___ um gol.', qual é a palavra correta?", "options": ["marquei", "markei", "marqei", "marqueí"], "correct": 0},
    {"question": "Escolha a palavra correta: 'Eu gosto de ___ na praia.'?", "options": ["nadar", "naddar", "nada", "nadarr"], "correct": 0},

    # Parte 3: Marcadores de Tempo, Lugar e Modo (10 questões mais desafiadoras)
    {"question": "Qual marcador de tempo melhor completa a frase: 'Eu estudei ___ para a prova.'?", "options": ["ontem", "aqui", "cuidadosamente", "perto"], "correct": 0},
    {"question": "Na frase 'Eu corro ___ na pista.', qual é o marcador de lugar mais adequado?", "options": ["rapidamente", "hoje", "atrás", "dentro"], "correct": 3},
    {"question": "Qual marcador de modo se encaixa melhor na frase: 'Ela fala ___ com os amigos.'?", "options": ["ontem", "alegremente", "perto", "agora"], "correct": 1},
    {"question": "Escolha o marcador de tempo para completar: '___ eu vou viajar para a praia.'?", "options": ["Amanhã", "Atrás", "Cuidadosamente", "Aqui"], "correct": 0},
    {"question": "Na frase 'Eu deixei o livro ___ da estante.', qual é o marcador de lugar correto?", "options": ["ontem", "acima", "rapidamente", "hoje"], "correct": 1},
    {"question": "Qual marcador de modo completa a frase: 'Ele escreve ___ para não errar.'?", "options": ["perto", "devagar", "ontem", "aqui"], "correct": 1},
    {"question": "Escolha o marcador de tempo para: '___ eu estava muito cansado.'?", "options": ["Abaixo", "Ontem", "Cuidadosamente", "Perto"], "correct": 1},
    {"question": "Na frase 'Eu moro ___ da escola.', qual é o marcador de lugar mais adequado?", "options": ["longe", "hoje", "rapidamente", "ontem"], "correct": 0},
    {"question": "Qual marcador de modo se encaixa na frase: 'Ela dança ___ no palco.'?", "options": ["ontem", "perto", "graciosamente", "aqui"], "correct": 2},
    {"question": "Escolha o marcador de tempo para completar: '___ eu vou ao cinema.'?", "options": ["Atrás", "Hoje", "Cuidadosamente", "Perto"], "correct": 1},
]

# Função para carregar resultados anteriores do JSON
def load_results():
    if os.path.exists("results.json"):
        with open("results.json", "r") as f:
            return json.load(f)
    return []

# Função para salvar resultados no JSON
def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

# Título do simulado
st.title("Simulado de Língua Portuguesa – 6º Ano")

# Inicializar estado da sessão
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(QUESTIONS, 20)

# Lista de letras para as opções
LETTERS = ["A", "B", "C", "D"]

# Formulário para as respostas
with st.form(key="simulado_form"):
    # Exibir as questões
    for i, q in enumerate(st.session_state.selected_questions):
        st.markdown(f"**Questão {i + 1}: {q['question']}**")
        # Mapear as opções com letras (A, B, C, D)
        labeled_options = [f"{LETTERS[j]}. {opt}" for j, opt in enumerate(q["options"])]
        # Usar o índice da opção selecionada, sem pré-seleção (index=None)
        selected_option = st.radio(
            "Escolha uma opção:",
            options=range(len(q["options"])),
            format_func=lambda x: labeled_options[x],
            key=f"q_{i}",
            index=None  # Nenhuma opção pré-selecionada
        )
        st.session_state.answers[i] = selected_option

    # Botão para enviar respostas
    submitted = st.form_submit_button("Enviar Respostas")

# Validação: verificar se todas as questões foram respondidas
if submitted:
    # Verificar se há respostas não preenchidas
    unanswered = [i + 1 for i in range(len(st.session_state.selected_questions)) if st.session_state.answers.get(i) is None]
    if unanswered:
        st.error(f"Por favor, responda todas as questões! Questões não respondidas: {', '.join(map(str, unanswered))}.")
    else:
        st.session_state.submitted = True

        # Calcular pontuação
        correct = 0
        total = len(st.session_state.selected_questions)
        for i, q in enumerate(st.session_state.selected_questions):
            user_answer = st.session_state.answers[i]  # Índice da opção escolhida
            if user_answer == q["correct"]:
                correct += 1

        errors = total - correct

        # Exibir resultado
        st.write("### Resultado do Simulado")
        st.write(f"**Acertos:** {correct}/{total}")
        st.write(f"**Erros:** {errors}/{total}")
        st.write(f"**Percentual de acertos:** {correct/total*100:.1f}%")

        # Salvar resultado no JSON
        results = load_results()
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "correct": correct,
            "errors": errors,
            "total": total,
            "percentage": correct / total * 100
        }
        results.append(result)
        save_results(results)

        # Exibir histórico de tentativas
        st.write("### Histórico de Tentativas")
        for i, res in enumerate(results):
            st.write(f"Tentativa {i + 1} ({res['date']}): {res['correct']}/{res['total']} acertos ({res['percentage']:.1f}%)")

# Botão para reiniciar o simulado
if st.session_state.submitted and st.button("Tentar Novamente"):
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.selected_questions = random.sample(QUESTIONS, 20)
    st.experimental_rerun()