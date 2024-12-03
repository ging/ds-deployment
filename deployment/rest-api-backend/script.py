import requests
import json
import pprint
import pandas as pd
import os


# Configuración de constantes
DATA_SPACE_PROVIDER = "http://ds-provider:1234"
DATA_SPACE_CONSUMER = "http://ds-consumer:1235"
REST_API_SERVICE = "http://rest-api-service:8000" # API de G1


def create_catalog():
    """Crea un catálogo en el proveedor de datos."""
    payload = {
        "foaf:homepage": "My catalog in Dataspace provider",
        "dct:title": "My catalog in Dataspace provider"
    }
    headers = {"Content-Type": "application/json"}
    url = f"{DATA_SPACE_PROVIDER}/api/v1/catalogs"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    pprint.pprint(response.json())
    return response.json()["@id"]

# VIVIENDAS


def create_data_service_viviendas(catalog_id):
    """Crea un servicio de datos en el catálogo especificado y guarda la respuesta JSON en un archivo."""
    # Definir el payload y la URL de la API
    payload = {
        "dcat:endpointURL": f"{REST_API_SERVICE}/viviendas"  # Viviendas es el endpoint de la API de G1
    }
    headers = {"Content-Type": "application/json"}
    url = f"{DATA_SPACE_PROVIDER}/api/v1/catalogs/{catalog_id}/data-services"
    
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)


    # Verificar que la respuesta es exitosa
    response.raise_for_status()
    
    # Obtener el contenido de la respuesta en formato JSON
    response_json = response.json()
    
    # Imprimir la respuesta para depuración
    # pprint.pprint(response_json)
    return response_json['@id']
    
# SERVICIOS
def create_data_servicios(catalog_id):
    """Crea un servicio de datos en el catálogo especificado y guarda la respuesta JSON en un archivo."""
    # Definir el payload y la URL de la API
    payload = {
        "dcat:endpointURL": f"{REST_API_SERVICE}/servicios"  # Viviendas es el endpoint de la API de G1
    }
    headers = {"Content-Type": "application/json"}
    url = f"{DATA_SPACE_PROVIDER}/api/v1/catalogs/{catalog_id}/data-services"
    
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)
    pprint.pprint("Prueba 3:")
    pprint.pprint(response.json())
    
    # Verificar que la respuesta es exitosa
    response.raise_for_status()
    
    # Obtener el contenido de la respuesta en formato JSON
    response_json = response.json()
    
    # Imprimir la respuesta para depuración
    pprint.pprint(response_json)
    
    return response_json['@id']

# TERRENOS
def create_data_terrenos(catalog_id):
    """Crea un servicio de datos en el catálogo especificado y guarda la respuesta JSON en un archivo."""
    # Definir el payload y la URL de la API
    payload = {
        "dcat:endpointURL": f"{REST_API_SERVICE}/terrenos"  # Viviendas es el endpoint de la API de G1
    }
    headers = {"Content-Type": "application/json"}
    url = f"{DATA_SPACE_PROVIDER}/api/v1/catalogs/{catalog_id}/data-services"
    
    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)
    
    # Verificar que la respuesta es exitosa
    response.raise_for_status()
    
    # Obtener el contenido de la respuesta en formato JSON
    response_json = response.json()
    
    # Imprimir la respuesta para depuración
    pprint.pprint(response_json)
    return response_json['@id']
    
def create_agreement(dataservice_id):
    """Crea un acuerdo utilizando un servicio de datos."""
    pprint.pprint(dataservice_id)
    payload = {"dataServiceId": dataservice_id}
    headers = {"Content-Type": "application/json"}
    url = f"{DATA_SPACE_PROVIDER}/api/v1/agreements"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    agreement_id = response.json()["agreement_id"]
    pprint.pprint(response.json())
    return agreement_id, f"urn:uuid:{agreement_id}"


def setup_transfer():
    """Configura la transferencia en el consumidor."""
    url = f"{DATA_SPACE_CONSUMER}/api/v1/setup-transfer"
    response = requests.post(url)
    response.raise_for_status()
    pprint.pprint(response.json())
    return response.json()


