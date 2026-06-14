# TFG-IDS-RaspberryPi
Sistema de Detecció d'Intrusos perimetral (Edge IDS) basat en Random Forest i Suricata sobre Raspberry Pi 4.

Aquest repositori conté el codi font desenvolupat per al meu Treball de Fi de Grau (TFG) en Enginyeria en Xarxes de Telecomunicació a la Universitat Pompeu Fabra (UPF).

L'objectiu del projecte és demostrar la viabilitat d'implementar un Sistema de Detecció d'Intrusos (IDS) al perímetre de la xarxa (Edge Computing) utilitzant una Raspberry Pi 4, el motor *uricata i un algorisme de Random Forest per classificar amenaces en temps real sense dependre del Cloud.

## Estructura del Repositori

### 1. `Codi_Ordinador`
Conté els scripts que s'executen des de l'equip de control i atacant (Windows):
* `ataque_ddos.py`: Desenvolupat a mida per simular una inundació volumètrica de datagrames UDP cap al node Edge.
* `ataque_fuerza_bruta.py`: Dissenyat per llançar ràfegues massives de paquets TCP apuntant al port 22 (SSH) emulant un atac de diccionari.
* `calcular_latencia.py`: Script auxiliar que processa els fitxers de registre, emparella els temps d'enviament ($T_0$) i detecció ($T_1$) i calcula les latències netes estadístiques.
* `nube_siem.py`: Servidor Socket TCP actiu que simula el receptor centralitzat de l'entorn Cloud Computing.
* `rendimiento_windows.py`: Eina de monitoratge que registra cíclicament l'ús de CPU i RAM del sistema durant les proves en un fitxer CSV.

### 2. `Codi_Raspberri`
Conté els fitxers i scripts allotjats estrictament dins del node perimetral ARM:
* `id_final.py`: El nucli de l'IDS local. Realitza una lectura asíncrona en calent del fitxer `eve.json` de Suricata, n'extreu les característiques numèriques i invoca el model predictiu.
* `agente_sensor.py`: Script de reenviament que llegeix les línies en brut de Suricata i les encapsula cap al túnel Ngrok per simular l'arquitectura tradicional.
* `procesa_datos.py`: Script encarregat de generar de forma automatitzada el dataset sintètic balancejat per entrenar la IA sense sobreajustament.

