import socket
import json
import joblib
from datetime import datetime, timezone

modelo = joblib.load('modelo_ids_multiclase.pkl')

PUERTO_ESCUCHA = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PUERTO_ESCUCHA))
s.listen(1)

print("SERVIDOR CLOUD ACTIVO Y ESCUCHANDO EN PUERTO 5000...")
conn, addr = s.accept()
print(f"Raspberry conectada desde {addr[0]}")

buffer = ""
while True:
    data = conn.recv(4096)
    if not data:
        break
    buffer += data.decode('utf-8')
    
    # Procesar líneas completas
    while '\n' in buffer:
        linea, buffer = buffer.split('\n', 1)
        try:
            dato = json.loads(linea)
            if dato.get('event_type') == 'flow':
                proto = 6 if dato.get('proto') == 'TCP' else 17
                puerto = dato.get('dest_port', 0)
                paquetes = dato.get('flow', {}).get('pkts_toserver', 0)
                t0_str = dato.get('timestamp')
                t0 = datetime.fromisoformat(t0_str.replace('Z', '+00:00'))
                if t0.tzinfo is None:
                    t0 = t0.replace(tzinfo=timezone.utc)
                prediccion = modelo.predict([[proto, puerto, paquetes]])
                clase = prediccion[0]
                if clase != 'Normal':
                    t2 = datetime.now(timezone.utc)
                    latencia_cloud = abs((t2 - t0).total_seconds())
                    print(f"\n[!] ALERTA CLOUD: {clase} desde {addr[0]}")
                    print(f" -> Latencia Cloud End-to-End: {latencia_cloud:.4f} segundos")
        except json.JSONDecodeError:
            continue