def request_transfer(agreement_pid, callback_info):
    """Solicita una transferencia."""
    url = f"{DATA_SPACE_CONSUMER}/api/v1/request-transfer"
    payload = {
        "agreementId": agreement_pid,
        "format": "http+pull",
        "dataAddress": None,
        "callbackAddress": callback_info["callbackAddress"],
        "callbackId": callback_info["callbackId"],
        "consumerPid": callback_info["consumerPid"]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    pprint.pprint(response.json())
    return response.json()


def get_data_plane_address(consumer_pid): #Devuelve cada uno de los datasets
    """Obtiene la dirección del plano de datos."""
    consumer_pid_uuid = consumer_pid.replace("urn:uuid:", "")
    url = f"{DATA_SPACE_CONSUMER}/api/v1/data-address/{consumer_pid_uuid}"
    response = requests.get(url)
    response.raise_for_status()
    pprint.pprint(response.json())
    return response.json()["dataPlaneAddress"]


# Funcion que junta los dataset en un dataset gordo -> FALTA!!!

def create_combined_dataset(catalog_id):
    """
    Combina los datos de viviendas, servicios y terrenos en un único dataset.
    
    Args:
        catalog_id (str): ID del catálogo en el que se registran los servicios de datos.
        
    Returns:
        pd.DataFrame: Un DataFrame que contiene la combinación de todos los datos.
    """
    # Crear servicios de datos individuales
    viviendas_id = create_data_service_viviendas(catalog_id)
    servicios_id = create_data_servivios(catalog_id) 
    terrenos_id = create_data_terrenos(catalog_id)
    
    # Obtener datos individuales (simulación de datos para este ejemplo)
    viviendas_data = {
        "type": "viviendas",
        "data_service_id": viviendas_id,
        "endpoint": f"{REST_API_SERVICE}/get_viviendas"
    }
    servicios_data = {
        "type": "servicios",
        "data_service_id": servicios_id,
        "endpoint": f"{REST_API_SERVICE}/get_servicios"
    }
    terrenos_data = {
        "type": "terrenos",
        "data_service_id": terrenos_id,
        "endpoint": f"{REST_API_SERVICE}/get_terrenos"
    }

    # Combinar los datos en un solo dataset
    combined_data = [viviendas_data, servicios_data, terrenos_data]
    dataset = pd.DataFrame(combined_data)
    
    return dataset



def fetch_data_from_data_plane(data_plane_address):
    # """Obtiene datos del plano de datos."""
    # pprint.pprint("data_plane_address " + data_plane_address)
    # url = data_plane_address
    # pprint.pprint("url " + url)
    # # df = pd.read_csv(url)
    # df = requests.get(url) 
    # pprint.pprint("df ")
    # pprint.pprint(df.res)
    # return df
    """Obtiene datos del plano de datos y los convierte en un DataFrame."""
    pprint.pprint("data_plane_address " + data_plane_address)
    url = data_plane_address
    pprint.pprint("url " + url)

    # Hacer una solicitud GET a la URL
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        pprint.pprint("Respuesta recibida correctamente.")
        
        # Convertir la respuesta en JSON
        json_data = response.json()
        
        # El JSON contiene el contenido dentro de la clave "content"
        content = json_data.get("content", "[]")  # Si no hay contenido, usamos un array vacío por defecto
        
        # Convertir el contenido JSON (una cadena de texto) en una lista de diccionarios
        content_list = pd.read_json(content)
        
        # Crear un DataFrame a partir de la lista de diccionarios
        df = pd.DataFrame(content_list)
        pprint.pprint("DataFrame creado:")
        pprint.pprint(df)
        
        return df
    else:
        print("Error en la solicitud:", response.status_code)
        return None



def suspend_transfer(consumer_pid):
    """Suspende la transferencia."""
    url = f"{DATA_SPACE_CONSUMER}/api/v1/suspend-transfer"
    payload = {"consumerPid": consumer_pid}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    pprint.pprint(response.json())


def restart_transfer(consumer_pid):
    """Reinicia la transferencia."""
    url = f"{DATA_SPACE_CONSUMER}/api/v1/restart-transfer"
    payload = {"consumerPid": consumer_pid}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    pprint.pprint(response.json())


def complete_transfer(consumer_pid):
    """Completa la transferencia."""
    url = f"{DATA_SPACE_CONSUMER}/api/v1/complete-transfer"
    payload = {"consumerPid": consumer_pid}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    pprint.pprint(response.json())
