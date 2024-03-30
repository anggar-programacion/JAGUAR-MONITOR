import jlrpy
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from mis_utilidades import read_credentials_from_file
from geopy.geocoders import Nominatim


def obtener_valor_estad(estad, clave, valor_predeterminado="No puedo localizar el dato"):
	core_status = estad.get("vehicleStatus", {}).get("coreStatus", [])

	for status_entry in core_status:
		if status_entry.get("key") == clave:
			return status_entry.get("value")
	return valor_predeterminado

def obtener_nombre_calle(latitud, longitud):
    # Configura el geocodificador con Nominatim
    geolocalizador = Nominatim(user_agent="nombre_calle_app")

    # Obtiene la dirección a partir de la latitud y longitud
    # Da el nombre de la calle, el barrio la ciudad el codigo postal y el pais
    location = geolocalizador.reverse((latitud, longitud), language='es')
    print (location)
    # Extrae el nombre de la calle desde la dirección
    nombre_calle = location.address.split(",")[0]
    barrio = location.address.split(",")[1]
    ciudad = location.address.split(",")[2]
    region = location.address.split(",")[3]
    codigo_postal = location.address.split(",")[4]
    pais = location.address.split(",")[5]

    print (barrio)
    print (ciudad)
    print (region)
    print (codigo_postal)
    print (pais)

    return nombre_calle, ciudad, pais

def obtener_temperatura(latitud, longitud, api_key):
    # Configura la URL de la API de OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={api_key}"

    try:
        # Realiza la solicitud a la API
        respuesta = requests.get(url)
        datos_clima = respuesta.json()

        # Extrae la temperatura actual
        temperatura_actual = datos_clima['main']['temp']

        # La temperatura se devuelve en Kelvin, puedes convertirla a Celsius o Fahrenheit según tus necesidades
        # Ejemplo de conversión a Celsius
        temperatura_celsius = temperatura_actual - 273.15

        return temperatura_celsius

    except Exception as e:
        print(f"Error al obtener la temperatura: {e}")
        return None

api_key_openweathermap = "c437c66223239cdcea44744b70c0084f"

#AUTENTIFICACION USANDO ARCHIVO CONFIG.TXT

credentials = read_credentials_from_file("config.txt")
username, password = credentials
#print ("Nombre de usuario: ",username)
#print ("Password: ",password)


c = jlrpy.Connection(username, password)

v = c.vehicles[0]

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
# Escribe aquí el ID de tu documento:
SPREADSHEET_ID = '1M9Nu20PSDOg2uxh81MaSWe-DVXlWxw1h_OP9qxOQlGM'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# LEE ESTADO DEL VEHICULO
estad = v.get_status()


#Consumos coche

KM_totales = obtener_valor_estad(estad, "ODOMETER_METER")
KM_totales = str(int (KM_totales)/1000)
Reserva_fuel = obtener_valor_estad(estad, "DISTANCE_TO_EMPTY_FUEL")
Porc_Reserva_fuel = obtener_valor_estad(estad,"FUEL_LEVEL_PERC")
KM_add_blue = obtener_valor_estad(estad, "EXT_EXHAUST_FLUID_DISTANCE_TO_SERVICE_KM")
KM_cambio = obtener_valor_estad(estad, "EXT_KILOMETERS_TO_SERVICE")
voltaje_bateria = obtener_valor_estad(estad, "BATTERY_VOLTAGE")
temp_motor = obtener_valor_estad(estad, "ENGINE_COOLANT_TEMP")
# OJO PASAR DE FARENHEN A CENTIGRADOS ?
temp_motor = str(round((int (temp_motor)-32)*(5/9),2)) 
#print(temp_motor)


#Seguridad del coche:

