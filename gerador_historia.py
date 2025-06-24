import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gerador de Histórias e Demandas", layout="wide")
st.title("Gerador de Histórias JIRA + Demandas Pipefy (Gemini)")

st.markdown("""
Preencha um objetivo ou problema de negócio. O app irá gerar automaticamente:
- Uma User Story completa no padrão JIRA
- Uma demanda Pipefy preenchida, pronta para uso

Utilize exemplos reais (ex: “Quero automatizar o KPI de Retido Digital para o dashboard LevelUp Analytics”)!
""")

entrada_usuario = st.text_area("Descreva o objetivo ou problema a ser resolvido:")

if st.button("Gerar história e demanda"):
    if entrada_usuario.strip() == "":
        st.warning("Digite um texto para gerar a história e a demanda.")
    else:
        # Configure a API Key do Gemini de forma segura
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

        prompt = f"""


Com base no texto do usuário abaixo, crie **DUAS respostas automáticas**:
1. **História de usuário no padrão JIRA**, usando a estrutura detalhada do exemplo (pilar, what, why, who, stakeholders, dor, critérios INVEST, DOD, principais mudanças etc.).
2. **Demanda no padrão Pipefy**, preenchida como no exemplo (Squad, Email, Tipo de Solicitação, Tipo de Demanda, Prioridade, Descrição da Solicitação, Motivo da Solicitação, Expectativa de Entrega).

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

Exemplo de Demanda Pipefy:
Solicitação de: Lyriam Milesi  
Squad: MCM | APP  
Email: usuario@teste.com.br  
Tipo de Solicitação: Analytics - Análises de dados  
Tipo de Demanda: Pesquisa de dados  
Prioridade: Importante  
Descrição da Solicitação: Precisamos saber o volume de Usuários únicos por segmento no App e Site.  
Motivo da Solicitação: Marketing precisa dessa volumetria para propor campanhas de incentivo para o Auto Atendimento  
Expectativa de Entrega: 31/10/2023

---

Gere as duas respostas AUTOMATICAMENTE, com todos os campos preenchidos, adaptando ao contexto do usuário.

Responda em markdown para facilitar a visualização.
"""
        model = genai.GenerativeModel('gemini-pro')
        resposta = model.generate_content(prompt)
        
        st.markdown("---")
        st.markdown("### Resposta da IA")
        st.markdown(resposta.text)

st.info("Este app usa a API do Google Gemini para gerar histórias de usuário e demandas Pipefy automaticamente.")
