# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import pytz

from flask_cors import CORS, cross_origin

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_23005263_bd",
    user="u760464709_23005263_usr",
    password="8Bw]!4L7*UV"
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("index.html")

@app.route("/app")
def app2():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return "<h5>Hola, soy la view app</h5>";

@app.route("/Decoraciones")
def decoraciones():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Decoracion,
           NombreMaterial

    FROM decoraciones

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()

    return render_template("Decoracions.html", decoraciones=registros)

@app.route("/Decoraciones/buscar", methods=["GET"])
def buscarDecoraciones():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Decoracion,
           NombreMaterial

    FROM decoraciones

    WHERE NombreMaterial LIKE %s

    ORDER BY Id_Decoracion DESC

    LIMIT 10 OFFSET 0
    """
    val    = (busqueda )

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()

    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/v", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def guardarDecoracion():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    nombre      = request.form["nombre"]
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE decoraciones

        SET Nombre_Decoracion = %s,


        WHERE Id_Decoracion = %s
        """
        val = (nombre, id)
    else:
        sql = """
        INSERT INTO decoraciones (Nombre_Decoracion)
                    VALUES    (%s,          %s)
        """
        val =                 (nombre )
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

@app.route("/Decoraciones/<int:id>")
def editarDecoracion(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Decoracion, NombreMaterial

    FROM Decoracions

    WHERE Id_Decoracion = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/Decoraciones/eliminar", methods=["POST"])
def eliminarDecoracion():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM Decoracions
    WHERE Id_Decoracion = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))
