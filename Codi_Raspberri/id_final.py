import pandas as pd
import joblib
import json
import os
import time
import warnings
from datetime import datetime, timezone

# Ignorar avisos innecesarios de scikit-learn
warnings.filterwarnings("ignore")

# 1. Cargar el cerebro multiclase
modelo = joblib.load('modelo_ids_multiclase.pkl')
ruta_log = '/var/log/suricata/eve.json'

# Archivo donde guardaremos las IPs maliciosas para el futuro Firewall
archivo_alertas = 'alertas_firewall.log' 

print("IDS activado")
print(f"Las IPs bloqueables se guardarán en: {archivo_alertas}")

def monitorear():
    print(f"Monitoreando... logs en: {ruta_log}")
    with open(ruta_log, 'r') as log_file:
        log_file.seek(0, os.SEEK_END)
        while True:
            linea = log_file.readline()
            if not linea:
                time.sleep(0.1)
                continue
            
            try:
                dato = json.loads(linea)
            except json.JSONDecodeError:
                continue
                
            if dato.get('event_type') == 'flow':
                proto_str = dato.get('proto', 'TCP')
                proto = 6 if proto_str == 'TCP' else 17
                puerto = dato.get('dest_port', 0)
                paquetes = dato.get('flow', {}).get('pkts_toserver', 0)
                ip_origen = dato.get('src_ip', 'Desconocida')
                                
                # T0: La hora exacta a la que Suricata vio el PRIMER paquete del ataque
                t0_str = dato.get('timestamp')
                t0 = datetime.fromisoformat(t0_str.replace('Z', '+00:00'))
                
                # Intervención IA
                prediccion = modelo.predict([[proto, puerto, paquetes]])
                clase = prediccion[0]
                
                if clase != 'Normal':
                    # T1: La hora exacta, tras decidir que es un ataque
                    t1 = datetime.now(timezone.utc)
                    
                    # Calculamos la diferencia en segundos (Latencia total)
                    latencia_segundos = (t1 - t0).total_seconds()
                    
                    # Imprimimos la alerta con el dato
                    print(f"\n[!] ALERTA: {clase.upper()} detectado desde {ip_origen}")
                    print(f" Tiempo total de procesamiento: {latencia_segundos:.4f} segundos")
                    
                    # Lo guardamos en un archivo
                    with open("latencia_resultados.csv", 'a') as f_alertas:
                        f_alertas.write(f"{clase},{paquetes},{latencia_segundos:.4f}\n")

if __name__ == "__main__":
    if os.path.exists(ruta_log):
        monitorear()
    else:
        print(f"Error: No se encuentra el log de Suricata en {ruta_log}.")