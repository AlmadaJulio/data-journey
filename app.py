import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Julio Almada | Data Portfolio",
    page_icon="📊",
    layout="wide"
)

# Sidebar com perfil
with st.sidebar:
    st.title("Julio Almada")
    st.markdown("📊 Analista de Dados em formação")
    st.markdown("🌎 Buscando vagas remotas")
    st.divider()
    st.markdown("🔗 [GitHub](https://github.com/julioalmada)")
    st.markdown("💼 [LinkedIn](#)")
    st.divider()
    st.caption("Dados via Remotive API")

# Header
st.title("📊 Mercado de Trabalho Remoto em Dados")
st.markdown("Análise de vagas remotas em tempo real")
st.divider()

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/vagas_remotas.csv")
    return df

df = load_data()

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vagas", len(df))
col2.metric("Empresas Únicas", df['company_name'].nunique())
col3.metric("Categorias", df['category'].nunique())

st.divider()

# Gráfico: Top categorias
st.subheader("🏆 Top Categorias")
top_cats = df['category'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(top_cats.index, top_cats.values, color='#845EF7')
ax.set_xlabel("Número de Vagas")
st.pyplot(fig)

# Tabela interativa
st.subheader("🔍 Explorar Vagas")
categoria = st.selectbox("Filtrar por categoria:", ["Todas"] + list(df['category'].unique()))
df_filtrado = df[df['category'] == categoria] if categoria != "Todas" else df
st.dataframe(df_filtrado, use_container_width=True)
