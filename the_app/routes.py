import csv, sqlite3
from the_app import app
from the_app.forms import ProductForm, ModProductForm

from flask import render_template, request, redirect, url_for

BASE_DATOS = app.config["BASE_DATOS"]

@app.route('/')
def index():
    fVentas = open(app.config["VENTAS"], "r")
    csvreader = csv.reader(fVentas, delimiter=",")

    d = {}
    for linea in csvreader:
        if linea[0] in d:
            d[linea[0]]["ingresos"] += float(linea[10])
            d[linea[0]]["beneficios"] += float(linea[12])
        else:
            if linea[0] != "region":
                d[linea[0]] = {"ingresos": float(linea[10]), "beneficios": float(linea[12])}

    return render_template("region.html", ventas=d)


@app.route("/paises")
def paises():
    region_name = request.values["region"]

    fVentas = open(app.config["VENTAS"], "r")
    csvreader = csv.reader(fVentas, delimiter=",")
    d = {}
    for linea in csvreader:
        if linea[0] == region_name:
            if linea[1] in d:
                d[linea[1]]["ingresos"] += float(linea[10])
                d[linea[1]]["beneficios"] += float(linea[12])
            else:
                d[linea[1]] = {"ingresos": float(linea[10]), "beneficios": float(linea[12])}


    return render_template("pais.html", ventas_pais=d, region_nm=request.values["region"])

@app.route("/productos")
def productos():
    conn = sqlite3.connect(BASE_DATOS)
    cur = conn.cursor()

    query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos;"
    productos = cur.execute(query).fetchall()

    conn.close()
    return render_template("productos.html", productos=productos)

@app.route("/addproducto", methods=["GET", "POST"])
def addproduct():
    form = ProductForm(request.form)

    if request.method == "GET":
        return render_template("newproduct.html", form=form, error_gral=False)
    else:
        if form.validate():
            conn = sqlite3.connect(BASE_DATOS)
            cur = conn.cursor()
            query = "INSERT INTO productos (tipo_producto, precio_unitario, coste_unitario) values (?, ?, ?);"
            datos = (request.values.get("tipo_producto"), request.values.get("precio_unitario"), request.values.get("coste_unitario"))
            try:
                cur.execute(query, datos)
                conn.commit()
                conn.close()
            except Exception as e:
                print("INSERT - Error en acceso a base de datos: {}".format(e))
                conn.close()
                return render_template("newproduct.html", form=form, error_gral="{}".format(e))

            return redirect(url_for("productos"))
        
        else:
            return render_template("newproduct.html", form=form, error_gral=False)

@app.route("/modificaproducto", methods=["GET", "POST"])
def modifica_producto():
    if request.method == "GET":
        id = request.values["id"]

        conn = sqlite3.connect(app.config["BASE_DATOS"])
        cur = conn.cursor()
        query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos WHERE id = ?;"

        cur.execute(query, (id,))

        fila = cur.fetchone()
        conn.close()

        if fila:
            form = ModProductForm(data={"id": fila[0], "tipo_producto": fila[1], "precio_unitario": fila[2], "coste_unitario": fila[3]})
            return render_template("modproduct.html", form=form)
        else:
            return redirect(url_for("productos"))

    else:
        form = ModProductForm(request.form)
       
        if request.form.get("modificar"):
            if form.validate():
                query = "UPDATE productos SET tipo_producto = ?, precio_unitario = ?, coste_unitario = ? WHERE id = ?;"
                tupla_data = (form.tipo_producto.data, form.precio_unitario.data, form.coste_unitario.data, form.id.data)
            else:
                return render_template("modproduct.html", form=form)

        else:
            query = "DELETE FROM productos WHERE id = ?;"
            tupla_data = (form.id.data,)

        conn = sqlite3.connect(app.config["BASE_DATOS"])
        cur = conn.cursor()
        try:
            cur.execute(query, tupla_data)
            conn.commit()
        except Exception as e:
            print("MOD/DEL - Error en acceso a base de datos: {}".format(e))

        conn.close()
        return redirect(url_for("productos"))
