import streamlit as st
import google.generativeai as genai
import openai
import time

# Configuração da página
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
        # PROMPT COMPLETO COM A ESTRUTURA ORIGINAL
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

        # Primeiro tenta com Gemini
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

        # Se falhar, usa OpenRouter (GPT-3.5)
        except Exception as e:
            st.warning("⚠️ Falha com Gemini. Usando GPT-3.5 (via OpenRouter) como alternativa...")

            try:
                client = openai.OpenAI(
                    api_key=st.secrets["OPENROUTER_API_KEY"],
                    base_url="https://openrouter.ai/api/v1"
                )

                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )

                historia = response.choices[0].message.content
                st.success("✅ História gerada com GPT-3.5!")
                st.markdown("### História JIRA (via OpenRouter)")
                st.markdown(historia)

            except Exception as err:
                st.error("❌ Falha também no modelo alternativo.")
                st.text(f"Erro: {err}")
