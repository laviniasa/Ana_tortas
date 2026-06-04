import sqlite3

conn = sqlite3.connect("eventos.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,
    horario TEXT,
    endereco TEXT NOT NULL,
    maps_url TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco criado!")