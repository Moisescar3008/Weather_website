import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

CSV_FOLDER = "csv"

def generate_graphs(city):
    clean_city = city.replace(" ", "_")
    filename = os.path.join(CSV_FOLDER, f"{clean_city}_weather.csv")

    if not os.path.exists(filename):
        st.error(f"No se encontró el archivo `{filename}`. Asegúrate de haber generado los datos primero.")
        return

    df = pd.read_csv(filename)
    df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"])

    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle(f"Gráficas del Clima en {city}", fontsize=16)

    axes[0, 0].plot(df["Fecha y Hora"], df["Temperatura (°C)"], marker='o', color='r', linestyle='-')
    axes[0, 0].set_title("Temperatura (°C)")
    axes[0, 0].set_xlabel("Fecha y Hora")
    axes[0, 0].set_ylabel("°C")
    axes[0, 0].grid()

    axes[0, 1].plot(df["Fecha y Hora"], df["Presión"], marker='o', color='b', linestyle='-')
    axes[0, 1].set_title("Presión (hPa)")
    axes[0, 1].set_xlabel("Fecha y Hora")
    axes[0, 1].set_ylabel("hPa")
    axes[0, 1].grid()

    axes[1, 0].plot(df["Fecha y Hora"], df["Humedad"], marker='o', color='g', linestyle='-')
    axes[1, 0].set_title("Humedad (%)")
    axes[1, 0].set_xlabel("Fecha y Hora")
    axes[1, 0].set_ylabel("%")
    axes[1, 0].grid()

    axes[1, 1].plot(df["Fecha y Hora"], df["Viento (km/h)"], marker='o', color='purple', linestyle='-')
    axes[1, 1].set_title("Velocidad del Viento (km/h)")
    axes[1, 1].set_xlabel("Fecha y Hora")
    axes[1, 1].set_ylabel("km/h")
    axes[1, 1].grid()

    axes[2, 0].plot(df["Fecha y Hora"], df["Nubosidad (%)"], marker='o', color='orange', linestyle='-')
    axes[2, 0].set_title("Nubosidad (%)")
    axes[2, 0].set_xlabel("Fecha y Hora")
    axes[2, 0].set_ylabel("%")
    axes[2, 0].grid()

    axes[2, 1].plot(df["Fecha y Hora"], df["Lluvia (mm)"], marker='o', color='cyan', linestyle='-')
    axes[2, 1].set_title("Precipitación (mm)")
    axes[2, 1].set_xlabel("Fecha y Hora")
    axes[2, 1].set_ylabel("mm")
    axes[2, 1].grid()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    st.pyplot(fig)

