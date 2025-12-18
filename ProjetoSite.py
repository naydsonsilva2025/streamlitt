import streamlit as st
import os
from openai import OpenAI

# ---------------------------------------------------------
# CONFIGURAÇÃO DO APP (sempre a primeira coisa!)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ChatBot - Naydson",
    page_icon="https://static.vecteezy.com/ti/vetor-gratis/p1/23060823-chatgpt-conceito-artificial-inteligencia-chatbot-neon-logotipo-em-preto-fundo-gratis-vetor.jpg"
)
st.write("Olá, venha conversar comigo !");

# ---------------------------------------------------------
# CARREGA SECRET DA OPENAI
# ---------------------------------------------------------
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Inicializa o client (NÃO PASSE api_key AQUI)
client = OpenAI()


# ---------------------------------------------------------
# FUNÇÃO PARA GERAR RESPOSTA COM IA
# ---------------------------------------------------------
def gerar_resposta(prompt):
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return resposta.choices[0].message.content

    except Exception as e:
        return f"❌ Erro ao gerar resposta: {e}"


# ---------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------
def app():

    st.image("image-Photoroom.png", width=50)
    st.title("Chatbot de IA")

    # Histórico
    if "mensagens" not in st.session_state:
        st.session_state["mensagens"] = []

    # Exibe mensagens
    for mensagem in st.session_state["mensagens"]:
        with st.chat_message(mensagem["usuario"]):
            st.markdown(mensagem["texto"])

    # Entrada do usuário
    mensagem_usuario = st.chat_input("Digite aqui sua mensagem...")

    if mensagem_usuario:
        st.session_state["mensagens"].append(
            {"usuario": "user", "texto": mensagem_usuario}
        )

        with st.chat_message("user"):
            st.markdown(mensagem_usuario)

        resposta_texto = gerar_resposta(mensagem_usuario)

        st.session_state["mensagens"].append(
            {"usuario": "assistant", "texto": resposta_texto}
        )

        # ------------ EXIBIÇÃO COM SUPORTE A LATEX BONITO -------------
        with st.chat_message("assistant"):
            resposta = resposta_texto.strip()
            linhas = resposta.split("\n")

            bloco_latex = []
            dentro_do_bloco = False

            for linha in linhas:
                linha_strip = linha.strip()

                # Início de bloco LaTeX com [
                if linha_strip == "[":
                    dentro_do_bloco = True
                    bloco_latex = []
                    continue

                # Fim de bloco LaTeX com ]
                if linha_strip == "]" and dentro_do_bloco:
                    dentro_do_bloco = False
                    conteudo = "\n".join(bloco_latex).strip()
                    st.latex(conteudo)
                    continue

                # Se estiver dentro do bloco, adicionar a linha
                if dentro_do_bloco:
                    bloco_latex.append(linha_strip)
                    continue

                # Linhas isoladas com LaTeX
                if linha_strip.startswith("$") and linha_strip.endswith("$"):
                    st.latex(linha_strip.replace("$", ""))
                elif linha_strip.startswith("$$") and linha_strip.endswith("$$"):
                    st.latex(linha_strip.replace("$$", ""))
                elif linha_strip.startswith(r"\[") and linha_strip.endswith(r"\]"):
                    st.latex(linha_strip[2:-2])
                elif linha_strip.startswith(r"\(") and linha_strip.endswith(r"\)"):
                    st.latex(linha_strip[2:-2])
                else:
                    st.markdown(linha)




# Executa
app()


# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------
st.sidebar.write("# Cadastro")

nome = st.sidebar.text_input("Digite seu nome:")

if nome:
    idade = st.sidebar.slider(
        f"Selecione sua idade, {nome}:",
        min_value=7, max_value=100
    )

    if st.sidebar.button("Selecionar"):
        st.sidebar.success("Armazenado com sucesso!")
        st.sidebar.write(
            f"## Olá, {nome.capitalize()}!\nVenha conversar comigo."
        )

st.sidebar.header("", divider=True)
st.sidebar.header("Informações do desenvolvedor")

st.sidebar.image(
    "Captura de tela 2025-11-15 180148.png",
    caption="Naydson Teixeira Silva",
    width=150
)

st.sidebar.markdown("""
* IDADE : **18 anos**
* CURSANDO : **3° ano do Ensino Médio**
* TELEFONE : **(87) 98105-8522**
* EMAIL : **naydsonsilvaaaa@gmail.com**
* LOCALIDADE : **Volta do Moxoto - Jatoba - PE**
""")

st.sidebar.write("")

# colunas
colunas = st.columns(2)





















