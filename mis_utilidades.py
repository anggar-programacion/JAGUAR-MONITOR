
import glob


def read_credentials_from_file(config_file):
        try:
            with open(config_file, 'r') as file:
                lines = file.readlines()
                username = None
                password = None
               

                for line in lines:
                    if line.startswith("usuario:"):
                        username = line.split(":")[1].strip()
                        
                    elif line.startswith("clave:"):
                        password = line.split(":")[1].strip()
                        

                if username and password:
                    return username, password
                else:
                    #self.label.text = "Credenciales incompletas en el archivo de configuración."
                    return None

        except FileNotFoundError:
            #self.label.text = "Archivo de configuración no encontrado."
            return None



def obtener_archivo_con_siguiente_indice_mas_alto(pattern):
    archivos = glob.glob(pattern)
    numeros = [int(archivo.split('_')[-1].split('.')[0]) for archivo in archivos]
    if numeros:
        numero_mas_alto = max(numeros)
        siguiente_indice = numero_mas_alto + 1
        nuevo_nombre = f'{pattern.split("*")[0]}{siguiente_indice}.png'
        return nuevo_nombre
    else:
        return ''

def obtener_archivo_con_indice_mas_alto(pattern):
    archivos = glob.glob(pattern)
    numeros = [int(archivo.split('_')[-1].split('.')[0]) for archivo in archivos]
    if numeros:
        numero_mas_alto = max(numeros)
        #siguiente_indice = numero_mas_alto + 1
        nuevo_nombre = f'{pattern.split("*")[0]}{numero_mas_alto}.png'
        return nuevo_nombre
    else:
        return ''