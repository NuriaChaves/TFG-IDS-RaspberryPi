from datetime import datetime

ARCHIVO_T0 = "t0_registro.log"
ARCHIVO_T1 = "alertas_firewall.log"

def parsear_timestamp(ts_str):
    # Limpia y parsea formato ISO8601 con o sin zona horaria
    ts_str = ts_str.strip().replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(ts_str)
    except Exception:
        return None

def cargar_t0(ruta):
    eventos = []
    with open(ruta, 'r') as f:
        for linea in f:
            partes = linea.strip().split(',')
            if len(partes) >= 2:
                ts = parsear_timestamp(partes[0])
                tipo = partes[1] if len(partes) > 1 else 'Desconocido'
                if ts:
                    eventos.append({'t0': ts, 'tipo': tipo})
    return eventos

def cargar_t1(ruta):
    alertas = []
    with open(ruta, 'r') as f:
        for linea in f:
            partes = linea.strip().split(',')
            if len(partes) >= 3:
                ts = parsear_timestamp(partes[0])
                ip = partes[1]
                clase = partes[2]
                if ts:
                    alertas.append({'t1': ts, 'ip': ip, 'clase': clase})
    return alertas

def calcular(t0_eventos, t1_alertas):
    print("\n========================================")
    print("   INFORME DE LATENCIA — IDS RASPBERRY  ")
    print("========================================\n")

    resultados = []

    for ataque in t0_eventos:
        t0 = ataque['t0']
        tipo = ataque['tipo']

        # Buscar la primera alerta posterior a T0
        alertas_validas = [
            a for a in t1_alertas
            if a['t1'] >= t0 and a['clase'] == tipo
        ]

        if not alertas_validas:
            print(f"[{tipo}] T0: {t0.isoformat()} → Sin alerta detectada")
            continue

        primera_alerta = min(alertas_validas, key=lambda a: a['t1'])
        t1 = primera_alerta['t1']

        # Calcular diferencia — quitar info de zona horaria si hay conflicto
        try:
            if t0.tzinfo and not t1.tzinfo:
                t1 = t1.replace(tzinfo=t0.tzinfo)
            elif t1.tzinfo and not t0.tzinfo:
                t0 = t0.replace(tzinfo=t1.tzinfo)
            latencia_ms = (t1 - t0).total_seconds() * 1000
        except Exception as e:
            print(f"Error calculando latencia: {e}")
            continue

        resultados.append(latencia_ms)

        print(f"Tipo de ataque   : {tipo}")
        print(f"T0 (envío)       : {t0.strftime('%H:%M:%S.%f')}")
        print(f"T1 (detección)   : {t1.strftime('%H:%M:%S.%f')}")
        print(f"IP detectada     : {primera_alerta['ip']}")
        print(f"Latencia         : {latencia_ms:.1f} ms")
        print("----------------------------------------")

    if resultados:
        print(f"\nRESUMEN")
        print(f"Ataques analizados : {len(resultados)}")
        print(f"Latencia mínima    : {min(resultados):.1f} ms")
        print(f"Latencia máxima    : {max(resultados):.1f} ms")
        print(f"Latencia media     : {sum(resultados)/len(resultados):.1f} ms")
        print(f"\nNota: incluye latencia de túnel VPN (~1-20ms).")
        print(f"Para latencia pura del IDS, restar el RTT de la VPN.")

if __name__ == "__main__":
    try:
        t0_eventos = cargar_t0(ARCHIVO_T0)
        t1_alertas = cargar_t1(ARCHIVO_T1)
        print(f"T0 cargados : {len(t0_eventos)} ataques")
        print(f"T1 cargados : {len(t1_alertas)} alertas")
        calcular(t0_eventos, t1_alertas)
    except FileNotFoundError as e:
        print(f"Error: no se encuentra el archivo {e}")
        print("Asegúrate de haber ejecutado primero atacante_latencia.py e ids_final.py")