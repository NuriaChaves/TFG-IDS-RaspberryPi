import psutil
import time
import csv
import os

# Nombre del archivo de salida
archivo_log = "rendimiento_sistema.csv"

print(f"--- MONITOR DE RENDIMIENTO ACTIVADO ---")
print(f"Guardando métricas en '{archivo_log}' cada 1 segundo.")
print("Pulsa Ctrl + C para detener la monitorización.\n")

# Si el archivo no existe, creamos la cabecera
if not os.path.exists(archivo_log):
    with open(archivo_log, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "CPU_Uso_Porcentaje", "RAM_Uso_Porcentaje", "RAM_Disponible_MB"])

try:
    while True:
        # Obtener la hora actual
        timestamp = time.strftime("%H:%M:%S")
        
        # Medir la CPU durante un intervalo de 1 segundo
        cpu_uso = psutil.cpu_percent(interval=1)
        
        # Obtener métricas de la memoria RAM
        ram = psutil.virtual_memory()
        ram_uso_porcentaje = ram.percent
        ram_disponible_mb = round(ram.available / (1024 * 1024), 2)
        
        # Guardar los datos en el archivo CSV
        with open(archivo_log, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, cpu_uso, ram_uso_porcentaje, ram_disponible_mb])
            
        # Mostrar por pantalla para control en tiempo real
        print(f"[{timestamp}] -> CPU: {cpu_uso}% | RAM: {ram_uso_porcentaje}% (Libre: {ram_disponible_mb} MB)")

except KeyboardInterrupt:
    print("\n[!] Monitorización detenida por el usuario.")
    print(f"[+] Archivo '{archivo_log}' guardado con éxito. ¡Listo para importar en Excel y crear tus gráficas del TFG!")