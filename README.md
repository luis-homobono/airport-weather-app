# API CLIMA EN AEROPUERTOS

Código de API para aplicación para obtener el clima de vuelos y aeropuertos.

## Descripción
Api para obtener el clima se caracteriza por:
- Endpoint para la carga de archivos. `/ticket/upload-file`. El layout que necesita se encuentra en la carpeta `./data/challenge_dataset.csv`.
- Servicios para obtener el clima desde `https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2#/`. Se selecciono este servicio debido a que tiene una capa de prueba y presenta muchos servicios como:
    - Forecast. Obtener el clima de un periodo de tiempo determinado
    - Historical. Obtener el historico del clima.
    - Astronomy. Obtener datos astronomicos de avistamientos de algún astro.
    - Air Quality. Datos de calidad de aire.
    - etc.
- Tiene 2 endpoints para obtener el clima, para aeropuertos y para vuelos:
    - `airport-weather/{airport_iata_code}`: Obtiene el clima a partir un codigo de aeropuerto.
    - `flights-weather/{num_flight}`: Obtiene el clima de origen y destino desde un numero de vuelo especifico
- Tiene 2 endpoints para obtener el listado de aeropuestos y de vuelos:
    - `airport/`: Obtiene el listado de aeropuertos.
    - `flights/`: Obtiene el listado de vuelos.

## Requerimientos
Este proyecto utiliza redis como sistema de cache.

Si deseas utilizar docker para levantar una instancia de docker utiliza el siguiente comando.
```
docker run -d --name my-redis-stack -p 6379:6379  redis/redis-stack-server:latest
```

De igual forma si deseas utilizar un gestor de cache puedes utilizar redis commander:
```
npm install -g redis-commander
redis-commander
```

## Instalación

Sí tu deseas instalar la api en tu local puedes hacer uso de los siguientes compandos:
1. Creación de ambiente virtual
```{bash}
python -m venv venv
source venv/bin/activate
```
2. Instalación de librerias
```{bash}
pip install -r requirements.txt
```
3. Correr pruebas unitarias (Opcional) # TODO: Necesita más pruebas unitarias
```{bash}
pytest --verbosity=2
```
4. Correr el servidor:
```{bash}
flask run
```

Sí deseas revisar la documentación de la API con Swagger-UI puedes revisarlo en la siguiente liga: [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)
¨
