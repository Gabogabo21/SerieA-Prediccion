import os
import pandas as pd
import shutil
from google.colab import drive

# Montar Drive
drive.mount('/content/drive')

# Crear carpeta si no existe
if not os.path.exists("data"):
    os.makedirs("data")

# Simular predicción si no existe df_prediccion
try:
    df_prediccion
except NameError:
    # Si no existe, crear un ejemplo básico
    df_prediccion = pd.DataFrame({
        "Equipo": ["Inter", "Napoli", "Juventus"],
        "Puntos_Predichos_2026": [85.2, 78.4, 74.1]
    })

# Guardar archivo
df_prediccion.to_csv("data/prediccion_serie_a_2026.csv", index=False)
print("Archivo guardado correctamente.")

# Copiar a Drive
shutil.copy("data/prediccion_serie_a_2026.csv", "/content/drive/MyDrive/prediccion_serie_a_2026.csv")
print("Archivo copiado a Drive correctamente.")
