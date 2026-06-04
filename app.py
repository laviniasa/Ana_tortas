from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():

    conn = sqlite3.connect("eventos.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM eventos
    ORDER BY data
    """)

    eventos = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        eventos=eventos
    )

@app.route("/admin")
def admin():

    conn = sqlite3.connect("eventos.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM eventos
    """)

    eventos = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        eventos=eventos
    )

@app.route("/salvar-evento", methods=["POST"])
def salvar_evento():

    nome = request.form["nome"]
    data = request.form["data"]
    horario = request.form["horario"]
    endereco = request.form["endereco"]
    maps_url = request.form["maps_url"]

    conn = sqlite3.connect("eventos.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO eventos(
        nome,
        data,
        horario,
        endereco,
        maps_url
    )
    VALUES(?,?,?,?,?)
    """,
    (
        nome,
        data,
        horario,
        endereco,
        maps_url
    ))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/excluir/<int:id>")
def excluir(id):

    conn = sqlite3.connect("eventos.db")

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM eventos
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)