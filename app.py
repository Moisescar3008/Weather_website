import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()  
api_k = os.getenv("OPENWEATHER_API_KEY")

# Título de la app
st.title("📊 Clima en las Ciudades de México")

# Lista de ciudades importantes en México
cities = [
    "Aguascalientes", "Mexicali", "La Paz", "Campeche", "Saltillo", "Colima", "Tuxtla Gutiérrez", "Chihuahua",
    "Ciudad de México", "Durango", "León", "Acapulco", "Pachuca", "Guadalajara", "Toluca", "Morelia", "Cuernavaca",
    "Tepic", "Monterrey", "Oaxaca", "Puebla", "Querétaro", "Chetumal", "San Luis Potosí", "Culiacán",
    "Hermosillo", "Villahermosa", "Ciudad Victoria", "Tlaxcala", "Xalapa", "Mérida", "Zacatecas"
]

# Función para convertir temperatura de Kelvin a Celsius
def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

# Selector de ciudad en Streamlit
city = st.selectbox("Selecciona una ciudad:", cities)

if st.button("Obtener Clima"):
    clean_city = re.sub(r'[^\w\s-]', '', city).replace(' ', '_')
    
    # Construir la URL de la API
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=40&appid={api_k}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        lat = data['city']['coord']['lat']
        lon = data['city']['coord']['lon']
        weather_data = []

        for hour in data['list']:
            date_time = datetime.utcfromtimestamp(hour['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = kelvin_to_celsius(hour['main']['feels_like'])
            pressure = hour['main']['pressure']
            humidity = hour['main']['humidity']
            weather_main = hour['weather'][0]['main']
            weather_description = hour['weather'][0]['description']
            wind_speed = hour['wind']['speed']
            wind_direction = hour['wind']['deg']
            cloudiness = hour['clouds']['all']
            rain_volume = hour.get('rain', {}).get('3h', 0)
            snow_volume = hour.get('snow', {}).get('3h', 0)

            weather_data.append({
                "Fecha y Hora": date_time,
                "Temperatura (°C)": temp,
                "Presión": pressure,
                "Humedad": humidity,
                "Clima": weather_main,
                "Descripción": weather_description,
                "Viento (km/h)": wind_speed,
                "Dirección del Viento": wind_direction,
                "Nubosidad (%)": cloudiness,
                "Lluvia (mm)": rain_volume,
                "Nieve (mm)": snow_volume
            })

        # Convertir a DataFrame
        df = pd.DataFrame(weather_data)

        # Mostrar tabla en Streamlit
        st.subheader(f"📌 Datos del Clima en {city}")
        st.dataframe(df)

        # Guardar en CSV
        csv_folder = "csv"
        filename = os.path.join(csv_folder, f"{clean_city}_weather.csv")

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        df.to_csv(filename, index=False, encoding="utf-8")
        st.success(f"Datos guardados en `{filename}`")

        st.success(f"Datos guardados en `{filename}`")

    else:
        st.error(f"No se pudo obtener el clima de {city}. Código de error: {response.status_code}")