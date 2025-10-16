%%writefile app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Predicción Serie A 2026", layout="wide")
st.title("⚽ Predicción Serie A 2026")
st.write("Bienvenido al dashboard de análisis y predicción.")

# Cargar datos
df_pred = pd.read_csv("data/prediccion_serie_a_2026.csv")
df_extra = pd.read_csv("data/serie_a_2024_procesado.csv")

# Clasificación proyectada
df_pred["Clasificación"] = df_pred["Puntos_Predichos_2026"].rank(ascending=False, method="min").astype(int)
df_pred.sort_values("Clasificación", inplace=True)

# Zonas de tabla
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
zona_seleccionada = st.sidebar.selectbox("📌 Filtrar por zona de tabla", ["Todas"] + df_pred["Zona"].unique().tolist())
equipo_seleccionado = st.sidebar.selectbox("🔍 Selecciona un equipo", ["Todos"] + df_pred["Equipo"].tolist())

# Aplicar filtros
df_vista = df_pred.copy()
if zona_seleccionada != "Todas":
    df_vista = df_vista[df_vista["Zona"] == zona_seleccionada]
if equipo_seleccionado != "Todos":
    df_vista = df_vista[df_vista["Equipo"] == equipo_seleccionado]

# Mostrar tabla
st.subheader("📋 Tabla de Predicción")
st.dataframe(df_vista.style.format({"Puntos_Predichos_2026": "{:.2f}"}))

# Ranking visual
if equipo_seleccionado == "Todos":
    st.subheader("📈 Ranking de Equipos por Puntos Estimados")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Puntos_Predichos_2026", y="Equipo", data=df_vista, hue="Zona", dodge=False, palette="Set2", ax=ax)
    ax.set_title("Predicción de Puntos Serie A 2026/2026")
    ax.set_xlabel("Puntos Estimados")
    st.pyplot(fig)

# Panel individual
if equipo_seleccionado != "Todos":
    st.subheader(f"📊 Panel del equipo: {equipo_seleccionado}")
    equipo_data = df_extra[df_extra["Equipo"] == equipo_seleccionado].iloc[0]
    st.metric("Goles", equipo_data["Goles"])
    st.metric("Goles en Contra", equipo_data["Goles_Contra"])
    st.metric("Eficiencia Ofensiva", f"{equipo_data['Eficiencia_Ofensiva']:.2f}")
    st.metric("Eficiencia Defensiva", f"{equipo_data['Eficiencia_Defensiva']:.2f}")
    st.metric("Posesión", f"{equipo_data['Posesion']:.1f}%")
    st.metric("Pases Precisos", f"{equipo_data['Pases_Precisos']:.1f}%")

# 📊 Matriz de Correlaciones con verificación de columnas
st.subheader("📊 Matriz de Correlaciones")

# Crear métricas si no existen
if "Eficiencia_Ofensiva" not in df_extra.columns:
    if "Goles" in df_extra.columns and "Pases_Precisos" in df_extra.columns:
        df_extra["Eficiencia_Ofensiva"] = df_extra["Goles"] / df_extra["Pases_Precisos"]

if "Eficiencia_Defensiva" not in df_extra.columns:
    if "Goles_Contra" in df_extra.columns and "Posesion" in df_extra.columns:
        df_extra["Eficiencia_Defensiva"] = df_extra["Goles_Contra"] / df_extra["Posesion"]

# Lista de columnas esperadas
columnas_deseadas = [
    "Goles", "Goles_Contra", "Posicion",
    "Eficiencia_Ofensiva", "Eficiencia_Defensiva",
    "Posesion", "Pases_Precisos"
]

# Filtrar columnas disponibles
columnas_disponibles = [col for col in columnas_deseadas if col in df_extra.columns]

# ⚠️ Avisar si faltan columnas
faltantes = [col for col in columnas_deseadas if col not in df_extra.columns]
if faltantes:
    print(f"⚠️ Columnas no disponibles para la matriz: {faltantes}")

# Calcular matriz de correlación
df_corr = df_extra[columnas_disponibles].dropna()
corr = df_corr.corr()

# Visualizar
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
st.pyplot(fig3)

