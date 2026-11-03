"""Base SQLite de demostración: crea datos ficticios al iniciar."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / 'laboratorio.db'

def conectar():
    return sqlite3.connect(DB)

def inicializar():
    with conectar() as db:
        db.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, clave TEXT NOT NULL)')
        db.executemany('INSERT OR IGNORE INTO usuarios(usuario, clave) VALUES (?, ?)', [('admin', 'clave123'), ('estudiante', 'demo123'), ('auditor', 'auditoria123')])
