"""Contraparte con parámetros SQL; no es una aplicación de producción."""
from aplicacion import crear_app
app = crear_app(segura=True)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
