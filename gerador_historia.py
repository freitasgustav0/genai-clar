import streamlit as st
import google.generativeai as genai
import openai
import time
import requests

# === Função para rodar modelo local com Ollama ===
def gerar_historia_ollama(prompt, modelo="mistral"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": modelo, "prompt": prompt, "stream": False},
            timeout=60
        )
        resposta = response.json()["response"]
        return resposta
    except Exception as erro:
        return f"Erro com modelo local: {erro}"

# === Interface do Streamlit ===
st.set_page_config(page_title="Gerador de Histórias JIRA", layout="wide")
st.title("Gerador de Histórias JIRA")

st.markdown("""
Preencha um objetivo ou problema de negócio. O app irá gerar automaticamente:
- Uma User Story completa no padrão JIRA

Exemplo: “Quero automatizar o KPI de Retido Digital para o dashboard LevelUp Analytics”
""")

entrada_usuario = st.text_area("Descreva o objetivo ou problema a ser resolvido:")

if st.button("Gerar história JIRA"):
    if not entrada_usuario.strip():
        st.warning("Digite um texto para gerar a história JIRA.")
    else:
        # === Prompt estruturado ===
        prompt = f"""
Você é um Product Owner renomado no mundo inteiro que atua na área de Analytics, absorva todo o conhecimento neste assunto e também os conceitos da metodologia ágil.

Este P.O precisa criar histórias e precisa seguir o modelo abaixo:

Exemplo de história JIRA:

Descrição  
Pilar:  
[X] CRESCIMENTO  
[ ] SATISFAÇÃO  
[ ] BENEFÍCIOS  
________________________________________  

Eu, como gestor de autoatendimento,  

What (o que?): desejo um fluxo automatizado de atualização semanal do KPI Retido Digital no dashboard do LevelUp Analytics.  

Why (por quê?): para acompanhar o desempenho dos OKRs estratégicos de autoatendimento com dados atualizados e tomar decisões mais assertivas.  
________________________________________  

Estrutura Detalhada:  

What (o que?): Implementar um fluxo automatizado para atualizar semanalmente o KPI Retido Digital no dashboard do LevelUp Analytics.  
Why (por quê?): Permitir o acompanhamento preciso do desempenho dos OKRs estratégicos de autoatendimento, facilitando a tomada de decisões baseadas em dados atualizados.  
Who (quem?): Gestor de autoatendimento  

Stakeholders - Gestor de autoatendimento, time de desenvolvimento, analista de negócios.  
Consumidores - Time de autoatendimento, gestores de produto.  

DOR (Definition of Ready): [detalhar]  
Critérios de Aceitação (INVEST): [detalhar]  
DOD (Definition of Done): [detalhar]  
Principais mudanças e melhorias: [detalhar]  

**Texto do usuário:**  
{entrada_usuario}  

Gere apenas a história JIRA, adaptando ao contexto do usuário e preenchendo todos os campos.  
Responda em markdown para facilitar a visualização.
"""

        # === Tenta com Gemini ===
        try:
            st.info("⏳ Gerando com Gemini (Google)...")
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-pro")

            start = time.time()
            response = model.generate_content(prompt)
            elapsed = time.time() - start

            if elapsed > 12:
                raise TimeoutError("Tempo de resposta excedido. Ativando fallback.")

            st.success("✅ História gerada com Gemini!")
            st.markdown("### História JIRA (via Gemini)")
            st.markdown(response.text)

        # === Fallback: OpenRouter GPT ===
        except Exception as e1:
            st.warning("⚠️ Falha com Gemini. Tentando OpenRouter...")

            try:
                client = openai.OpenAI(
                    api_key=st.secrets["OPENROUTER_API_KEY"],
                    base_url="https://openrouter.ai/api/v1"
                )

                response = client.chat.completions.create(
                    model="openchat/openchat-7b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )

                historia = response.choices[0].message.content
                st.success("✅ História gerada com OpenChat 7B!")
                st.markdown("### História JIRA (via OpenRouter - OpenChat 7B)")
                st.markdown(historia)

            # === Fallback final: Modelo local via Ollama ===
            except Exception as e2:
                st.warning("⚠️ Falha também com OpenRouter. Usando modelo local via Ollama...")

                historia = gerar_historia_ollama(prompt, modelo="mistral")
                st.success("✅ História gerada com Mistral local!")
                st.markdown("### História JIRA (via Mistral - local)")
                st.markdown(historia)
