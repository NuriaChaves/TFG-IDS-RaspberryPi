import time
import socket
import os

IP_PORTATIL = "5.tcp.eu.ngrok.io" #Ip del servidor Ngrok
PUERTO = 26717
RUTA_LOG = "/var/log/suricata/eve.json"

# TCP 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_PORTATIL, PUERTO))
print(f"Conectado al servidor cloud en {IP_PORTATIL}:{PUERTO}")

with open(RUTA_LOG, 'r') as log_file:
    log_file.seek(0, os.SEEK_END)
    while True:
        linea = log_file.readline()
        if not linea:
            time.sleep(0.1)
            continue
        s.sendall(linea.encode('utf-8'))