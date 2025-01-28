import requests
import concurrent.futures
import time

# URL del endpoint
endpoints = [
    'http://localhost:8000/api/bands',
    'http://localhost:8000/api/bands/2',
    'http://localhost:8000/api/genres',
    'http://localhost:8000/api/genres/1'
]

# Tipo de prueba
tipo_prueba = "Estrés"

# Configuración del número de solicitudes concurrentes
num_peticiones = 120  # Usuarios concurrentes

# Variables para medir resultados
resultados = {
    "total_solicitudes": 0,
    "exitos": 0,
    "errores": 0,
    "tiempos_respuesta": [],
}

def realizar_solicitudes(endpoint, peticion):
    inicio = time.time()  # Tiempo inicial
    try:
        respuesta = requests.get(endpoint)
        tiempo_respuesta = (time.time() - inicio) * 1000  # Convertir a ms
        resultados["tiempos_respuesta"].append(tiempo_respuesta)
        resultados["total_solicitudes"] += 1

        if respuesta.status_code == 200:
            resultados["exitos"] += 1
            print(f"Solicitud #{peticion} al endpoint {endpoint} exitosa ({tiempo_respuesta:.2f} ms)")
        else:
            resultados["errores"] += 1
            print(f"Error en solicitud #{peticion} al endpoint {endpoint}: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        resultados["errores"] += 1
        print(f"Error en solicitud #{peticion} al endpoint {endpoint}: {e}")

# Ejecutar solicitudes concurrentes
with concurrent.futures.ThreadPoolExecutor(max_workers=num_peticiones) as executor:
    tareas_pendientes = []
    for i, endpoint in enumerate(endpoints):
        for j in range(num_peticiones // len(endpoints)):
            tarea_pendiente = executor.submit(realizar_solicitudes, endpoint, f"{i}-{j}")
            tareas_pendientes.append(tarea_pendiente)

    for tarea_pendiente in tareas_pendientes:
        tarea_pendiente.result()

# Calcular resultados
if resultados["tiempos_respuesta"]:
    tiempo_promedio = sum(resultados["tiempos_respuesta"]) / len(resultados["tiempos_respuesta"])
    tiempo_maximo = max(resultados["tiempos_respuesta"])
    tasa_exito = (resultados["exitos"] / resultados["total_solicitudes"]) * 100
else:
    tiempo_promedio = 0
    tiempo_maximo = 0
    tasa_exito = 0

# Imprimir resultados finales
print("\n=== Resultados de la prueba de estres ===")
print(f"Tipo de prueba: {tipo_prueba}")
print(f"Usuarios concurrentes soportados: {num_peticiones}")
print(f"Tiempo de respuesta promedio: {tiempo_promedio:.2f} ms")
print(f"Tiempo de respuesta máximo: {tiempo_maximo:.2f} ms")
print(f"Tasa de éxito: {tasa_exito:.2f}%")
print(f"Total de solicitudes: {resultados['total_solicitudes']}")
print(f"Solicitudes exitosas: {resultados['exitos']}")
print(f"Errores: {resultados['errores']}")
print("========================================")
