from flask import Flask, render_template
import csv
# Crear la instancia de la aplicación Flask
app = Flask(__name__)


@app.route('/')
def index():
    fVentas = open("./sales10.csv", "r")
    csvreader = csv.reader(fVentas, delimiter=",")

    registros = []
    d = {}
    for linea in csvreader:
        registros.append(linea)
        if linea[0] in d:
            d[linea[0]]["ingresos"] += float(linea[10])
            d[linea[0]]["beneficios"] += float(linea[12])
        else:
            if linea[0] != "region":
                d[linea[0]] = {"ingresos": float(linea[10]), "beneficios": float(linea[12])}

    return render_template("region.html", ventas=d)
    
'''
    <mientras haya registros>

        registro = leerFichero
        registro. separar.por comas
        procesar ventas totales y beneficios totales
    
    Montar respuesta
    devolver respuesta

'''