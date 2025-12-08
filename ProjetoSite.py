# arquivo: debug_openai_streamlit.py (substitua temporariamente no app)
import streamlit as st
import os
import traceback
import time

# 0) show top instruction
st.title("DEBUG: verificar OPENAI secret e conexão")

# 1) mostrar se secrets existe (não mostre a chave inteira)
try:
    secret = st.secrets.get("OPENAI_API_KEY", None)
    st.write("secrets carregado?:", secret is not None)
    if secret is not None:
        # mostrar apenas começo e fim para confirmar que é completa (sem expor tudo)
        st.write("preview da key:", secret[:8] + "..." + secret[-6:])
        st.write("tamanho da key (caracteres):", len(secret))
    else:
        st.error("st.secrets['OPENAI_API_KEY'] é None — verifique painel Secrets no Streamlit Cloud.")
except Exception as e:
    st.error("Erro lendo st.secrets: " + str(e))
    st.text(traceback.format_exc())

# 2) setar variável de ambiente ANTES de importar client (faz aqui antes de qualquer import da SDK)
if secret:
    os.environ["OPENAI_API_KEY"] = secret
    st.write("Variável de ambiente OPENAI_API_KEY definida no processo.")

# 3) importar OpenAI AGORA (depois de setar env)
try:
    from openai import OpenAI
    st.write("OpenAI SDK importado com sucesso.")
except Exception as e:
    st.error("Erro ao importar OpenAI SDK: " + str(e))
    st.text(traceback.format_exc())
    st.stop()

# 4) inicializar client sem api_key= (deixe a lib usar env)
try:
    client = OpenAI()
    st.write("Cliente OpenAI inicializado (instância criada).")
except Exception as e:
    st.error("Erro ao criar client = OpenAI(): " + str(e))
    st.text(traceback.format_exc())
    st.stop()

# 5) Fazer uma requisição de teste (curta) para ver se a key funciona
if st.button("Fazer requisição de teste à API"):
    with st.spinner("Chamando OpenAI..."):
        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": "Diga olá em uma frase curta."}],
                max_tokens=20
            )
            st.success("Requisição OK")
            # mostrar parte da resposta
            content = resp.choices[0].message.content
            st.write("Resposta:", content)
            st.write("Raw:", resp)
        except Exception as e:
            st.error("Erro na chamada API: " + str(e))
            st.text(traceback.format_exc())

