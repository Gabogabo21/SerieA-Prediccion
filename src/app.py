# app.py - Predicción Serie A 2026 - VERSIÓN CORREGIDA
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Predicción Serie A 2026", 
    page_icon="⚽", 
    layout="wide"
)

st.title("⚽ Predicción Serie A 2026")
st.write("Bienvenido al dashboard de análisis y predicción.")

# Cargar datos con manejo de errores
@st.cache_data
# Cargar datos predefinidos (sin intentar cargar archivos)
@st.cache_data
def load_data():
    # Datos predefinidos para Serie A
    equipos_serie_a = [
        'Inter', 'Juventus', 'Milan', 'Napoli', 'Atalanta', 'Roma', 
        'Lazio', 'Fiorentina', 'Bologna', 'Torino', 'Monza', 'Genoa',
        'Lecce', 'Sassuolo', 'Frosinone', 'Verona', 'Empoli', 'Cagliari',
        'Udinese', 'Salernitana'
    ]
    
    # Datos de predicción 2026
    puntos_predichos = [85.2, 78.5, 76.8, 74.3, 71.6, 68.9, 66.4, 63.7, 61.2, 58.5, 
                       55.8, 53.1, 50.4, 47.7, 45.0, 42.3, 39.6, 36.9, 34.2, 31.5]
    
    df_pred = pd.DataFrame({
        'Equipo': equipos_serie_a,
        'Puntos_Predichos_2026': puntos_predichos
    })
    
    # Datos de temporada actual
    datos_extra = {
        'Goles': [75, 68, 72, 65, 70, 63, 60, 58, 55, 52, 48, 45, 42, 40, 38, 35, 32, 30, 28, 25],
        'Goles_Contra': [25, 30, 35, 32, 38, 40, 36, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70, 75],
        'Posicion': range(1, 21),
        'Posesion': [65.2, 58.7, 61.3, 59.8, 57.6, 55.4, 54.2, 52.8, 51.3, 49.7, 
                    48.5, 47.2, 46.1, 45.3, 44.2, 43.5, 42.7, 41.9, 40.8, 39.5],
        'Pases_Precisos': [88.5, 85.2, 86.8, 84.7, 83.1, 82.3, 81.6, 80.9, 79.4, 78.2,
                          77.1, 76.3, 75.4, 74.6, 73.8, 72.9, 71.8, 70.6, 69.7, 68.3]
    }
    
    df_extra = pd.DataFrame(datos_extra)
    df_extra['Equipo'] = equipos_serie_a
    
    return df_pred, df_extra
    except:
        # Crear datos de ejemplo si los archivos no existen
        st.warning("⚠️ No se encontraron archivos CSV. Usando datos de ejemplo.")
        
        # Crear datos de predicción de ejemplo
        equipos_serie_a = [
            'Inter', 'Juventus', 'Milan', 'Napoli', 'Atalanta', 'Roma', 
            'Lazio', 'Fiorentina', 'Bologna', 'Torino', 'Monza', 'Genoa',
            'Lecce', 'Sassuolo', 'Frosinone', 'Verona', 'Empoli', 'Cagliari',
            'Udinese', 'Salernitana'
        ]
        
        np.random.seed(42)
        
        # Datos de predicción
        df_pred = pd.DataFrame({
            'Equipo': equipos_serie_a,
            'Puntos_Predichos_2026': np.random.uniform(40, 85, len(equipos_serie_a))
        })
        
        # Datos extra de ejemplo
        df_extra = pd.DataFrame({
            'Equipo': equipos_serie_a,
            'Goles': np.random.randint(30, 80, len(equipos_serie_a)),
            'Goles_Contra': np.random.randint(25, 70, len(equipos_serie_a)),
            'Posicion': range(1, len(equipos_serie_a) + 1),
            'Posesion': np.random.uniform(45, 65, len(equipos_serie_a)),
            'Pases_Precisos': np.random.uniform(75, 90, len(equipos_serie_a))
        })
        
        return df_pred, df_extra

# Cargar datos
df_pred, df_extra = load_data()

# Procesar datos de predicción
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

# Sidebar
st.sidebar.title("⚙️ Configuración")

# Filtros
zona_seleccionada = st.sidebar.selectbox(
    "📌 Filtrar por zona de tabla", 
    ["Todas"] + df_pred["Zona"].unique().tolist()
)

equipo_seleccionado = st.sidebar.selectbox(
    "🔍 Selecciona un equipo", 
    ["Todos"] + df_pred["Equipo"].tolist()
)

# Aplicar filtros
df_vista = df_pred.copy()
if zona_seleccionada != "Todas":
    df_vista = df_vista[df_vista["Zona"] == zona_seleccionada]
if equipo_seleccionado != "Todos":
    df_vista = df_vista[df_vista["Equipo"] == equipo_seleccionado]

