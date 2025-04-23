import streamlit as st
import random
import json
from datetime import datetime
import os

# Lista de questões (50 no total)
QUESTIONS = [
    # Parte 1: Textos Narrativos (10 questões)
    {"question": "Qual característica define uma crônica?", "options": ["É uma história longa sobre fatos históricos.", "Combina literatura e jornalismo, narrando fatos cotidianos.", "É uma narrativa científica sobre o universo.", "Foca apenas em diálogos entre personagens."], "correct": 1},
    {"question": "Em uma narrativa de aventura, o que é comum encontrar?", "options": ["Personagens enfrentando desafios com tensão e surpresas.", "Descrições detalhadas de experimentos científicos.", "Listas de regras gramaticais.", "Receitas de culinária."], "correct": 0},
    {"question": "Qual tipo de narrador participa da história como personagem?", "options": ["Narrador-observador", "Narrador-onisciente", "Narrador-personagem", "Narrador-jornalista"], "correct": 2},
    {"question": "Um narrador-onisciente se diferencia por:", "options": ["Narrar em 1ª pessoa.", "Conhecer os sentimentos e pensamentos das personagens.", "Focar apenas nos diálogos.", "Não participar da história."], "correct": 1},
    {"question": "Em uma crônica, o autor geralmente escreve em:", "options": ["1ª pessoa, com tom pessoal.", "3ª pessoa, de forma imparcial.", "2ª pessoa, dando ordens.", "4ª pessoa, como narrador coletivo."], "correct": 0},
    {"question": "Qual é a função do narrador-observador?", "options": ["Narrar os fatos de forma imparcial, em 3ª pessoa.", "Participar ativamente da história.", "Descrever apenas os sentimentos do autor.", "Criar diálogos fictícios sem contexto."], "correct": 0},
    {"question": "Uma narrativa de aventura geralmente apresenta:", "options": ["Momentos de tensão e sobressaltos.", "Análises matemáticas detalhadas.", "Listas de compras.", "Relatórios escolares."], "correct": 0},
    {"question": "Qual tipo de texto narrativo é mais provável de ter um tom crítico ou humorístico?", "options": ["Narrativa de aventura", "Crônica", "Relatório científico", "Poema épico"], "correct": 1},
    {"question": "Um narrador que diz 'Eu vi o herói lutar' é:", "options": ["Narrador-observador", "Narrador-onisciente", "Narrador-personagem", "Narrador-externo"], "correct": 2},
    {"question": "Qual elemento NÃO é típico de uma narrativa de aventura?", "options": ["Momentos de tensão", "Surpresas na trama", "Desafios para os personagens", "Análise gramatical detalhada"], "correct": 3},

    # Parte 2: Pronomes Demonstrativos e Possessivos (20 questões)
    {"question": "Qual pronome demonstrativo é mais adequado: '___ sorvete é delicioso!' (referindo-se a algo próximo)?", "options": ["Esse", "Este", "Aquele", "Aquilo"], "correct": 1},
    {"question": "Escolha o pronome correto: '___ livro aí é meu.' (referindo-se a algo longe de quem fala, mas próximo de quem escuta)", "options": ["Este", "Aquele", "Esse", "Aquilo"], "correct": 2},
    {"question": "Qual pronome possessivo completa: 'Eu trouxe ___ lanche.'?", "options": ["teu", "meu", "dela", "nossa"], "correct": 1},
    {"question": "Escolha o pronome demonstrativo: '___ viagem foi inesquecível.' (referindo-se a algo no passado)", "options": ["Este", "Esse", "Aquele", "Aquela"], "correct": 2},
    {"question": "Qual pronome possessivo é correto: '___ ideias são ótimas!' (referindo-se a 'vocês')?", "options": ["Minhas", "Tuas", "Nossas", "Vossas"], "correct": 3},
    {"question": "Escolha o pronome demonstrativo: '___ é o melhor filme que já vi.' (referindo-se a algo que acabei de mencionar)", "options": ["Este", "Aquele", "Esse", "Aquilo"], "correct": 2},
    {"question": "Qual pronome possessivo completa: 'Você viu ___ irmão ontem?' (referindo-se a 'eu')?", "options": ["teu", "meu", "dela", "nosso"], "correct": 1},
    {"question": "Escolha o pronome demonstrativo: '___ cidade lá no horizonte é linda.' (referindo-se a algo muito distante)", "options": ["Esta", "Essa", "Aquela", "Este"], "correct": 2},
    {"question": "Qual pronome possessivo é correto: '___ casa é muito grande.' (referindo-se a 'ele')?", "options": ["Minha", "Tua", "Sua", "Nossa"], "correct": 2},
    {"question": "Escolha o pronome demonstrativo: '___ é o meu caderno.' (referindo-se a algo próximo)", "options": ["Esse", "Este", "Aquele", "Aquilo"], "correct": 1},
    {"question": "Qual pronome possessivo completa: 'Nós perdemos ___ chance.'?", "options": ["tua", "minha", "nossa", "vossa"], "correct": 2},
    {"question": "Escolha o pronome demonstrativo: '___ momento foi especial.' (referindo-se a algo no passado)", "options": ["Este", "Aquele", "Esse", "Esta"], "correct": 1},
    {"question": "Qual pronome possessivo é correto: 'Vocês trouxeram ___ livros?'?", "options": ["Meus", "Teus", "Vossos", "Nossos"], "correct": 2},
    {"question": "Escolha o pronome demonstrativo: '___ é o meu celular.' (referindo-se a algo próximo de quem escuta)", "options": ["Este", "Aquele", "Esse", "Aquilo"], "correct": 2},
    {"question": "Qual pronome possessivo completa: 'Ela esqueceu ___ mochila.'?", "options": ["minha", "sua", "nossa", "vossa"], "correct": 1},
    {"question": "Escolha o pronome demonstrativo: '___ é o melhor lugar para visitar.' (referindo-se a algo muito distante)", "options": ["Este", "Esse", "Aquele", "Esta"], "correct": 2},
    {"question": "Qual pronome possessivo é correto: 'Eu gosto de ___ escola.' (referindo-se a 'nós')?", "options": ["minha", "tua", "nossa", "vossa"], "correct": 2},
    {"question": "Escolha o pronome demonstrativo: '___ é o meu sonho.' (referindo-se a algo que acabei de mencionar)", "options": ["Este", "Aquele", "Esse", "Aquilo"], "correct": 2},
    {"question": "Qual pronome possessivo completa: 'Tu perdeste ___ chave?'?", "options": ["minha", "tua", "sua", "nossa"], "correct": 1},
    {"question": "Escolha o pronome demonstrativo: '___ é o meu bairro.' (referindo-se a algo próximo)", "options": ["Este", "Esse", "Aquele", "Aquilo"], "correct": 0},

    # Parte 3: Sintagma Nominal (10 questões)
    {"question": "Qual artigo definido é correto: '___ alunos chegaram.'?", "options": ["Um", "Os", "Uma", "Uns"], "correct": 1},
    {"question": "Escolha o adjetivo que completa: 'Os dias estão ___.'?", "options": ["quente", "quentes", "quentis", "quentos"], "correct": 1},
    {"question": "Qual numeral é correto: '___ lugar foi meu.'?", "options": ["Primeiro", "Um", "Uns", "Uma"], "correct": 0},
    {"question": "Qual artigo indefinido completa: 'Comprei ___ livro novo.'?", "options": ["O", "A", "Um", "Os"], "correct": 2},
    {"question": "Escolha a locução adjetiva: 'A casa é ___.'?", "options": ["cheia de alegria", "feliz", "alegres", "felizes"], "correct": 0},
    {"question": "Qual artigo definido é correto: '___ escola é grande.'?", "options": ["Uma", "A", "Um", "Uns"], "correct": 1},
    {"question": "Escolha o adjetivo: 'Os alunos são ___.'?", "options": ["dedicado", "dedicados", "dedicada", "dedicadas"], "correct": 1},
    {"question": "Qual numeral indica ordem: 'Cheguei em ___ lugar.'?", "options": ["Dois", "Segundo", "Duas", "Três"], "correct": 1},
    {"question": "Qual artigo indefinido é correto: 'Vi ___ pássaros voando.'?", "options": ["Os", "As", "Uns", "O"], "correct": 2},
    {"question": "Escolha a locução adjetiva: 'O céu está ___.'?", "options": ["cheio de estrelas", "estrelado", "estrelas", "estrelados"], "correct": 0},

    # Parte 4: Variação Linguística (10 questões)
    {"question": "Qual tipo de variação linguística é representada por 'uai, sô?' (típico de Minas Gerais)?", "options": ["Histórica", "Geográfica", "Social", "Situacional"], "correct": 1},
    {"question": "Escolha a forma mais adequada em um contexto formal: 'Eu ___ muito cansado.'?", "options": ["tô", "estou", "tava", "estava"], "correct": 1},
    {"question": "Qual tipo de variação ocorre quando uma palavra como 'tu' é substituída por 'você' ao longo do tempo?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 1},
    {"question": "Em um contexto informal em Minas Gerais, como se diria 'coisa'?", "options": ["Trem", "Negócio", "Bagulho", "Traste"], "correct": 0},
    {"question": "Qual tipo de variação linguística depende do nível social do falante?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 2},
    {"question": "Escolha a forma mais formal: '___ você fez o dever?'?", "options": ["Cê", "Tu", "Você", "Ocê"], "correct": 2},
    {"question": "Qual tipo de variação ocorre quando alguém diz 'vou ali' em um contexto informal e 'vou até aquele local' em um formal?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 3},
    {"question": "Em Minas Gerais, 'biscoito' pode ser chamado de:", "options": ["Bolacha", "Quitanda", "Pão", "Doce"], "correct": 0},
    {"question": "Qual tipo de variação linguística é observada quando uma pessoa muda o tom ao falar com um chefe e depois com um amigo?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 3},
    {"question": "Escolha a forma mais informal: 'Eu ___ feliz.'?", "options": ["estou", "tô", "estava", "era"], "correct": 1},
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
st.title("Simulado de Língua Portuguesa – Marina (7º Ano)")

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