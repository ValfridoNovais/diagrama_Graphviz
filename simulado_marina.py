import streamlit as st
import random
import json
from datetime import datetime
import os

# Lista de questões (50 no total, ajustadas para maior dificuldade)
QUESTIONS = [
    # Parte 1: Textos Narrativos (10 questões)
    {"question": "Leia o trecho: 'Eu nunca pensei que viveria algo assim. O vento soprava forte enquanto eu tentava salvar meu amigo.' Qual tipo de narrador está presente?", "options": ["Narrador-observador", "Narrador-onisciente", "Narrador-personagem", "Narrador-externo"], "correct": 2},
    {"question": "Leia o trecho de uma crônica: 'Hoje, ao passar pela praça, vi um cachorro correndo atrás de um pombo. Será que ele sabia que nunca o alcançaria?' O que caracteriza esse texto como crônica?", "options": ["A presença de um herói enfrentando desafios.", "A narração de um fato cotidiano com tom reflexivo.", "A descrição científica de um evento.", "A ausência de narrador."], "correct": 1},
    {"question": "Em uma narrativa de aventura, o autor escreveu: 'A floresta parecia viva, sussurrando segredos que só os mais corajosos entenderiam.' Qual elemento típico está presente?", "options": ["Um tom humorístico sobre a vida cotidiana.", "A criação de tensão e mistério.", "A análise gramatical detalhada.", "A narração imparcial dos fatos."], "correct": 1},
    {"question": "Leia o trecho: 'Maria sabia o que Pedro sentia, mesmo sem ele dizer uma palavra.' Qual tipo de narrador pode conhecer os sentimentos de Maria?", "options": ["Narrador-observador", "Narrador-personagem", "Narrador-onisciente", "Narrador-jornalista"], "correct": 2},
    {"question": "Em uma crônica, o autor escreveu: 'A fila do ônibus estava enorme, e eu, como sempre, atrasado.' Qual característica do narrador está evidente?", "options": ["Ele narra em 3ª pessoa, de forma imparcial.", "Ele participa da história, usando a 1ª pessoa.", "Ele conhece os pensamentos de todos os personagens.", "Ele descreve apenas fatos históricos."], "correct": 1},
    {"question": "Leia o trecho: 'O herói enfrentou o dragão, mas ninguém sabia se ele sobreviveria.' Qual tipo de narrador NÃO revelaria o destino do herói imediatamente?", "options": ["Narrador-onisciente", "Narrador-observador", "Narrador-personagem", "Narrador-autor"], "correct": 1},
    {"question": "Uma narrativa de aventura começa com: 'O barco balançava violentamente no meio da tempestade.' Qual é o objetivo desse início?", "options": ["Apresentar uma análise histórica.", "Criar um momento de tensão inicial.", "Explicar regras gramaticais.", "Descrever um diálogo formal."], "correct": 1},
    {"question": "Leia o trecho de uma crônica: 'Todo dia, o mesmo caminho, mas hoje o sol parecia diferente.' Qual sentimento o narrador pode estar expressando?", "options": ["Medo de uma tempestade.", "Reflexão sobre a rotina e algo novo.", "Alegria por estar atrasado.", "Indiferença total."], "correct": 1},
    {"question": "Em uma narrativa, o autor escreveu: 'João não sabia, mas aquele seria seu último dia na vila.' Quem poderia saber disso?", "options": ["Narrador-personagem", "Narrador-observador", "Narrador-onisciente", "Narrador-protagonista"], "correct": 2},
    {"question": "Leia o trecho: 'A caverna estava escura, e cada passo ecoava como um aviso.' Qual elemento de narrativa de aventura está presente?", "options": ["Um tom humorístico.", "A criação de suspense.", "A narração de fatos cotidianos.", "A ausência de personagens."], "correct": 1},

    # Parte 2: Pronomes Demonstrativos e Possessivos (20 questões)
    {"question": "Leia o diálogo: 'Você viu o caderno que estava aqui?' 'Sim, é ___ que está na mesa?' Qual pronome demonstrativo é mais adequado?", "options": ["este", "esse", "aquele", "aquilo"], "correct": 1},
    {"question": "Reescreva a frase ajustando o pronome: 'Eu gosto deste filme.' (referindo-se a um filme que foi mencionado antes)", "options": ["Eu gosto de esse filme.", "Eu gosto de aquele filme.", "Eu gosto de esse filme.", "Eu gosto de aquele filme."], "correct": 2},
    {"question": "Complete com o pronome possessivo: 'Eu e Ana perdemos ___ livros na escola.'", "options": ["nossos", "meus", "teus", "vossos"], "correct": 0},
    {"question": "Leia: 'Você já foi àquele lugar que te falei?' Qual pronome demonstrativo indica algo distante no discurso?", "options": ["este", "esse", "aquele", "aquela"], "correct": 2},
    {"question": "Corrija o pronome possessivo: 'Eu trouxe tua mochila, João.' (João é 'ele')", "options": ["Eu trouxe sua mochila, João.", "Eu trouxe minha mochila, João.", "Eu trouxe nossa mochila, João.", "Eu trouxe vossa mochila, João."], "correct": 0},
    {"question": "Complete: '___ é o melhor dia da semana!' (referindo-se a algo que está acontecendo agora)", "options": ["Este", "Esse", "Aquele", "Aquilo"], "correct": 0},
    {"question": "Leia: 'Nós esquecemos ___ lanches no ônibus.' Qual pronome possessivo é correto?", "options": ["meus", "teus", "nossos", "vossos"], "correct": 2},
    {"question": "Escolha o pronome demonstrativo: 'Você lembra ___ viagem que fizemos ano passado?'", "options": ["desta", "dessa", "daquela", "deste"], "correct": 2},
    {"question": "Reescreva ajustando o pronome: 'Esta casa é minha.' (referindo-se a algo longe de quem fala e de quem escuta)", "options": ["Essa casa é minha.", "Aquela casa é minha.", "Este casa é minha.", "Aquele casa é minha."], "correct": 1},
    {"question": "Complete: 'Você viu ___ bicicleta nova?' (referindo-se a 'eu')", "options": ["tua", "minha", "sua", "nossa"], "correct": 1},
    {"question": "Leia: '___ é o meu melhor amigo.' (apontando para alguém próximo)", "options": ["Este", "Esse", "Aquele", "Aquilo"], "correct": 0},
    {"question": "Complete: 'Vocês trouxeram ___ projetos para a feira?'", "options": ["meus", "teus", "vossos", "nossos"], "correct": 2},
    {"question": "Reescreva: 'Eu gosto desse lugar.' (referindo-se a algo muito distante)", "options": ["Eu gosto de este lugar.", "Eu gosto de aquele lugar.", "Eu gosto de esta lugar.", "Eu gosto de aquele lugar."], "correct": 1},
    {"question": "Complete: 'Ela disse que ___ ideias são ótimas.' (referindo-se a 'vocês')", "options": ["minhas", "tuas", "vossas", "nossas"], "correct": 2},
    {"question": "Leia o diálogo: 'Você já foi a este parque?' 'Não, mas ___ parque ali parece legal.' Qual pronome demonstrativo é adequado?", "options": ["este", "esse", "aquele", "aquilo"], "correct": 2},
    {"question": "Complete: 'Eu perdi ___ carteira no mercado.'", "options": ["minha", "tua", "sua", "vossa"], "correct": 0},
    {"question": "Escolha o pronome demonstrativo: '___ é o melhor show que já vi!' (referindo-se a algo que acabou de acontecer)", "options": ["Este", "Esse", "Aquele", "Aquilo"], "correct": 1},
    {"question": "Complete: 'Nós adoramos ___ escola nova.'", "options": ["minha", "tua", "nossa", "vossa"], "correct": 2},
    {"question": "Reescreva: 'Esse é o meu sonho.' (referindo-se a algo próximo)", "options": ["Este é o meu sonho.", "Aquele é o meu sonho.", "Este é o meu sonho.", "Aquele é o meu sonho."], "correct": 0},
    {"question": "Complete: 'Tu esqueceste ___ chave em casa?'", "options": ["minha", "tua", "sua", "nossa"], "correct": 1},

    # Parte 3: Sintagma Nominal (10 questões)
    {"question": "Corrija a frase: 'Os aluno chegaram atrasados.'", "options": ["Os alunos chegaram atrasados.", "O aluno chegaram atrasados.", "Os aluno chegou atrasados.", "Os alunos chegou atrasados."], "correct": 0},
    {"question": "Complete com o adjetivo correto: 'As meninas estão ___ com o resultado.'", "options": ["feliz", "felizes", "felizs", "felizis"], "correct": 1},
    {"question": "Escolha o numeral ordinal: 'Eu fiquei em ___ lugar na corrida.'", "options": ["dois", "segundo", "duas", "segunda"], "correct": 1},
    {"question": "Complete com o artigo indefinido: 'Quero comprar ___ blusa nova.'", "options": ["o", "a", "uma", "uns"], "correct": 2},
    {"question": "Reescreva com uma locução adjetiva: 'O menino está feliz.'", "options": ["O menino está cheio de alegria.", "O menino está alegrado.", "O menino está felizes.", "O menino está felicidade."], "correct": 0},
    {"question": "Corrija a frase: 'A livros estão na mesa.'", "options": ["O livros estão na mesa.", "Os livros estão na mesa.", "A livro estão na mesa.", "As livros estão na mesa."], "correct": 1},
    {"question": "Complete com o adjetivo: 'Os cães são ___.'", "options": ["leal", "leais", "leals", "lealz"], "correct": 1},
    {"question": "Escolha o numeral cardinal: 'Comprei ___ maçãs.'", "options": ["primeiro", "segundo", "três", "terceiro"], "correct": 2},
    {"question": "Complete com o artigo definido: '___ crianças brincam no parque.'", "options": ["Um", "Uma", "As", "Uns"], "correct": 2},
    {"question": "Reescreva com uma locução adjetiva: 'O céu está estrelado.'", "options": ["O céu está cheio de estrelas.", "O céu está estrelas.", "O céu está estrelados.", "O céu está estrelar."], "correct": 0},

    # Parte 4: Variação Linguística (10 questões)
    {"question": "Leia o diálogo em Minas Gerais: 'Uai, sô, cê viu meu trem?' Qual tipo de variação está presente e qual é o significado de 'trem'?", "options": ["Geográfica; significa 'traste'.", "Geográfica; significa 'coisa'.", "Social; significa 'brinquedo'.", "Histórica; significa 'carro'."], "correct": 1},
    {"question": "Reescreva a frase em um contexto formal: 'Tô muito cansado depois do trampo.'", "options": ["Estou muito cansado depois do trabalho.", "Tava muito cansado depois do trampo.", "Estou muito cansado depois do trampo.", "Tô muito cansado depois do trabalho."], "correct": 0},
    {"question": "Leia: 'Antigamente, usava-se 'vós' em vez de 'vocês'.' Qual tipo de variação está sendo descrita?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 1},
    {"question": "Em um contexto informal em Minas Gerais, 'biscoito' pode ser chamado de 'bolacha'. Qual tipo de variação isso representa?", "options": ["Histórica", "Social", "Geográfica", "Situacional"], "correct": 2},
    {"question": "Leia o diálogo: 'Você trouxe o material?' (formal) / 'Cê trouxe o trem?' (informal). Qual tipo de variação está presente?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 3},
    {"question": "Reescreva a frase em um contexto informal típico de Minas Gerais: 'Eu estou com fome.'", "options": ["Eu tô com fome, sô.", "Eu estou com fome, senhor.", "Eu tava com fome.", "Eu tô com fome, meu."], "correct": 0},
    {"question": "Leia: 'O doutor disse que eu preciso de repouso.' (formal). Como ficaria em um contexto informal?", "options": ["O doutor disse que eu preciso de repouso, sô.", "O médico falou que eu preciso descansar.", "O doutor falou que eu preciso de repouso.", "O médico disse que eu preciso de descanso, uai."], "correct": 1},
    {"question": "Qual tipo de variação linguística é observada quando um aluno fala 'tu' com os amigos, mas 'você' com o professor?", "options": ["Geográfica", "Histórica", "Social", "Situacional"], "correct": 3},
    {"question": "Leia: 'Em algumas regiões de Minas, 'mandioca' é chamada de 'macaxeira'.' Qual tipo de variação está presente?", "options": ["Histórica", "Geográfica", "Social", "Situacional"], "correct": 1},
    {"question": "Reescreva a frase em um contexto formal: 'Cê viu o jogo ontem?'", "options": ["Você viu o jogo ontem?", "Tu viu o jogo ontem?", "Ocê viu o jogo ontem?", "Cê viu o jogo ontem, sô?"], "correct": 0},
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