# Mostrar tabla de predicción
st.subheader("📋 Tabla de Predicción Serie A 2026")

# Formatear la tabla para mejor visualización
df_display = df_vista[['Clasificación', 'Equipo', 'Puntos_Predichos_2026', 'Zona']].copy()
df_display['Puntos_Predichos_2026'] = df_display['Puntos_Predichos_2026'].round(2)

st.dataframe(
    df_display,
    use_container_width=True,
    column_config={
        "Clasificación": st.column_config.NumberColumn(format="%d"),
        "Puntos_Predichos_2026": st.column_config.NumberColumn(format="%.2f")
    }
)

# Gráfico de ranking
if equipo_seleccionado == "Todos":
    st.subheader("📈 Ranking de Equipos por Puntos Estimados")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Ordenar para el gráfico
    df_grafico = df_vista.sort_values('Puntos_Predichos_2026', ascending=True)
    
    # Crear gráfico de barras
    bars = ax.barh(df_grafico['Equipo'], df_grafico['Puntos_Predichos_2026'], 
                   color=['#1f77b4' if zona != 'Descenso' else '#ff7f0e' for zona in df_grafico['Zona']])
    
    ax.set_xlabel('Puntos Estimados')
    ax.set_title('Predicción de Puntos - Serie A 2026')
    ax.grid(axis='x', alpha=0.3)
    
    # Añadir valores en las barras
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)

# Panel individual del equipo
if equipo_seleccionado != "Todos":
    st.subheader(f"📊 Panel Detallado: {equipo_seleccionado}")
    
    # Buscar datos del equipo
    equipo_pred_data = df_pred[df_pred["Equipo"] == equipo_seleccionado].iloc[0]
    equipo_extra_data = df_extra[df_extra["Equipo"] == equipo_seleccionado]
    
    if not equipo_extra_data.empty:
        equipo_extra_data = equipo_extra_data.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏆 Clasificación Predicha", f"#{int(equipo_pred_data['Clasificación'])}")
            st.metric("📈 Puntos Estimados", f"{equipo_pred_data['Puntos_Predichos_2026']:.1f}")
            st.metric("🎯 Zona", equipo_pred_data['Zona'])
        
        with col2:
            if 'Goles' in equipo_extra_data:
                st.metric("⚽ Goles", int(equipo_extra_data['Goles']))
            if 'Goles_Contra' in equipo_extra_data:
                st.metric("🛡️ Goles en Contra", int(equipo_extra_data['Goles_Contra']))
            if 'Posicion' in equipo_extra_data:
                st.metric("📊 Posición Actual", f"#{int(equipo_extra_data['Posicion'])}")
        
        with col3:
            if 'Posesion' in equipo_extra_data:
                st.metric("🎮 Posesión", f"{equipo_extra_data['Posesion']:.1f}%")
            if 'Pases_Precisos' in equipo_extra_data:
                st.metric("🎯 Pases Precisos", f"{equipo_extra_data['Pases_Precisos']:.1f}%")
    else:
        st.info("ℹ️ No hay datos adicionales disponibles para este equipo.")

# Matriz de Correlaciones
st.subheader("📊 Análisis de Correlaciones")

# Preparar datos para correlación
columnas_interes = ['Goles', 'Goles_Contra', 'Posicion', 'Posesion', 'Pases_Precisos']
columnas_disponibles = [col for col in columnas_interes if col in df_extra.columns]

if len(columnas_disponibles) >= 2:
    # Calcular métricas adicionales
    if 'Goles' in df_extra.columns and 'Pases_Precisos' in df_extra.columns:
        df_extra["Eficiencia_Ofensiva"] = df_extra["Goles"] / df_extra["Pases_Precisos"]
        columnas_disponibles.append("Eficiencia_Ofensiva")
    
    if 'Goles_Contra' in df_extra.columns and 'Posesion' in df_extra.columns:
        df_extra["Eficiencia_Defensiva"] = df_extra["Goles_Contra"] / df_extra["Posesion"].replace(0, 1)
        columnas_disponibles.append("Eficiencia_Defensiva")
    
    # Calcular matriz de correlación
    df_corr = df_extra[columnas_disponibles].dropna()
    
    if not df_corr.empty and len(df_corr.columns) > 1:
        corr = df_corr.corr()
        
        # Crear heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", center=0, ax=ax)
        ax.set_title("Matriz de Correlaciones - Serie A")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No hay suficientes datos para calcular correlaciones.")
else:
    st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones.")

# Información adicional
st.sidebar.markdown("---")
st.sidebar.info("""
**💡 Acerca de esta app:**
- Predicciones basadas en datos históricos
- Análisis de rendimiento por equipo
- Proyección temporada 2026
""")

# Footer
st.markdown("---")
st.caption("Desarrollado con Streamlit | Datos de demostración para análisis predictivo")

