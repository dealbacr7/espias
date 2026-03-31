import math
import re
from collections import Counter

MORSE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..'
}

ANAGRAMS = {
    'otnerc': 'centro',
    'laconfiden': 'confidencial',
    'larcocal': 'local'
}


def quitar_tildes(texto: str) -> str:
    reemplazos = str.maketrans('áéíóúÁÉÍÓÚüÜñÑ', 'aeiouAEIOUuUnN')
    return texto.translate(reemplazos)


def es_primo(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limite = int(math.isqrt(n))
    for i in range(3, limite + 1, 2):
        if n % i == 0:
            return False
    return True


def letra_mas_frecuente(texto: str) -> str:
    limpio = [c.lower() for c in quitar_tildes(texto) if c.isalpha()]
    conteo = Counter(limpio)
    max_frec = max(conteo.values())
    candidatas = sorted([k for k, v in conteo.items() if v == max_frec])
    return candidatas[0]


def ordenar_letras(texto: str) -> str:
    return ''.join(sorted(texto.replace(' ', '').lower()))


def a_morse(texto: str) -> str:
    palabras = []
    for palabra in quitar_tildes(texto.lower()).split():
        letras = [MORSE[c] for c in palabra if c in MORSE]
        palabras.append(' '.join(letras))
    return ' / '.join(palabras)


def rot13(texto: str) -> str:
    resultado = []
    for c in texto:
        if 'a' <= c <= 'z':
            resultado.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            resultado.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            resultado.append(c)
    return ''.join(resultado)


def generar_misiones():
    misiones = [
        {'id': 1, 'mensaje': 'Intercepta y suma los dígitos de 274961', 'respuesta_correcta': str(sum(map(int, '274961')))},
        {'id': 2, 'mensaje': "Descifra este anagrama: 'otnerc' (pista: moneda)", 'respuesta_correcta': ANAGRAMS['otnerc']},
        {'id': 3, 'mensaje': "Ubica la letra más frecuente en 'infiltración'", 'respuesta_correcta': letra_mas_frecuente('infiltración')},
        {'id': 4, 'mensaje': 'Convierte 1337 a binario (es una pista numérica)', 'respuesta_correcta': bin(1337)[2:]},
        {'id': 5, 'mensaje': "Cuenta las vocales en 'comunicacionesencriptadas'", 'respuesta_correcta': str(sum(1 for c in 'comunicacionesencriptadas' if c in 'aeiou'))},
        {'id': 6, 'mensaje': 'Calcula raíz cuadrada entera de 762423', 'respuesta_correcta': str(math.isqrt(762423))},
        {'id': 7, 'mensaje': '¿Es primo el número 177013?', 'respuesta_correcta': 'sí' if es_primo(177013) else 'no'},
        {'id': 8, 'mensaje': "Transforma la palabra 'espionaje' a mayúsculas y ordénala alfabéticamente", 'respuesta_correcta': ''.join(sorted('ESPIONAJE'))},
        {'id': 9, 'mensaje': "Repite el mensaje 'infiltrado detectado' cinco veces en una línea", 'respuesta_correcta': ' '.join(['infiltrado detectado'] * 5)},
        {'id': 10, 'mensaje': 'Convierte el número 451 a hexadecimal', 'respuesta_correcta': hex(451)[2:]},
        {'id': 11, 'mensaje': "Cuenta cuántas veces aparece la letra 'e' en 'enemigoenelterritorio'", 'respuesta_correcta': str('enemigoenelterritorio'.count('e'))},
        {'id': 12, 'mensaje': "Descifra este anagrama: 'laconfiden' (pista: documento)", 'respuesta_correcta': ANAGRAMS['laconfiden']},
        {'id': 13, 'mensaje': 'Calcula la suma de todos los números del 1 al 150', 'respuesta_correcta': str(sum(range(1, 151)))},
        {'id': 14, 'mensaje': "¿Cuántas letras tiene la palabra 'criptografía'?", 'respuesta_correcta': str(len('criptografía'))},
        {'id': 15, 'mensaje': "Invierta la palabra 'reconocimiento'", 'respuesta_correcta': 'reconocimiento'[::-1]},
        {'id': 16, 'mensaje': "Codifica 'invisible' en código Morse", 'respuesta_correcta': a_morse('invisible')},
        {'id': 17, 'mensaje': 'Multiplica 27 por 63', 'respuesta_correcta': str(27 * 63)},
        {'id': 18, 'mensaje': "Convierte la frase 'comando alfa listo' en una lista de palabras", 'respuesta_correcta': str('comando alfa listo'.split())},
        {'id': 19, 'mensaje': "¿Cuántos caracteres hay en 'redsegurainternacional2025'?", 'respuesta_correcta': str(len('redsegurainternacional2025'))},
        {'id': 20, 'mensaje': "Descifra este anagrama: 'larcocal' (pista: lugar de reunión)", 'respuesta_correcta': ANAGRAMS['larcocal']},
        {'id': 21, 'mensaje': '¿Cuál es el factorial de 6?', 'respuesta_correcta': str(math.factorial(6))},
        {'id': 22, 'mensaje': "Reemplaza todas las 'a' por 'x' en 'agente clasificado'", 'respuesta_correcta': 'agente clasificado'.replace('a', 'x')},
        {'id': 23, 'mensaje': 'Suma los dígitos de 999999', 'respuesta_correcta': str(sum(map(int, '999999')))},
        {'id': 24, 'mensaje': "Convierte 'inteligencia' en minúsculas y cuéntalas", 'respuesta_correcta': str(len('inteligencia'.lower()))},
        {'id': 25, 'mensaje': 'Divide 4096 entre 64', 'respuesta_correcta': str(4096 // 64)},
        {'id': 26, 'mensaje': "Cuenta cuántas palabras hay en 'mensaje encriptado recibido'", 'respuesta_correcta': str(len('mensaje encriptado recibido'.split()))},
        {'id': 27, 'mensaje': "Escribe 'operación oculta' sin espacios", 'respuesta_correcta': 'operaciónoculta'},
        {'id': 28, 'mensaje': "¿Cuántos caracteres tiene 'infiltraciónexitosacodificada'?", 'respuesta_correcta': str(len('infiltraciónexitosacodificada'))},
        {'id': 29, 'mensaje': "Codifica 'enemigo invisible' usando ROT13", 'respuesta_correcta': rot13('enemigo invisible')},
        {'id': 30, 'mensaje': "Ordena alfabéticamente las letras de 'secreto'", 'respuesta_correcta': ordenar_letras('secreto')},
    ]
    return misiones


def validar_respuesta(mision: dict, respuesta: str) -> bool:
    esperada = str(mision['respuesta_correcta']).strip().lower()
    recibida = str(respuesta).strip().lower()
    return esperada == recibida


def resolver_mision_por_texto(mensaje: str) -> str:
    # Resolver a partir del texto permite que el worker no necesite conocer la respuesta.
    if 'suma los dígitos de 274961' in mensaje:
        return str(sum(map(int, '274961')))
    if "anagrama: 'otnerc'" in mensaje:
        return 'centro'
    if "letra más frecuente en 'infiltración'" in mensaje:
        return letra_mas_frecuente('infiltración')
    if 'Convierte 1337 a binario' in mensaje:
        return bin(1337)[2:]
    if "Cuenta las vocales en 'comunicacionesencriptadas'" in mensaje:
        return str(sum(1 for c in 'comunicacionesencriptadas' if c in 'aeiou'))
    if 'raíz cuadrada entera de 762423' in mensaje:
        return str(math.isqrt(762423))
    if '¿Es primo el número 177013?' in mensaje:
        return 'sí' if es_primo(177013) else 'no'
    if "'espionaje' a mayúsculas y ordénala" in mensaje:
        return ''.join(sorted('ESPIONAJE'))
    if "Repite el mensaje 'infiltrado detectado'" in mensaje:
        return ' '.join(['infiltrado detectado'] * 5)
    if 'Convierte el número 451 a hexadecimal' in mensaje:
        return hex(451)[2:]
    if "aparece la letra 'e' en 'enemigoenelterritorio'" in mensaje:
        return str('enemigoenelterritorio'.count('e'))
    if "anagrama: 'laconfiden'" in mensaje:
        return 'confidencial'
    if 'suma de todos los números del 1 al 150' in mensaje:
        return str(sum(range(1, 151)))
    if "'criptografía'" in mensaje:
        return str(len('criptografía'))
    if "Invierta la palabra 'reconocimiento'" in mensaje:
        return 'reconocimiento'[::-1]
    if "Codifica 'invisible' en código Morse" in mensaje:
        return a_morse('invisible')
    if 'Multiplica 27 por 63' in mensaje:
        return str(27 * 63)
    if "'comando alfa listo' en una lista de palabras" in mensaje:
        return str('comando alfa listo'.split())
    if "'redsegurainternacional2025'" in mensaje:
        return str(len('redsegurainternacional2025'))
    if "anagrama: 'larcocal'" in mensaje:
        return 'local'
    if 'factorial de 6' in mensaje:
        return str(math.factorial(6))
    if "Reemplaza todas las 'a' por 'x'" in mensaje:
        return 'agente clasificado'.replace('a', 'x')
    if 'Suma los dígitos de 999999' in mensaje:
        return str(sum(map(int, '999999')))
    if "'inteligencia' en minúsculas y cuéntalas" in mensaje:
        return str(len('inteligencia'.lower()))
    if 'Divide 4096 entre 64' in mensaje:
        return str(4096 // 64)
    if "cuántas palabras hay en 'mensaje encriptado recibido'" in mensaje:
        return str(len('mensaje encriptado recibido'.split()))
    if "'operación oculta' sin espacios" in mensaje:
        return 'operaciónoculta'
    if "'infiltraciónexitosacodificada'" in mensaje:
        return str(len('infiltraciónexitosacodificada'))
    if "'enemigo invisible' usando ROT13" in mensaje:
        return rot13('enemigo invisible')
    if "'secreto'" in mensaje:
        return ordenar_letras('secreto')
    return 'NO_RESUELTA'
