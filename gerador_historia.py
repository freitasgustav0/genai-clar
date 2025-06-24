import streamlit as st
from google import genai

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
        API_KEY = st.secrets["GOOGLE_API_KEY"]   
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
Com base no texto do usuário abaixo, crie **uma História de usuário no padrão JIRA**, usando a estrutura detalhada do exemplo (pilar, what, why, who, stakeholders, dor, critérios INVEST, DOD, principais mudanças etc.).

**Texto do usuário:**  
{entrada_usuario}

Exemplo de história JIRA:
Descrição

Pilar:
[X] CRESCIMENTO;
[  ] SATISFAÇÃO;
[  ] BENEFÍCIOS;
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

DOR (Definition of Ready):

Dependências Técnicas: [detalhar]

Critérios de Aceitação (INVEST): [detalhar]

DOD (Definition of Done): [detalhar]

Principais mudanças e melhorias: [detalhar]

---

Gere apenas a história JIRA, adaptando ao contexto do usuário e preenchendo todos os campos.
Responda em markdown para facilitar a visualização.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        st.markdown("---")
        st.markdown("### Resposta da IA")
        st.markdown(response.text)


