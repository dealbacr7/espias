import time
from multiprocessing.connection import Listener
from misiones import generar_misiones, validar_respuesta
from logs import escribir_log

HOST = 'localhost'
PORT = 6000
AUTHKEY = b'espias2026'
NUM_ESPias_ESPERADOS = 2
TIMEOUT_RESPUESTA = 20


def enviar_mensaje(conn, payload):
    conn.send(payload)


def recibir_con_timeout(conn, timeout):
    inicio = time.time()
    while time.time() - inicio < timeout:
        if conn.poll(0.2):
            return conn.recv()
    raise TimeoutError('Tiempo de espera agotado')


def main():
    misiones = generar_misiones()
    resultados = {}
    estadisticas = {}
    agentes = []

    print(f'[COMANDANTE] Escuchando en {HOST}:{PORT}...')
    escribir_log(f'Comandante iniciado en {HOST}:{PORT}')

    with Listener((HOST, PORT), authkey=AUTHKEY) as listener:
        while len(agentes) < NUM_ESPias_ESPERADOS:
            conn = listener.accept()
            datos_presentacion = conn.recv()
            nombre = datos_presentacion.get('agente', f'espia_{len(agentes)+1}')
            velocidad = datos_presentacion.get('velocidad', 1.0)
            agentes.append({'nombre': nombre, 'conn': conn, 'velocidad': velocidad})
            estadisticas[nombre] = {'aciertos': 0, 'fallos': 0, 'tiempo_total': 0.0, 'misiones': 0}
            print(f'[COMANDANTE] Conectado: {nombre}')
            escribir_log(f'Conectado el agente {nombre}')

        for indice, mision in enumerate(misiones):
            agente = agentes[indice % len(agentes)]
            conn = agente['conn']
            nombre = agente['nombre']

            payload = {'tipo': 'mision', 'id': mision['id'], 'mensaje': mision['mensaje']}
            print(f"[COMANDANTE] Enviando misión {mision['id']} a {nombre}: {mision['mensaje']}")
            escribir_log(f"Misión {mision['id']} enviada a {nombre}")

            momento_envio = time.time()
            enviar_mensaje(conn, payload)

            try:
                respuesta = recibir_con_timeout(conn, TIMEOUT_RESPUESTA)
                tiempo_total = time.time() - momento_envio
                correcta = validar_respuesta(mision, respuesta.get('respuesta', ''))

                resultados[mision['id']] = {
                    'agente': nombre,
                    'mensaje': mision['mensaje'],
                    'respuesta': respuesta.get('respuesta', ''),
                    'correcta': correcta,
                    'tiempo': tiempo_total,
                }

                estadisticas[nombre]['misiones'] += 1
                estadisticas[nombre]['tiempo_total'] += tiempo_total
                if correcta:
                    estadisticas[nombre]['aciertos'] += 1
                    estado = 'CORRECTA'
                else:
                    estadisticas[nombre]['fallos'] += 1
                    estado = 'INCORRECTA'

                print(f"[COMANDANTE] Respuesta de {nombre}: {respuesta.get('respuesta')} -> {estado} ({tiempo_total:.2f}s)")
                escribir_log(
                    f"Misión {mision['id']} resuelta por {nombre} | respuesta={respuesta.get('respuesta')} | "
                    f"estado={estado} | tiempo={tiempo_total:.2f}s"
                )

            except TimeoutError:
                resultados[mision['id']] = {
                    'agente': nombre,
                    'mensaje': mision['mensaje'],
                    'respuesta': 'SIN_RESPUESTA',
                    'correcta': False,
                    'tiempo': TIMEOUT_RESPUESTA,
                }
                estadisticas[nombre]['misiones'] += 1
                estadisticas[nombre]['fallos'] += 1
                estadisticas[nombre]['tiempo_total'] += TIMEOUT_RESPUESTA
                print(f'[COMANDANTE] {nombre} no respondió a tiempo.')
                escribir_log(f"Misión {mision['id']} sin respuesta de {nombre}")

        for agente in agentes:
            enviar_mensaje(agente['conn'], {'tipo': 'fin'})
            agente['conn'].close()

    print('\n=== INFORME FINAL ===')
    escribir_log('=== INFORME FINAL ===')
    for nombre, datos in estadisticas.items():
        promedio = datos['tiempo_total'] / datos['misiones'] if datos['misiones'] else 0.0
        print(
            f"{nombre}: aciertos={datos['aciertos']}, fallos={datos['fallos']}, "
            f"tiempo total={datos['tiempo_total']:.2f}s, media={promedio:.2f}s"
        )
        escribir_log(
            f"{nombre}: aciertos={datos['aciertos']}, fallos={datos['fallos']}, "
            f"tiempo total={datos['tiempo_total']:.2f}s, media={promedio:.2f}s"
        )

    ranking = sorted(
        estadisticas.items(),
        key=lambda item: (-item[1]['aciertos'], item[1]['tiempo_total'])
    )
    mejor_agente = ranking[0][0]
    print(f'\n🏆 Agente del Año: {mejor_agente}')
    escribir_log(f'Agente del Año: {mejor_agente}')


if __name__ == '__main__':
    main()
