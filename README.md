# Laboratorio de seguridad: inyección SQL y escaneo TCP

Proyecto académico para comparar una consulta construida mediante concatenación con otra parametrizada. Utiliza Python, Flask y SQLite, y genera una base de datos local con registros ficticios. El laboratorio incluye bypass de autenticación, extracción simulada y escaneo TCP de puertos.

**Uso exclusivo en equipos propios o expresamente autorizados.** La versión vulnerable contiene una falla deliberada, utiliza contraseñas de ejemplo en texto plano y no debe publicarse ni utilizarse en producción. Ambas aplicaciones escuchan únicamente en `127.0.0.1`.

## Archivos

- `app_vulnerable.py`: servidor vulnerable en el puerto 5000.
- `app_segura.py`: servidor con consultas parametrizadas en el puerto 5001.
- `aplicacion.py`: formulario y lógica compartida que permite comparar las consultas.
- `base_datos.py`: inicialización de SQLite y registros ficticios.
- `ataque_sql_i.py`: pruebas HTTP locales de credenciales, bypass y extracción.
- `escaneo_red.py`: escáner TCP connect con rango configurable.
- `MANUAL_USO.md`: instalación, ejecución, pruebas y recomendaciones de seguridad.
- `requirements.txt`: dependencia Flask; `.gitignore` excluye entorno y base generada.

## Inicio rápido

Requiere Python 3.10 o posterior y pip. En una terminal ubicada en esta carpeta:

```bash
python -m venv .venv
```

Activa el entorno: Windows PowerShell `.\.venv\Scripts\Activate.ps1`; Windows CMD `.venv\Scripts\activate.bat`; Linux/macOS `source .venv/bin/activate`. En Linux puede ser necesario instalar el paquete de venv de la distribución.

```bash
pip install -r requirements.txt
python app_vulnerable.py
```

Abre otra terminal, activa el mismo entorno y ejecuta `python ataque_sql_i.py --puerto 5000`. Para comparar, inicia `python app_segura.py` en otra terminal y ejecuta `python ataque_sql_i.py --puerto 5001`. Los pasos detallados están en el manual.

Este material es un apoyo: la guía académica exige verificarlo y analizarlo críticamente, limitar el uso de IA al 30 % del contenido total y declarar su uso en el informe posterior.
