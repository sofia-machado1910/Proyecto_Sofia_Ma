import sqlite3

# Conecta a la base de datos
conn = sqlite3.connect("entradas.db")
cursor = conn.cursor()

# Elimina la tabla 'entradas'
cursor.execute("DROP TABLE IF EXISTS entradas")

# Elimina la tabla 'productos' (si existe)
cursor.execute("DROP TABLE IF EXISTS productos")

# Confirma las acciones
conn.commit()

# Cierra la conexión
conn.close()

print("El archivo 'entradas.db' ha sido borrado.")