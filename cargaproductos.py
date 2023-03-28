import csv, sqlite3

filename = "./sales10.csv"
database = "./data/ventas.db"

conn = sqlite3.connect(database)
cur = conn.cursor()

fSales = open(filename, "r")
csvreader = csv.reader(fSales, delimiter=",")

headerRow = next(csvreader)
print(headerRow)

query = "INSERT OR IGNORE into productos (tipo_producto, precio_unitario, coste_unitario) values (?, ?, ?);"
for dataRow in csvreader:
    tupla_datos = ( dataRow[2], float(dataRow[9]), float(dataRow[10]) )
    cur.execute(query, tupla_datos)

conn.commit()
conn.close()