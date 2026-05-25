import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Funciones para cargar y guardar datos
def cargar_datos():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"recordatorios": [], "comidas": [], "pendientes": []}

def guardar_datos(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Recordatorios
@app.route("/recordatorios", methods=["GET", "POST"])
def recordatorios():
    data = cargar_datos()
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]  # texto libre
        data["recordatorios"].append({"nombre": nombre, "categoria": categoria, "fecha": fecha})
        guardar_datos(data)
        return redirect(url_for("recordatorios"))
    return render_template("recordatorios.html", recordatorios=data["recordatorios"])

# Comidas
@app.route("/comidas", methods=["GET", "POST"])
def comidas():
    data = cargar_datos()
    if request.method == "POST":
        dia = request.form["dia"]
        menu = request.form["menu"]
        data["comidas"].append({"dia": dia, "menu": menu})
        guardar_datos(data)
        return redirect(url_for("comidas"))
    return render_template("comidas.html", comidas=data["comidas"])

# Pendientes
@app.route("/pendientes", methods=["GET", "POST"])
def pendientes():
    data = cargar_datos()
    if "pendientes" not in data:
        data["pendientes"] = []
    if request.method == "POST":
        tarea = request.form["tarea"]
        data["pendientes"].append({"tarea": tarea})
        guardar_datos(data)
        return redirect(url_for("pendientes"))
    return render_template("pendientes.html", pendientes=data["pendientes"])

# Visor de datos JSON
@app.route("/datos")
def datos():
    data = cargar_datos()
    json_pretty = json.dumps(data, indent=4, ensure_ascii=False)
    return render_template("datos.html", json_data=json_pretty)

if __name__ == "__main__":
    app.run(debug=True)
