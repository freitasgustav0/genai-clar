import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Gerador de Histórias JIRA", layout="wide")
st.title("Gerador de Histórias JIRA")

st.markdown("""
Preencha um objetivo ou problema de negócio. O app irá gerar automaticamente:
- Uma User Story completa no padrão JIRA

Utilize exemplos reais (ex: “Quero automatizar o KPI de Retido Digital para o dashboard LevelUp Analytics”)!
""")

entrada_usuario = st.text_area("Descreva o objetivo ou problema a ser resolvido:")

if st.button("Gerar história JIRA"):
    if entrada_usuario.strip() == "":
        st.warning("Digite um texto para gerar a história JIRA.")
    else:
        try:
            # Configuração da API
            API_KEY = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel("gemini-1.5-pro")

            # Prompt com estrutura completa
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

            # Chamada ao modelo
            response = model.generate_content(prompt)

            # Exibir resultado
            st.markdown("---")
            st.markdown("### História JIRA Gerada")
            st.markdown(response.text)

        except Exception as e:
            st.error("❌ Erro ao gerar a história JIRA. Tente novamente mais tarde.")
            st.text(f"Detalhes técnicos: {e}")
