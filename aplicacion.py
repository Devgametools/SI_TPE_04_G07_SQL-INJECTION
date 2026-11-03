"""Aplicación común para comparar dos formas de consultar SQLite."""
import sqlite3
from flask import Flask, render_template, request
from base_datos import conectar, inicializar

def crear_app(segura):
    app = Flask(__name__)
    inicializar()

    @app.route('/', methods=['GET', 'POST'])
    def inicio():
        resultado = None
        estado = 200
        if request.method == 'POST':
            usuario = request.form.get('usuario', '')
            clave = request.form.get('clave', '')
            try:
                with conectar() as db:
                    if segura:
                        fila = db.execute('SELECT usuario FROM usuarios WHERE usuario = ? AND clave = ?', (usuario, clave)).fetchone()
                    else:
                        # INTENCIONALMENTE INSEGURO: solo para este laboratorio local.
                        consulta = f"SELECT usuario FROM usuarios WHERE usuario = '{usuario}' AND clave = '{clave}'"
                        fila = db.execute(consulta).fetchone()
                if fila:
                    resultado = f'Acceso concedido. Usuario: {fila[0]}'
                else:
                    resultado, estado = 'Credenciales inválidas.', 401
            except sqlite3.Error:
                resultado, estado = 'Error en la consulta SQL.', 400
        return render_template('index.html', resultado=resultado, modo='seguro' if segura else 'vulnerable'), estado

    return app
