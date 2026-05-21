import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(
    page_title="Julio Almada | Data Portfolio",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Julio Almada")
    st.markdown("📊 Analista de Dados em formação")
    st.markdown("🌎 Buscando vagas remotas")
    st.divider()
    st.markdown("🔗 [GitHub](https://github.com/AlmadaJulio)")
    st.markdown("💼 [LinkedIn](#)")
    st.divider()
    st.caption("Dados via Remotive API · Atualizado em tempo real")

# Buscar dados reais da API
@st.cache_data(ttl=3600)
def load_data():
    categorias = ["data", "engineering", "analytics"]
    todas_vagas = []
    for cat in categorias:
        try:
            r = requests.get(
                "https://remotive.com/api/remote-jobs",
                params={"category": cat, "limit": 50},
                timeout=10
            )
            todas_vagas.extend(r.json().get("jobs", []))
        except:
            pass
    df = pd.DataFrame(todas_vagas)
    if df.empty:
        return pd.DataFrame()
    colunas = ['title', 'company_name', 'category',
               'job_type', 'publication_date', 'url']
    return df[[c for c in colunas if c in df.columns]]

# Header
st.title("📊 Mercado de Trabalho Remoto em Dados")
st.markdown("Análise de vagas remotas em tempo real")
st.divider()

# Carregar dados
with st.spinner("Buscando vagas remotas..."):
    df = load_data()

if df.empty:
    st.error("Não foi possível carregar os dados. Tente novamente.")
    st.stop()

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vagas", len(df))
col2.metric("Empresas Únicas", df['company_name'].nunique())
col3.metric("Categorias", df['category'].nunique())
st.divider()

# Gráfico 1: Top categorias
st.subheader("🏆 Top Categorias")
top_cats = df['category'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(top_cats.index, top_cats.values, color='#845EF7')
ax.set_xlabel("Número de Vagas")
ax.invert_yaxis()
st.pyplot(fig)

# Gráfico 2: Top empresas
st.subheader("🏢 Empresas que Mais Contratam")
top_emp = df['company_name'].value_counts().head(8)
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.barh(top_emp.index, top_emp.values, color='#00C9A7')
ax2.set_xlabel("Número de Vagas")
ax2.invert_yaxis()
st.pyplot(fig2)

# Gráfico 3: Tipo de contrato
st.subheader("📋 Tipo de Contrato")
tipo = df['job_type'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.pie(tipo.values, labels=tipo.index, autopct='%1.1f%%',
        colors=['#845EF7','#00C9A7','#F76707','#1C7ED6'])
st.pyplot(fig3)

# Tabela interativa
st.divider()
st.subheader("🔍 Explorar Vagas")
categoria = st.selectbox(
    "Filtrar por categoria:",
    ["Todas"] + sorted(df['category'].unique().tolist())
)
df_filtrado = df[df['category'] == categoria] if categoria != "Todas" else df

# Tornar título clicável
if 'url' in df_filtrado.columns:
    df_filtrado = df_filtrado.copy()
    df_filtrado['link'] = df_filtrado['url']
    st.dataframe(
        df_filtrado[['title','company_name','category','job_type','publication_date']],
        use_container_width=True
    )
else:
    st.dataframe(df_filtrado, use_container_width=True)

st.caption(f"Mostrando {len(df_filtrado)} vagas · Dados atualizados a cada hora")