puertas_cerradas = obtener_valor_estad(estad, "DOOR_IS_ALL_DOORS_LOCKED")
puerta_del_izq = obtener_valor_estad(estad, "DOOR_FRONT_LEFT_POSITION")	
bloqueo_puert_del_izq = obtener_valor_estad(estad, "DOOR_FRONT_LEFT_LOCK_STATUS")
puerta_del_dec = obtener_valor_estad(estad, "DOOR_FRONT_RIGHT_POSITION")	
bloqueo_puert_del_dec = obtener_valor_estad(estad, "DOOR_FRONT_RIGHT_LOCK_STATUS")	
puerta_tra_izq = obtener_valor_estad(estad, "DOOR_REAR_LEFT_POSITION")	
bloqueo_puert_tra_izq = obtener_valor_estad(estad, "DOOR_REAR_LEFT_LOCK_STATUS")	
puerta_tra_dec = obtener_valor_estad(estad, "DOOR_REAR_RIGHT_POSITION")
bloqueo_puert_tra_dec = obtener_valor_estad(estad, "DOOR_REAR_RIGHT_LOCK_STATUS")
capo = obtener_valor_estad(estad, "DOOR_ENGINE_HOOD_POSITION")
bloqueo_capo = obtener_valor_estad(estad, "DOOR_ENGINE_HOOD_LOCK_STATUS")
maletero = obtener_valor_estad(estad, "DOOR_BOOT_POSITION")
bloqueo_maletero = obtener_valor_estad(estad, "DOOR_BOOT_LOCK_STATUS")


#PRESION NEUMATICOS
pres_rued_del_izq = obtener_valor_estad(estad, "TYRE_PRESSURE_FRONT_LEFT")		
pres_rued_del_izq=int(pres_rued_del_izq)/100
#print(pres_rued_del_izq)
pres_rued_del_der = obtener_valor_estad(estad, "TYRE_PRESSURE_FRONT_RIGHT")	
pres_rued_del_der=int(pres_rued_del_der)/100
#print(pres_rued_del_der)
pres_rued_tra_izq = obtener_valor_estad(estad, "TYRE_PRESSURE_REAR_LEFT")	
pres_rued_tra_izq=int(pres_rued_tra_izq)/100
#print(pres_rued_tra_izq)
pres_rued_tra_der = obtener_valor_estad(estad, "TYRE_PRESSURE_REAR_LEFT")	
pres_rued_tra_der=int(pres_rued_tra_der)/100
#print(pres_rued_tra_der)


# LEE POSICION DEL VEHICULO
posicion = v.get_position()
#posicion coche
latitud = (posicion['position']['latitude'])
longitud = (posicion['position']['longitude'])
velocidad = (posicion['position']['speed'])


fecha = str(datetime.now())
#print (fecha)

values_consumo =[[fecha, KM_totales, Reserva_fuel, Porc_Reserva_fuel, KM_add_blue, KM_cambio, voltaje_bateria, temp_motor]]
print(values_consumo)

values_seguridad =[[fecha, puertas_cerradas, puerta_del_izq, bloqueo_puert_del_izq, puerta_del_dec, bloqueo_puert_del_dec, puerta_tra_izq, bloqueo_puert_tra_izq, puerta_tra_dec,bloqueo_puert_tra_dec,capo, bloqueo_capo,maletero,bloqueo_maletero]]
print(values_seguridad)

values_presion =[[fecha, pres_rued_del_izq, pres_rued_del_der, pres_rued_tra_izq,pres_rued_tra_der]]
print(values_presion)


nombre_calle, ciudad, pais = obtener_nombre_calle(latitud, longitud)
#print(f"La calle en la ubicación ({latitud}, {longitud}) es: {nombre_calle}")
temperatura = obtener_temperatura(latitud, longitud, api_key_openweathermap)
#print(f"La temperatura actual en la ubicación ({latitud}, {longitud}) es: {temperatura:.2f} °C")

values_posicion= [[fecha, latitud, longitud, velocidad, nombre_calle, ciudad, pais, temperatura]]
print(values_posicion)




# Llamamos a la api para grabar los datos en la hoja de calculo.
result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
							range='PRES NEUMATICOS!A4',
							valueInputOption='USER_ENTERED',
							body={'values':values_presion}).execute()


# Llamamos a la api para grabar los datos en la hoja de calculo.
result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
							range='CONSUMOS!A4',
							valueInputOption='USER_ENTERED',
							body={'values':values_consumo}).execute()

# Llamamos a la api para grabar los datos en la hoja de calculo.
result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
							range='SEGURIDAD!A4',
							valueInputOption='USER_ENTERED',
							body={'values':values_seguridad}).execute()


#Llamamos a la api para grabar los datos en la hoja de calculo.
result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
							range='POSICION!A4',
							valueInputOption='USER_ENTERED',
							body={'values':values_posicion}).execute()


print(f"Datos insertados correctamente.\n{(result.get('updates').get('updatedCells'))}")

