import streamlit as st
import requests

def gerar_resposta(prompt):
    try:
        # Faz a requisição para o servidor local do Ollama
        resposta = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi", "prompt": prompt},
            timeout=60  # tempo máximo de espera (em segundos)
        )

        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get("response", "❌ Sem resposta gerada.")
        else:
            return f"❌ Erro {resposta.status_code}: {resposta.text}"

    except requests.exceptions.ConnectionError:
        return "⚠️ O Ollama não está rodando. Abra o aplicativo Ollama e tente novamente."
    except Exception as e:
        return f"❌ Erro inesperado: {e}"


# titulo
def app():

    st.set_page_config(
    page_title="ChatBot - Naydson",
    page_icon=r"https://static.vecteezy.com/ti/vetor-gratis/p1/23060823-chatgpt-conceito-artificial-inteligencia-chatbot-neon-logotipo-em-preto-fundo-gratis-vetor.jpg",  # caminho do seu favicon
    )

    st.image(
        image="image-Photoroom.png",
        width=50
    )
    st.title("Chatbot de IA")
    # Inicializa o histórico de mensagens
    if "mensagens" not in st.session_state:
        st.session_state["mensagens"] = []

    # Mostrar as mensagens anteriores
    for mensagem in st.session_state["mensagens"]:
        with st.chat_message(mensagem["usuario"]):
            st.markdown(mensagem["texto"])

    # Entrada do usuário
    mensagem_usuario = st.chat_input("Digite aqui sua mensagem...")

    if mensagem_usuario:
        # Exibe a mensagem do usuário
        st.session_state["mensagens"].append({"usuario": "user", "texto": mensagem_usuario})
        with st.chat_message("user"):
            st.markdown(mensagem_usuario)

            # Gera resposta com o Ollama (modelo phi)
        resposta_texto = gerar_resposta(mensagem_usuario)

        # Exibe a resposta do assistente
        st.session_state["mensagens"].append({"usuario": "assistant", "texto": resposta_texto})
        with st.chat_message("assistant"):
            st.markdown(resposta_texto)

app()


# barra lateral
st.sidebar.write("# Cadastro")

nome = st.sidebar.text_input(label="Digite seu nome: ", )
if nome:
    valor_slide = st.sidebar.slider(
            label=f"Selecione sua idade {nome}: ",
            min_value=7,
            max_value=100
        )
    
    if st.sidebar.button("Selecionar"):
        st.sidebar.success("Armazenado com sucesso !")
        if valor_slide:
            st.sidebar.write(f"## Olá, **{nome.capitalize()}**!\nVenha conversar comigo.")


    
st.sidebar.header("", divider=True) 
st.sidebar.header("Informações do meu desenvolvedor")
st.sidebar.image(
    image="Captura de tela 2025-11-15 180148.png",

    caption="Naydson Teixeira Silva",

    width=150
)

st.sidebar.markdown("""
* IDADE : **18 anos**
* CURSANDO : **Ensino Médio**
* TELEFONE : **(87) 98105-8522**
* EMAIL : **naydsonsilvaaaa@gmail.com**
* LOCALIDADE : **Volta do Moxoto - Jatoba - PE**
""")


st.sidebar.write("")

# colunas

colunas = st.columns(2)
