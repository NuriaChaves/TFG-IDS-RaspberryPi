import pandas as pd
import numpy as np
import random

print("--- FASE 1: GENERANDO DATASET ---")
random.seed(42)
np.random.seed(42)
datos = []

# 1. Tráfico NORMAL
for _ in range(5000):
    proto = random.choice([6, 17])
    # Tráfico normal incluye SSH legítimo, HTTP, etc.
    puerto = random.choice([22, 80, 443, 8080, random.randint(1024, 65535)])
    # Volumen variable, a veces alto (streaming, descargas)
    paquetes = int(np.random.exponential(scale=15)) + 1
    paquetes = min(paquetes, 300)  # Cap realista
    datos.append([proto, puerto, paquetes, 'Normal'])

# 2. ESCANEO DE RED
for _ in range(3000):
    proto = 6
    puerto = random.randint(1, 1024)
    # Mayoría 1-2 paquetes, pero algunos flujos legítimos también son cortos
    paquetes = random.choices([1, 2, 3, random.randint(4, 10)], weights=[50, 30, 15, 5])[0]
    # Algunos escaneos van a puertos altos también
    if random.random() < 0.2:
        puerto = random.randint(1025, 65535)
    datos.append([proto, puerto, paquetes, 'Escaneo_Red'])

# 3. FUERZA BRUTA
for _ in range(2000):
    proto = 6
    # Mayoría al 22, pero también RDP (3389), FTP (21)
    puerto = random.choices([22, 3389, 21, random.randint(1, 65535)], weights=[70, 15, 10, 5])[0]
    # Solapamiento con normal: algunos intentos son pocos paquetes
    paquetes = int(np.random.normal(loc=40, scale=15))
    paquetes = max(5, min(paquetes, 150))  # Entre 5 y 150
    datos.append([proto, puerto, paquetes, 'Fuerza_Bruta'])

# 4. DDoS UDP
for _ in range(2000):
    proto = random.choices([17, 6], weights=[85, 15])[0]  # Mayoría UDP pero no todo
    puerto = random.randint(1, 65535)
    # Solapamiento: algunos DDoS no son tan masivos
    paquetes = int(np.random.normal(loc=300, scale=100))
    paquetes = max(50, min(paquetes, 1000))  # Entre 50 y 1000
    datos.append([proto, puerto, paquetes, 'DDoS_UDP'])

df = pd.DataFrame(datos, columns=['proto', 'dest_port', 'flow_pkts_toserver', 'clase'])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv('dataset_multiclase.csv', index=False)

print(f"Dataset generado: {len(df)} filas")
print("\nDistribución de clases:")
print(df['clase'].value_counts())
print("\nEstadísticas de paquetes por clase:")
print(df.groupby('clase')['flow_pkts_toserver'].describe().round(1))