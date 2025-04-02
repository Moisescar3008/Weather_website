import json
import requests
import pandas as pd
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()  

api_k = os.getenv("OPENWEATHER_API_KEY")  # Obtiene la API Key

# Diccionario con la ciudad más importante de cada estado de México
cities = [
    "Aguascalientes", "Mexicali", "La Paz", "Campeche", "Saltillo", "Colima", "Tuxtla Gutiérrez", "Chihuahua",
    "Ciudad de México", "Durango", "León", "Acapulco", "Pachuca", "Guadalajara", "Toluca", "Morelia", "Cuernavaca",
    "Tepic", "Monterrey", "Oaxaca", "Puebla", "Querétaro", "Chetumal", "San Luis Potosí", "Culiacán",
    "Hermosillo", "Villahermosa", "Ciudad Victoria", "Tlaxcala", "Xalapa", "Mérida", "Zacatecas"
]

# Función para convertir temperatura de Kelvin a Celsius
def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

# Crear directorio si no existe
if not os.path.exists("csv"):
    os.makedirs("csv")

# Iterar sobre cada ciudad
for city in cities:
    clean_city = re.sub(r'[^\w\s-]', '', city).replace(' ', '_')
    
    # Aquí se define el nombre del archivo para cada ciudad
    filename = os.path.join("csv", f"{clean_city}_weather.csv")

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
                "DateTime": date_time,
                "Latitude": lat,
                "Longitude": lon,
                "Temperature (C)": temp,
                "Pressure": pressure,
                "Humidity": humidity,
                "Weather": weather_main,
                "Weather description": weather_description,
                "Wind speed": wind_speed,
                "Wind direction": wind_direction,
                "Cloudiness": cloudiness,
                "Rain volume": rain_volume,
                "Snow volume": snow_volume
            })

        # Guardar los datos en un archivo CSV
        df = pd.DataFrame(weather_data)
        df.to_csv(filename, index=False, encoding="utf-8")

        response = requests.get(url, timeout=10)  # 10 segundos de tiempo de espera

        print(f"Weather data for '{city}' saved to '{filename}'")
    else:
        print(f"Failed to get data for '{city}': {response.status_code}")


