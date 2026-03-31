from datetime import datetime
from pathlib import Path

RUTA_LOG = Path('registro_misiones.txt')


def escribir_log(texto: str) -> None:
    marca = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with RUTA_LOG.open('a', encoding='utf-8') as f:
        f.write(f'[{marca}] {texto}\n')
