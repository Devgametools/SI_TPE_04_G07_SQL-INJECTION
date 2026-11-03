# Manual de uso y pruebas

## 1. Preparación

Instala Python 3.10 o superior y abre una terminal en la carpeta del proyecto. En Windows, si `python` no funciona, prueba `py` en los comandos de creación y ejecución. Comprueba la instalación con `python --version`.

```bash
python -m venv .venv
```

Activa el entorno en cada terminal nueva:

- PowerShell: `.\.venv\Scripts\Activate.ps1`
- Símbolo del sistema (CMD): `.venv\Scripts\activate.bat`
- Ubuntu/Linux o macOS: `source .venv/bin/activate`

Si Ubuntu indica que falta `venv`, instala el paquete `python3-venv` con el gestor de paquetes. Si PowerShell bloquea la activación, puedes usar CMD o ejecutar directamente `.venv\Scripts\python.exe` en vez de `python`.

```bash
python -m pip install -r requirements.txt
```

Al terminar, `deactivate` desactiva el entorno. La base `laboratorio.db` se crea automáticamente la primera vez; para restaurar los datos iniciales, detén los servidores y elimina ese archivo. No contiene información real.

## 2. Servidor vulnerable

```bash
python app_vulnerable.py
```

Abre `http://127.0.0.1:5000`. Prueba `admin` / `clave123` y luego una contraseña incorrecta. En una segunda terminal con el entorno activado:

```bash
python ataque_sql_i.py --puerto 5000
```

El script envía cuatro casos. El tercero introduce `' OR 1=1 -- ` en el usuario: altera la condición y comenta el resto de la consulta. El cuarto utiliza `UNION SELECT` y `group_concat` para mostrar usuarios y claves ficticias; la consulta original devuelve una columna, por lo que el `UNION` también devuelve una columna. El espacio tras `--` forma parte del ejemplo.

## 3. Servidor corregido y comparación

Mantén el primer servidor abierto y, en otra terminal con el entorno activado, ejecuta:

```bash
python app_segura.py
```

Abre `http://127.0.0.1:5001`. Ejecuta en otra terminal:

```bash
python ataque_sql_i.py --puerto 5001
```

Resultados esperados:

| Caso | Vulnerable (5000) | Parametrizada (5001) |
|---|---|---|
| Credenciales válidas | HTTP 200, acceso concedido | HTTP 200, acceso concedido |
| Credenciales inválidas | HTTP 401 | HTTP 401 |
| Bypass | HTTP 200, acceso indebido | HTTP 401 |
| Extracción | HTTP 200, registros ficticios visibles | HTTP 401 |

En la versión corregida `?` representa valores separados de la estructura SQL: el texto malicioso se trata como dato. Esto mitiga esta inyección concreta, pero no reemplaza otras medidas de seguridad. Guarda capturas propias de terminales, navegador y resultados para el informe. Detén cada servidor con `Ctrl+C`.

## 4. Escaneo de puertos TCP

Escanea únicamente equipos propios o con autorización expresa. Con una aplicación de Flask en ejecución:

```bash
python escaneo_red.py
```

## 5. Seguridad de bases de datos y límites

- En aplicaciones reales almacena contraseñas mediante un algoritmo de hashing para contraseñas como Argon2id, con sal y parámetros apropiados; nunca en texto plano como en esta simulación.
- Usa consultas parametrizadas en todas las operaciones y valida tipos, tamaño y formato de las entradas. Los identificadores SQL dinámicos necesitan una lista de permitidos: no se parametrizan como valores.
- Aplica el mínimo privilegio a cuentas y procesos, restringe el acceso a archivos SQLite y a la red, y no expongas archivos de base de datos. SQLite no ofrece cuentas y roles propios como un servidor de bases de datos.
- Protege respaldos, gestiona secretos fuera del código, actualiza dependencias, audita accesos y evita mostrar errores internos al usuario. Para despliegues reales aplica HTTPS y controles de autenticación y sesión.
- Este ejemplo no implementa sesiones, hashing, CSRF, límite de intentos ni autorización; la etiqueta “segura” se refiere a la consulta parametrizada frente a estas pruebas, no a seguridad integral.

## 6. Solución de problemas

- `ModuleNotFoundError: flask`: activa el entorno correcto e instala los requisitos con ese mismo intérprete.
- Puerto ocupado: detén el proceso que lo utiliza. Los puertos de este laboratorio están definidos en los archivos de arranque y en el script de pruebas.
- No hay conexión: inicia el servidor correspondiente y comprueba el puerto. El script de ataque solo acepta los puertos locales 5000 y 5001.
- Si aparecen resultados diferentes, verifica que estés ejecutando el archivo y puerto esperados y que la base sea la creada por este proyecto.
