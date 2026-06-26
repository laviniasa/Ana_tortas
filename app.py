from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
import os


app = Flask(__name__)
app.secret_key = "ana_tortas_2026"

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


@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    if usuario == "ana" and senha == "123456":
        session["logado"] = True
        return redirect("/admin")

    return redirect("/")


@app.route("/admin")
def admin():

    if not session.get("logado"):
        return redirect("/")

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

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/salvar-evento", methods=["POST"])
def salvar_evento():

    if not session.get("logado"):
        return redirect("/")

    nome = request.form["nome"]

    data_inicio = request.form["data_inicio"]
    data_fim = request.form["data_fim"]

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    fim = datetime.strptime(data_fim, "%Y-%m-%d")

    if data_inicio == data_fim:
        data = inicio.strftime("%d/%m/%Y")

    elif inicio.month == fim.month and inicio.year == fim.year:
        data = f"{inicio.day:02d} a {fim.day:02d} de {meses[inicio.month-1]}"

    else:
        data = (
            f"{inicio.day:02d}/{inicio.month:02d} "
            f"a "
            f"{fim.day:02d}/{fim.month:02d}"
        )

    horario = request.form["horario"]
    endereco = request.form["endereco"]
    maps_url = request.form["maps_url"]

    foto = request.files["foto"]

    nome_foto = ""

    if foto and foto.filename != "":

        nome_foto = secure_filename(foto.filename)

        foto.save(
            os.path.join(
                "static",
                "eventos",
                nome_foto
            )
        )

    conn = sqlite3.connect("eventos.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO eventos(
        nome,
        data,
        horario,
        endereco,
        maps_url,
        foto
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        nome,
        data,
        horario,
        endereco,
        maps_url,
        nome_foto
    ))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/excluir/<int:id>")
def excluir(id):

    if not session.get("logado"):
        return redirect("/")

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
