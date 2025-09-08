import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Predicción Serie A", layout="wide")
st.title("⚽ Predicción Serie A 2025")
st.write("Bienvenido al dashboard de análisis y predicción.")

# Cargar datos
df_pred = pd.read_csv("data/prediccion_serie_a_2025.csv")
df_extra = pd.read_csv("data/serie_a_2024_procesado.csv")

# Clasificación y zona
df_pred["Clasificación"] = df_pred["Puntos_Predichos_2025"].rank(ascending=False).astype(int)
df_pred.sort_values("Clasificación", inplace=True)

def zona_tabla(pos):
    if pos <= 4:
        return "Champions League"
    elif pos <= 6:
        return "Europa League"
    elif pos >= 18:
        return "Descenso"
    else:
        return "Media Tabla"

df_pred["Zona"] = df_pred["Clasificación"].apply(zona_tabla)

# Filtros
zona = st.sidebar.selectbox("📌 Zona de tabla", ["Todas"] + df_pred["Zona"].unique().tolist())
equipo = st.sidebar.selectbox("🔍 Equipo", ["Todos"] + df_pred["Equipo"].tolist())

df_vista = df_pred.copy()
if zona != "Todas":
    df_vista = df_vista[df_vista["Zona"] == zona]
if equipo != "Todos":
    df_vista = df_vista[df_vista["Equipo"] == equipo]

# Tabla de predicción
st.subheader("📋 Tabla de Predicción")
st.dataframe(df_vista.style.format({"Puntos_Predichos_2025": "{:.2f}"}))

# Gráfico de ranking
if equipo == "Todos":
    st.subheader("📈 Ranking de Equipos")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Puntos_Predichos_2025", y="Equipo", data=df_vista, hue="Zona", dodge=False, palette="Set2", ax=ax)
    ax.set_title("Predicción de Puntos Serie A 2025/2026")
    st.pyplot(fig)

# Panel individual
if equipo != "Todos":
    st.subheader(f"📊 Panel del equipo: {equipo}")
    equipo_data = df_extra[df_extra["Equipo"] == equipo].iloc[0]
    st.metric("Goles", equipo_data["Goles"])
    st.metric("Goles en Contra", equipo_data["Goles_Contra"])
    st.metric("Eficiencia Ofensiva", f"{equipo_data['Eficiencia_Ofensiva']:.2f}")
    st.metric("Eficiencia Defensiva", f"{equipo_data['Eficiencia_Defensiva']:.2f}")
    st.metric("Posesión", f"{equipo_data['Posesion']:.1f}%")
    st.metric("Pases Precisos", f"{equipo_data['Pases_Precisos']:.1f}%")

# Matriz de correlaciones
st.subheader("📊 Matriz de Correlaciones")
columnas_corr = ["Goles", "Goles_Contra", "Posesion", "Pases_Precisos", "Eficiencia_Ofensiva", "Eficiencia_Defensiva"]
df_corr = df_extra[columnas_corr].
