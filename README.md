# ⚽ Predicción Serie A 2026

Dashboard interactivo para visualizar y analizar predicciones de puntos en la Serie A italiana, basado en métricas ofensivas, defensivas y de posesión.

## 🚀 ¿Qué incluye?

- Visualización de ranking proyectado por puntos
- Panel individual por equipo con métricas clave
- Matriz de correlaciones entre variables
- Filtros por zona de tabla y equipo

## 📊 Datos utilizados

- `serie_a_2024.csv`: Datos originales extraídos manualmente
- `serie_a_2024_procesado.csv`: Datos procesados con nuevas métricas
- `prediccion_serie_a_2026.csv`: Resultados del modelo de regresión lineal

## 🧠 Modelo

Se utiliza regresión lineal para estimar los puntos proyectados en base a:

- Goles a favor y en contra
- Posesión
- Precisión de pases
- Eficiencia ofensiva y defensiva


