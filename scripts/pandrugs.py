#Acceso a API de Pandrugs 

import requests
import json

# URL del endpoint público oficial
api_url = "https://www.pandrugs.org/pandrugs-backend/api/analyze"

# 1. Carga el archivo VCF
VCF = "data/data_grch38.vcf"

try:
    archivos = {
        "vcf_file": (VCF,open(VCF,'rb'),'text/vcard')
    }
except FileNotFoundError:
    print(f"Error:No se encuentra el archivo {VCF} en este directorio.")
    exit()

# 2. Parámetros clínicos de la petición
datos = {
    'assembly':'GRCh38',
    'incude_germline':'true?'
}

print ("Conectando con el servidor público de PanDrugs...(esto puede tardar unos segundos)")

try:
    # 3. Lanzo petición
    respuesta = requests.post(api_url,files=archivos,data=datos,timeout=300)

    # Comprobar si servidor ha devuelto error
    respuesta.raise_for_status()

    # 4. Procesar resultados
    resultados = respuesta.json()
    farmacos = resultados.get('drugs',[])

    print(f"Análisis completado, se han priorizado {len(farmacos)} posible interacciones variante-fármaco.")

    # 5. Guardar los resultados
    with open('resultados_pandrugs.json','2',encoding='utf-8') as f:
        json.dump(resultados,f,indent=4)

    print ("Datos guardados correctamente en 'resultados_pandrugs.json'.")

except requests.exceptions.Timeout:
    print ("Error crítico: El servidor ha tardado más de 5 minutos en responder y la conexión se ha cortado. Inténtalo en otro momento o hazlo en local.")
except requests.exceptions.RequestException as e:
    print (f"Fallo e la comuicación con la API: {e}")