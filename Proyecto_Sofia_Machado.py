import requests
import json
import datetime
import random
from collections import namedtuple
from functools import reduce
import matplotlib.pyplot as plt
import os
from itertools import permutations
import sqlite3

# Clase para representar un equipo
class Equipo:
    def __init__(self, nombre, codigo_fifa, grupo):
        self.nombre = nombre
        self.codigo_fifa = codigo_fifa
        self.grupo = grupo

# Clase para representar un estadio
class Estadio:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

# Clase para representar un partido
class Partido:
    def __init__(self, equipo_local, equipo_visitante, fecha_hora, estadio):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha_hora = fecha_hora
        self.estadio = estadio
        self.asistencia = 0

# Clase para representar un asiento
class Asiento:
    def __init__(self, numero, fila, ocupado):
        self.numero = numero
        self.fila = fila
        self.ocupado = ocupado

# Clase para representar un cliente
class Cliente:
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

# Clase para representar una entrada
class Entrada:
    def __init__(self, cliente, partido, tipo, asiento, costo, codigo_unico):
        self.cliente = cliente
        self.partido = partido
        self.tipo = tipo
        self.asiento = asiento
        self.costo = costo
        self.codigo_unico = codigo_unico

# Clase para representar un producto
class Producto:
    def __init__(self, nombre, tipo, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio

# Clase para representar una orden de restaurante
class OrdenRestaurante:
    def __init__(self, cliente, productos, costo):
        self.cliente = cliente
        self.productos = productos
        self.costo = costo

# Clase para representar un asiento en el estadio
class Seat:
    def __init__(self, row, column, seat_type):
        self.row = row
        self.column = column
        self.occupied = False
        self.seat_type = seat_type

    # Ocupa un asiento
    def occupy(self):
        self.occupied = True

    # Desocupa un asiento
    def vacate(self):
        self.occupied = False

# Clase para representar el estadio
class Stadium:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        # Crea una matriz de asientos
        self.seats = [[Seat(row, column, "regular") for column in range(columns)] for row in range(rows)]

    # Imprime el estadio
    def print_stadium(self):
        # Calcula cuántas secciones se necesitan
        num_sections = (self.columns + 29) // 30

        # Imprime cada sección
        for section in range(num_sections):
            start_column = section * 30
            end_column = min(start_column + 30, self.columns)

            # Imprime encabezado de la sección
            print(f"\nSección {chr(ord('A') + section)}")
            print("   ", end="")
            # Imprime numeración de columnas comenzando en 1 para cada sección
            for column in range(start_column, end_column):
                # La numeración comienza en 1 y se ajusta al índice de la columna
                print(f"{column - start_column + 1:2d} ", end=" ") 
            print()

            # Imprime asientos
            for row in range(self.rows):
                print(f"{row + 1:2d} ", end="")
                for column in range(start_column, end_column):
                    seat = self.seats[row][column]
                    if seat.occupied:
                        print("[X]", end=" ")
                    else:
                        print("[ ]", end=" ")
                print()

    # Ocupa un asiento específico
    def occupy_seat(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.seats[row][column].occupy()
            return True
        else:
            return False

    # Guarda la información de los asientos ocupados en un archivo
    def save_occupied_seats(self):
        with open("occupied_seats.json", "w") as f:
            occupied_seats = []
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.seats[row][column].occupied:
                        occupied_seats.append({"row": row, "column": column})
            json.dump(occupied_seats, f)

    # Carga la información de los asientos ocupados desde un archivo
    def load_occupied_seats(self):
        try:
            with open("occupied_seats.json", "r") as f:
                occupied_seats_data = json.load(f)
                for seat_data in occupied_seats_data:
                    self.seats[seat_data["row"]][seat_data["column"]].occupy()
        except FileNotFoundError:
            pass

# Función para verificar si un número es vampiro
def es_numero_vampiro(cedula):
    """
    Verifica si una cédula es un número vampiro.
    """
    cedula_str = str(cedula)
    largo = len(cedula_str)

    # Si la cédula no tiene una longitud par, no puede ser un número vampiro.
    if largo % 2 != 0:
        return False

    # Genera todas las permutaciones posibles de los dígitos de la cédula.
    permutaciones = list(permutations(cedula_str))

    # Itera a través de todas las permutaciones.
    for permutacion in permutaciones:
        # Divide la permutación en dos partes iguales.
        mitad1 = int("".join(permutacion[:largo // 2]))
        mitad2 = int("".join(permutacion[largo // 2:]))

        # Verifica si la multiplicación de las mitades es igual a la cédula.
        if mitad1 * mitad2 == cedula and mitad1 != 1 and mitad1 != mitad2:
            return True

    # Si no se encontró ninguna permutación válida, la cédula no es un número vampiro.
    return False

# Función para verificar si un número es perfecto
def es_numero_perfecto(numero):
    if numero <= 1:
        return False
    divisores = [1]
    for i in range(2, numero):
        if numero % i == 0:
            divisores.append(i)
    suma_divisores = reduce(lambda x, y: x + y, divisores)
    return suma_divisores == numero

# Función para cargar equipos desde la API
def cargar_equipos():
    equipos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
    equipos = []
    for equipo_json in equipos_json:
        nombre = equipo_json["name"]
        codigo_fifa = equipo_json["code"]
        grupo = equipo_json["group"]
        equipos.append(Equipo(nombre, codigo_fifa, grupo))
    return equipos

# Función para cargar estadios desde la API
def cargar_estadios():
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    estadios = []
    for estadio_json in estadios_json:
        nombre = estadio_json["name"]
        ubicacion = estadio_json["city"]
        estadios.append(Estadio(nombre, ubicacion))
    return estadios

# Función para cargar partidos desde la API
def cargar_partidos():
    partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
    partidos = []
    for partido_json in partidos_json:
        equipo_local_codigo_fifa = partido_json["home"]
        equipo_visitante_codigo_fifa = partido_json["away"]
        fecha_hora_str = partido_json["date"]
        estadio_nombre = partido_json["stadium_id"]
        partidos.append(Partido(equipo_local_codigo_fifa, equipo_visitante_codigo_fifa, fecha_hora_str, estadio_nombre))
    return partidos

# Función para buscar un equipo por su código FIFA
def buscar_equipo_por_codigo_fifa(codigo_fifa):
    for equipo in equipos:
        if equipo.codigo_fifa == codigo_fifa:
            return equipo
    return None

# Función para buscar un estadio por su nombre
def buscar_estadio_por_nombre(nombre):
    for estadio in estadios:
        if estadio.nombre == nombre:
            return estadio
    return None

# Función para buscar partidos por fecha
def buscar_partido_por_fecha(fecha):
    partidos_filtrados = []
    for partido in partidos:
        if partido.fecha_hora.date() == fecha:
            partidos_filtrados.append(partido)
    return partidos_filtrados

# Función para buscar partidos por estadio
def buscar_partido_por_estadio(estadio):
    partidos_filtrados = []
    for partido in partidos:
        if partido.estadio == estadio:
            partidos_filtrados.append(partido)
    return partidos_filtrados

# Función para buscar partidos por equipo
def buscar_partido_por_equipo(equipo):
    partidos_filtrados = []
    for partido in partidos:
        if partido.equipo_local == equipo or partido.equipo_visitante == equipo:
            partidos_filtrados.append(partido)
    return partidos_filtrados

# Función para crear un cliente
def crear_cliente(nombre, cedula, edad):
    cliente = Cliente(nombre, cedula, edad)
    clientes.append(cliente)
    guardar_clientes()
    return cliente

# Función para buscar un cliente por su cédula
def buscar_cliente_por_cedula(cedula):
    for cliente in clientes:
        if cliente.cedula == cedula:
            return cliente
    return None

# Función para crear una entrada
def crear_entrada(cliente, partido, tipo, asiento, costo):
    entrada = Entrada(cliente, partido, tipo, asiento, costo)
    entradas.append(entrada)
    guardar_entradas()
    return entrada

# Función para calcular el costo de una entrada
def calcular_costo_entrada(partido, tipo, cedula):
    costo = 0
    if tipo == "General":
        costo = 35
    elif tipo == "VIP":
        costo = 75
    return costo

# Función para actualizar un asiento
def actualizar_asiento(asiento):
    for i in range(len(asientos)):
        if asientos[i].numero == asiento.numero and asientos[i].fila == asiento.fila:
            asientos[i] = asiento
            break
    guardar_asientos()

# Función para crear un producto
def crear_producto(nombre, tipo, precio):
    producto = Producto(nombre, tipo, precio)
    productos.append(producto)
    guardar_productos()
    return producto

# Función para buscar un producto por su nombre
def buscar_producto_por_nombre(nombre):
    for producto in productos:
        if producto.nombre == nombre:
            return producto
    return None

# Función para buscar productos por tipo
def buscar_productos_por_tipo(tipo):
    productos_filtrados = []
    for producto in productos:
        if producto.tipo == tipo:
            productos_filtrados.append(producto)
    return productos_filtrados

# Función para buscar productos por precio
def buscar_productos_por_precio(precio_min, precio_max):
    productos_filtrados = []
    for producto in productos:
        if producto.precio >= precio_min and producto.precio <= precio_max:
            productos_filtrados.append(producto)
    return productos_filtrados

# Función para crear una orden de restaurante
def crear_orden_restaurante(cliente, productos):
    costo_total = 0
    for producto in productos:
        costo_total += producto.precio
    orden = OrdenRestaurante(cliente, productos, costo_total)
    ordenes_restaurante.append(orden)
    guardar_ordenes_restaurante()
    return orden

# Función para calcular el descuento de una orden
def calcular_descuento_orden(orden):
    if es_numero_perfecto(orden.cliente.cedula):
        return 0.15
    return 0

# Función para realizar una venta en el restaurante
def realizar_venta_restaurante(cliente, productos):
    orden = crear_orden_restaurante(cliente, productos)
    descuento = calcular_descuento_orden(orden)
    costo_total = orden.costo * (1 - descuento)
    print(f"Su orden tiene un descuento de {descuento * 100}%.")
    print(f"El costo total de su orden es: {costo_total}")
    for producto in productos:
        restar_inventario(producto)

# Función para restar inventario
def restar_inventario(producto):
    for i in range(len(productos)):
        if productos[i].nombre == producto.nombre:
            productos[i].precio -= 1
            break
    guardar_productos()

# Función para cargar equipos desde un archivo
def cargar_equipos_desde_archivo(archivo):
    global equipos
    equipos = []
    with open(archivo, "r") as f:
        equipos_json = json.load(f)
        for equipo_json in equipos_json:
            equipos.append(Equipo(equipo_json["nombre"], equipo_json["codigo_fifa"], equipo_json["grupo"]))

# Función para guardar equipos en un archivo
def guardar_equipos():
    equipos_json = []
    for equipo in equipos:
        equipos_json.append({"nombre": equipo.nombre, "codigo_fifa": equipo.codigo_fifa, "grupo": equipo.grupo})
    with open("equipos.json", "w") as f:
        json.dump(equipos_json, f)

# Función para cargar estadios desde un archivo
def cargar_estadios_desde_archivo(archivo):
    global estadios
    estadios = []
    with open(archivo, "r", encoding='utf-8') as f:  
        estadios_json = json.load(f)
        for estadio_json in estadios_json:
            estadios.append(Estadio(estadio_json["name"], estadio_json["city"]))

# Función para guardar estadios en un archivo
def guardar_estadios():
    estadios_json = []
    for estadio in estadios:
        estadios_json.append({"nombre": estadio.nombre, "ubicacion": estadio.ubicacion})
    with open("estadios.json", "w") as f:
        json.dump(estadios_json, f)

# Función para cargar partidos desde un archivo
def cargar_partidos_desde_archivo(archivo):
    global partidos
    partidos = []
    with open(archivo, "r") as f:
        partidos_json = json.load(f)
        for partido_json in partidos_json:
            fecha_hora = datetime.datetime.strptime(partido_json["date"], "%Y-%m-%d")
            partidos.append(Partido(partido_json["home"], partido_json["away"], fecha_hora, partido_json["stadium_id"]))

# Función para guardar partidos en un archivo
def guardar_partidos():
    partidos_json = []
    for partido in partidos:
        partidos_json.append({"equipo_local": partido.equipo_local, "equipo_visitante": partido.equipo_visitante, "fecha_hora": partido.fecha_hora.isoformat(), "estadio": partido.estadio})
    with open("partidos.json", "w") as f:
        json.dump(partidos_json, f)

# Función para cargar clientes desde un archivo
def cargar_clientes_desde_archivo(archivo):
    global clientes
    clientes = []
    with open(archivo, "r") as f:
        clientes_json = json.load(f)
        for cliente_json in clientes_json:
            clientes.append(Cliente(cliente_json["nombre"], cliente_json["cedula"], cliente_json["edad"]))

# Función para guardar clientes en un archivo
def guardar_clientes():
    clientes_json = []
    for cliente in clientes:
        clientes_json.append({"nombre": cliente.nombre, "cedula": cliente.cedula, "edad": cliente.edad})
    with open("clientes.json", "w") as f:
        json.dump(clientes_json, f)

# Función para cargar entradas desde un archivo
def cargar_entradas_desde_archivo(archivo):
    global entradas
    entradas = []
    with open(archivo, "r") as f:
        entradas_json = json.load(f)
        for entrada_json in entradas_json:
            cliente = buscar_cliente_por_cedula(entrada_json["cliente_cedula"])
            partido = buscar_partido_por_fecha(datetime.datetime.strptime(entrada_json["partido_fecha_hora"], "%Y-%m-%d").date())
            asiento = buscar_asiento_por_numero(entrada_json["asiento_numero"], entrada_json["asiento_fila"])
            entradas.append(Entrada(cliente, partido, entrada_json["tipo"], asiento, entrada_json["costo"]))

# Función para guardar entradas en un archivo
def guardar_entradas():
    entradas_json = []
    for entrada in entradas:
        entradas_json.append({"cliente_cedula": entrada.cliente.cedula, "partido_fecha_hora": entrada.partido.fecha_hora.isoformat(), "tipo": entrada.tipo, "asiento_numero": entrada.asiento.numero, "asiento_fila": entrada.asiento.fila, "costo": entrada.costo})
    with open("entradas.json", "w") as f:
        json.dump(entradas_json, f)

# Función para cargar asientos desde un archivo
def cargar_asientos_desde_archivo(archivo):
    global asientos
    asientos = []
    with open(archivo, "r") as f:
        asientos_json = json.load(f)
        for asiento_json in asientos_json:
            asientos.append(Asiento(asiento_json["numero"], asiento_json["fila"], asiento_json["ocupado"]))

# Función para guardar asientos en un archivo
def guardar_asientos():
    asientos_json = []
    for asiento in asientos:
        asientos_json.append({"numero": asiento.numero, "fila": asiento.fila, "ocupado": asiento.ocupado})
    with open("asientos.json", "w") as f:
        json.dump(asientos_json, f)

# Función para cargar productos desde un archivo
def cargar_productos_desde_archivo(archivo):
    global productos
    productos = []
    with open(archivo, "r") as f:
        productos_json = json.load(f)
        for producto_json in productos_json:
            productos.append(Producto(producto_json["nombre"], producto_json["tipo"], producto_json["precio"]))

# Función para guardar productos en un archivo
def guardar_productos():
    productos_json = []
    for producto in productos:
        productos_json.append({"nombre": producto.nombre, "tipo": producto.tipo, "precio": producto.precio})
    with open("productos.json", "w") as f:
        json.dump(productos_json, f)

# Función para cargar órdenes de restaurante desde un archivo
def cargar_ordenes_restaurante_desde_archivo(archivo):
    global ordenes_restaurante
    ordenes_restaurante = []
    with open(archivo, "r") as f:
        ordenes_restaurante_json = json.load(f)
        for orden_restaurante_json in ordenes_restaurante_json:
            cliente = buscar_cliente_por_cedula(orden_restaurante_json["cliente_cedula"])
            productos = []
            for producto_json in orden_restaurante_json["productos"]:
                producto = buscar_producto_por_nombre(producto_json["nombre"])
                productos.append(producto)
            ordenes_restaurante.append(OrdenRestaurante(cliente, productos, orden_restaurante_json["costo"]))

# Función para guardar órdenes de restaurante en un archivo
def guardar_ordenes_restaurante():
    ordenes_restaurante_json = []
    for orden_restaurante in ordenes_restaurante:
        productos_json = []
        for producto in orden_restaurante.productos:
            productos_json.append({"nombre": producto.nombre})
        ordenes_restaurante_json.append({"cliente_cedula": orden_restaurante.cliente.cedula, "productos": productos_json, "costo": orden_restaurante.costo})
    with open("ordenes_restaurante.json", "w") as f:
        json.dump(ordenes_restaurante_json, f)

# Función para buscar partidos por fecha desde la API
def buscar_partido_por_fecha_api(fecha):
    partidos_filtrados = []
    partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
    for partido_json in partidos_json:
        fecha_hora_str = partido_json["date"]
        # Convertir fecha_hora_str a datetime
        fecha_hora = datetime.datetime.strptime(fecha_hora_str, "%Y-%m-%d")
        if fecha_hora.date() == fecha:
            equipo_local_codigo_fifa = partido_json["home"]["code"]
            equipo_visitante_codigo_fifa = partido_json["away"]["code"]
            estadio_nombre = partido_json["stadium_id"]
            # Buscar nombres de los equipos en la API
            equipo_local_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_local_codigo_fifa)
            equipo_visitante_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_visitante_codigo_fifa)
            partidos_filtrados.append(Partido(equipo_local_nombre, equipo_visitante_nombre, fecha_hora, estadio_nombre))
    return partidos_filtrados

# Función para buscar partidos por estadio desde la API
def buscar_partido_por_estadio_api(estadio_nombre):
    partidos_filtrados = []
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    for estadio_json in estadios_json:
        if estadio_json["name"] == estadio_nombre:
            estadio_id = estadio_json["id"]
            partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
            for partido_json in partidos_json:
                if partido_json["stadium_id"] == estadio_id:
                    equipo_local_codigo_fifa = partido_json["home"]["code"]
                    equipo_visitante_codigo_fifa = partido_json["away"]["code"]
                    fecha_hora_str = partido_json["date"]
                    # Buscar nombres de los equipos en la API
                    equipo_local_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_local_codigo_fifa)
                    equipo_visitante_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_visitante_codigo_fifa)
                    partidos_filtrados.append(Partido(equipo_local_nombre, equipo_visitante_nombre, fecha_hora_str, estadio_id))
    return partidos_filtrados

# Función para buscar partidos por equipo desde la API
def buscar_partido_por_equipo_api(equipo_nombre):
    partidos_filtrados = []
    partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
    for partido_json in partidos_json:
        equipo_local_codigo_fifa = partido_json["home"]["code"]
        equipo_visitante_codigo_fifa = partido_json["away"]["code"]
        equipo_local_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_local_codigo_fifa)
        equipo_visitante_nombre = obtener_nombre_equipo_por_codigo_fifa(equipo_visitante_codigo_fifa)
        if equipo_local_nombre == equipo_nombre or equipo_visitante_nombre == equipo_nombre:
            estadio_nombre = partido_json["stadium_id"]
            fecha_hora_str = partido_json["date"]
            fecha_hora = datetime.datetime.strptime(fecha_hora_str, "%Y-%m-%d").date()
            partidos_filtrados.append(Partido(equipo_local_nombre, equipo_visitante_nombre, fecha_hora, estadio_nombre))
    return partidos_filtrados

# Función para obtener el nombre de un equipo por su código FIFA
def obtener_nombre_equipo_por_codigo_fifa(codigo_fifa):
    equipos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
    for equipo_json in equipos_json:
        if equipo_json["code"] == codigo_fifa:
            return equipo_json["name"]
    return None

# Función para buscar un partido por estadio
def buscar_partido_por_estadio(estadio_nombre):
    partidos_filtrados = []
    for partido in partidos:
        estadio = buscar_estadio_por_nombre(partido.estadio)
        if estadio is not None and estadio.nombre == estadio_nombre:
            partidos_filtrados.append(partido)
    return partidos_filtrados

# Función para obtener el nombre de un estadio por su ID
def obtener_nombre_estadio_por_id(estadio_id):
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    for estadio_json in estadios_json:
        if estadio_json["id"] == estadio_id:
            return estadio_json["name"]
    return None

# Función para actualizar la asistencia de un partido
def actualizar_partido(partido):
    for i in range(len(partidos)):
        if partidos[i].fecha_hora == partido.fecha_hora and partidos[i].equipo_local == partido.equipo_local and partidos[i].equipo_visitante == partido.equipo_visitante:
            partidos[i] = partido
            break
    guardar_partidos()

# Función para buscar un asiento por su número y fila
def buscar_asiento_por_numero(numero, fila):
    for asiento in asientos:
        if asiento.numero == numero and asiento.fila == fila:
            return asiento
    return None

# Función para mostrar el mapa del estadio
def mostrar_mapa_estadio(entradas, filas, asientos_por_fila):
    # Generar el mapa del estadio
    mapa = ""
    for fila in range(1, filas + 1):
        fila_str = f"Fila {fila}: "
        for asiento in range(1, asientos_por_fila + 1):
            asiento_ocupado = False
            for entrada in entradas:
                if entrada.asiento.fila == fila and entrada.asiento.numero == asiento:
                    asiento_ocupado = True
                    break
            if asiento_ocupado:
                fila_str += "X "
            else:
                fila_str += f"{asiento:02} "
        mapa += fila_str + "\n"

    print(mapa)

# Función para vender una entrada
def vender_entrada(cliente, partido, tipo):
    entrada = None

    # Solicitar sección, fila y columna al usuario
    print("Ingrese los datos del asiento")
    seccion = input("Ingrese la sección (A-Z): ").upper()
    fila = int(input("Ingrese el número de fila: "))
    columna = int(input("Ingrese el número de columna: "))

    # Convertir la sección a un índice de sección
    seccion_index = ord(seccion) - ord('A')

    # Calcular la columna real en el estadio
    columna_real = (seccion_index * 30) + columna - 1

    # Verificar si el asiento está ocupado
    if stadium.occupy_seat(fila - 1, columna_real):
        # Calcular el costo de la entrada
        costo = calcular_costo_entrada(partido, tipo, cliente.cedula)
        codigo_unico = generar_codigo_unico()
        # Mostrar el costo al cliente
        subtotal = costo
        descuento = 0
        if es_numero_vampiro(cliente.cedula):
            descuento = 0.5
            print("¡Felicidades! Su cédula es un número vampiro, por lo que tiene un 50% de descuento.")

        iva = costo * 0.16
        print(f"Asiento: {seccion}{fila}{columna}.")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Descuento: ${subtotal * descuento:.2f}")
        print(f"IVA (16%): ${iva}")
        print(f"Total: ${(costo + iva)-descuento}")

        # Confirmar pago
        pagar = input("¿Desea proceder a pagar la entrada? (s/n): ").lower()
        if pagar == "s":
            print(f"Estadio: {stadium_data['name']}")#----
            print(f"Ciudad: {stadium_data['city']}")
            stadium.print_stadium()#-----
            print("Pago exitoso.")
            print(f"Asiento {seccion}{fila}{columna} ocupado correctamente.")
            print(f"Código único del boleto: {codigo_unico}")
            print("¡Disfrute del partido!")
            asiento = Asiento(columna_real, fila, True)
            entrada = Entrada(cliente, partido, tipo, asiento, costo, codigo_unico) 
            guardar_entrada(entrada, asiento)
        else:
            print("Compra cancelada.")
            # Liberar el asiento
            stadium.seats[fila - 1][columna_real].vacate()
    else:
        print("Asiento inválido o ocupado. Por favor, seleccione otro asiento.")

    return entrada

# Función para obtener los restaurantes de un estadio
def obtener_restaurantes_estadio(estadio_nombre):
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()

    for estadio in estadios_json:
        if estadio["name"] == estadio_nombre:
            return estadio["restaurants"]

    return []

# Función para mostrar los restaurantes disponibles
def mostrar_restaurantes(restaurantes):
    if not restaurantes:
        print("No se encontraron restaurantes en este estadio.")
        return

    print("Restaurantes disponibles:")
    for i, restaurante in enumerate(restaurantes):
        print(f"{i+1}. {restaurante['name']}")

# Función para mostrar los productos de un restaurante
def mostrar_productos_restaurante(restaurante):
    productos = restaurante["products"]

    if not productos:
        print("No se encontraron productos en este restaurante.")
        return None  # Retorna None si no hay productos

    print("Todos los productos disponibles en este establecimiento:")
    for i, producto in enumerate(productos):
        print(f"{i+1}. {producto['name']} - {producto['adicional']} - ${producto['price']}")

    # Retorna la lista de productos si se encontraron
    return productos

# Función para buscar productos por nombre, tipo o precio
def buscar_productos(productos, tipo_busqueda, valor_busqueda):
    productos_filtrados = []

    for producto in productos:
        if tipo_busqueda == "name" and producto["name"] == valor_busqueda:
            productos_filtrados.append(producto)
        elif tipo_busqueda == "additional" and producto["adicional"] == valor_busqueda:
            productos_filtrados.append(producto)
        elif tipo_busqueda == "price":
            try:
                precio = valor_busqueda
                if producto["price"] == precio:
                    productos_filtrados.append(producto)
            except ValueError:
                print("Valor de precio inválido.")

    return productos_filtrados

# Función para gestionar el módulo de restaurantes
def gestionar_restaurantes():
    estadio_nombre = input("Ingrese el nombre del estadio al que va a asistir: ")

    restaurantes = obtener_restaurantes_estadio(estadio_nombre)
    mostrar_restaurantes(restaurantes)

    if not restaurantes:
        return

    opcion_restaurante = int(input("Seleccione el número del restaurante: "))
    if 1 <= opcion_restaurante <= len(restaurantes):
        restaurante = restaurantes[opcion_restaurante - 1]
        mostrar_productos_restaurante(restaurante)

        while True:
            print("\n¿Cómo desea buscar los productos?")
            print("1. Por nombre")
            print("2. Por tipo")
            print("3. Por precio")
            print("4. Volver")
            opcion_productos = input("Seleccione la opción que desea: ")

            if opcion_productos == "1":
                tipo_busqueda = "name"
            elif opcion_productos == "2":
                tipo_busqueda = "additional"
            elif opcion_productos == "3":
                tipo_busqueda = "price"
            elif opcion_productos == "4":
                break
            else:
                print("Opción inválida.")
                continue

            valor_busqueda = input("Ingrese el valor a buscar: ")
            productos_filtrados = buscar_productos(restaurante["products"], tipo_busqueda, valor_busqueda)

            if productos_filtrados:
                print("Productos encontrados:")
                for i, producto in enumerate(productos_filtrados):
                    print(f"{i+1}. {producto['name']} - {producto['adicional']} - ${producto['price']}")

                # Seleccionar producto
                while True:
                    try:
                        opcion_producto = int(input("Seleccione el número del producto: "))
                        if 1 <= opcion_producto <= len(productos_filtrados):
                            producto_seleccionado = productos_filtrados[opcion_producto - 1]
                            break
                        else:
                            print("Opción inválida.")
                    except ValueError:
                        print("Ingrese un número válido.")

                # Mostrar precio con IVA
                precio_con_iva = float(producto_seleccionado["price"]) * 1.16
                print(f"El precio del producto {producto_seleccionado['name']} con IVA (16%) es: ${precio_con_iva:.2f}")

            else:
                print("No se encontraron productos que coincidan con la búsqueda.")

# Función para gestionar la compra de productos en el módulo de aficionados
def gestionar_restaurantes_compra(cliente):
    global estadio_nombre
    if not restaurantes:
        return

    opcion_restaurante = int(input("Seleccione el número del restaurante: "))
    if 1 <= opcion_restaurante <= len(restaurantes):
        restaurante = restaurantes[opcion_restaurante - 1]
        estadio_nombre_restaurante = estadio_nombre
        # Lista para almacenar los productos seleccionados
        productos_seleccionados = []

        while True:
            print("\n¿Cómo desea buscar los productos?")
            print("1. Por nombre")
            print("2. Por tipo")
            print("3. Por precio")
            print("4. Ver todos los productos")
            print("5. Finalizar compra")
            opcion_productos = input("Seleccione la opción que desea: ")

            if opcion_productos == "1":
                tipo_busqueda = "name"
            elif opcion_productos == "2":
                tipo_busqueda = "additional"
            elif opcion_productos == "3":
                tipo_busqueda = "price"
            elif opcion_productos == "4":
                # Mostrar todos los productos y permitir selección
                productos_filtrados = mostrar_productos_restaurante(restaurante)
                if productos_filtrados is not None:  # Verifica si hay productos
                    while True:
                        try:
                            opcion_producto = int(input("Seleccione el número del producto (o ingrese 0 para volver): "))
                            if opcion_producto == 0:
                                break
                            elif 1 <= opcion_producto <= len(productos_filtrados):
                                producto_seleccionado = productos_filtrados[opcion_producto - 1]

                                # Validar edad para bebidas alcohólicas
                                if producto_seleccionado["adicional"] == "alcoholic" and cliente.edad < 18:
                                    print("Lo siento, no puedes comprar bebidas alcohólicas.")
                                else:
                                    productos_seleccionados.append(producto_seleccionado)
                                    print(f"Producto {producto_seleccionado['name']} agregado al carrito.")
                            else:
                                print("Opción inválida.")
                        except ValueError:
                            print("Ingrese un número válido.")
                else:
                    print("No se encontraron productos en este restaurante.")
                continue  # Volver al menú principal de búsqueda
            elif opcion_productos == "5":
                break
            else:
                print("Opción inválida.")
                continue

            valor_busqueda = input("Ingrese el valor a buscar: ")
            productos_filtrados = buscar_productos(restaurante["products"], tipo_busqueda, valor_busqueda)

            if productos_filtrados:
                print("Productos encontrados:")
                for i, producto in enumerate(productos_filtrados):
                    print(f"{i+1}. {producto['name']} - {producto['adicional']} - ${producto['price']}")

                # Seleccionar producto
                while True:
                    try:
                        opcion_producto = int(input("Seleccione el número del producto (o ingrese 0 para volver): "))
                        if opcion_producto == 0:
                            break
                        elif 1 <= opcion_producto <= len(productos_filtrados):
                            producto_seleccionado = productos_filtrados[opcion_producto - 1]
                            
                            # Validar edad para bebidas alcohólicas
                            if producto_seleccionado["adicional"] == "alcoholic" and cliente.edad < 18:
                                print("Lo siento, no puedes comprar bebidas alcohólicas.")
                            else:
                                productos_seleccionados.append(producto_seleccionado)
                                print(f"Producto {producto_seleccionado['name']} agregado al carrito.")
                            break
                        else:
                            print("Opción inválida.")
                    except ValueError:
                        print("Ingrese un número válido.")

            else:
                print("No se encontraron productos que coincidan con la búsqueda.")

        if productos_seleccionados:
            # Mostrar el resumen de la compra
            subtotal = 0
            for producto in productos_seleccionados:
                subtotal += float(producto["price"])
            
            descuento = calcular_descuento_orden(subtotal, cliente.cedula)

            total = subtotal * (1 - descuento)
            print(f"\nResumen de la compra:")
            for i, producto in enumerate(productos_seleccionados):
                print(f"{i+1}. {producto['name']} - ${float(producto['price']):.2f}")

            print(f"Subtotal: ${subtotal:.2f}")
            print(f"Descuento: ${subtotal * descuento:.2f}")
            print(f"Total: ${total:.2f}")

            # Confirmar la compra
            confirmar_compra = input("¿Desea proceder con la compra? (s/n): ").lower()
            if confirmar_compra == "s":
                print("¡Pago exitoso!")
                for producto in productos_seleccionados:  # Recorre los productos comprados
                    estadio_nombre = estadio_nombre_restaurante  # Obtén el nombre del estadio
                    restaurante_nombre = restaurante["name"]  # Obtén el nombre del restaurante
                    nombre_producto = producto["name"]  # Obtén el nombre del producto
                    nuevo_stock = obtener_stock_producto(estadio_nombre, restaurante_nombre, nombre_producto) 
                    if nuevo_stock is not None:
                        nuevo_stock -= 1  # Resta 1 solo si el stock no es None
                        actualizar_stock_producto(estadio_nombre, restaurante_nombre, nombre_producto, nuevo_stock)  # Actualiza el stock en la base de datos
                        actualizar_stock_producto_en_memoria(estadio_nombre, restaurante_nombre, nombre_producto, nuevo_stock)
                    else:
                        print(f"No se encontró el producto {nombre_producto} en este restaurante.")
            else:
                print("Compra cancelada.")
        else:
            print("No ha seleccionado ningún producto.")

# Función para calcular el descuento en las ventas
def calcular_descuento_orden(subtotal, cedula):
    if es_numero_perfecto(cedula):
        return 0.15
    return 0

# Función para gestionar los productos en el módulo de restaurantes
def gestionar_restaurantes_vendedores():
    estadio_nombre = input("Ingrese el nombre del estadio donde se encuentra el restaurante a administrar: ")

    restaurantes = obtener_restaurantes_estadio(estadio_nombre)
    mostrar_restaurantes(restaurantes)

    if not restaurantes:
        return

    opcion_restaurante = int(input("Seleccione el número del restaurante que administrará: "))
    if 1 <= opcion_restaurante <= len(restaurantes):
        restaurante = restaurantes[opcion_restaurante - 1]

        while True:
            print("\n¿Cómo desea buscar los productos?")
            print("1. Por nombre")
            print("2. Por tipo")
            print("3. Por precio")
            print("4. Ver todos los productos")
            print("5. Volver")
            opcion_productos = input("Seleccione la opción que desea: ")

            if opcion_productos == "1":
                tipo_busqueda = "name"
            elif opcion_productos == "2":
                tipo_busqueda = "additional"
            elif opcion_productos == "3":
                tipo_busqueda = "price"
            elif opcion_productos == "4":
                # Mostrar todos los productos
                productos_filtrados = mostrar_productos_restaurante(restaurante)
                if productos_filtrados:
                    # Seleccionar producto
                    while True:
                        try:
                            opcion_producto = int(input("Seleccione el número del producto (o ingrese 0 para volver): "))
                            if opcion_producto == 0:
                                break
                            elif 1 <= opcion_producto <= len(productos_filtrados):
                                producto_seleccionado = productos_filtrados[opcion_producto - 1]

                                # Mostrar precio con IVA
                                precio_con_iva = float(producto_seleccionado["price"]) * 1.16
                                print(f"El precio del producto {producto_seleccionado['name']} con IVA (16%) es: ${precio_con_iva:.2f}")
                                continue
                            else:
                                print("Opción inválida.")
                        except ValueError:
                            print("Ingrese un número válido.")
                else:
                    print("No se encontraron productos en este restaurante.")
                break
            elif opcion_productos == "5":
                break
            else:
                print("Opción inválida.")
                continue

            valor_busqueda = input("Ingrese el valor a buscar: ")
            productos_filtrados = buscar_productos(restaurante["products"], tipo_busqueda, valor_busqueda)

            if productos_filtrados:
                print("Productos encontrados:")
                for i, producto in enumerate(productos_filtrados):
                    print(f"{i+1}. {producto['name']} - {producto['adicional']} - ${producto['price']}")

                # Seleccionar producto
                while True:
                    try:
                        opcion_producto = int(input("Seleccione el número del producto: "))
                        if 1 <= opcion_producto <= len(productos_filtrados):
                            producto_seleccionado = productos_filtrados[opcion_producto - 1]
                            break
                        else:
                            print("Opción inválida.")
                    except ValueError:
                        print("Ingrese un número válido.")

                # Mostrar precio con IVA
                precio_con_iva = float(producto_seleccionado["price"]) * 1.16
                print(f"El precio del producto {producto_seleccionado['name']} con IVA (16%) es: ${precio_con_iva:.2f}")

            else:
                print("No se encontraron productos que coincidan con la búsqueda.")

# Función para imprimir el gráfico de los estadios
def print_stadiums_from_api():
    response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
    stadiums_data = response.json()

    for stadium_data in stadiums_data:
        # Calcular el número de columnas del estadio
        columns_stadium = (stadium_data['capacity'][0] + stadium_data['capacity'][1]) // 10
        stadium = Stadium(10, columns_stadium)

        # Carga la información de los asientos ocupados si existe
        stadium.load_occupied_seats()

        # Imprimir el estadio con secciones de 30 columnas
        print(f"Estadio: {stadium_data['name']}")
        print(f"Ciudad: {stadium_data['city']}")
        # Utiliza el método print_stadium() para imprimir el estadio
        stadium.print_stadium() 
        print()

        # Guarda la información de los asientos ocupados después de imprimir
        stadium.save_occupied_seats()

# Función para mostrar la información de los partidos que busque el usuario
def mostrar_informacion_partidos(partidos_filtrados):
    if partidos_filtrados:
        for i, partido in enumerate(partidos_filtrados):
            estadio_nombre = obtener_nombre_estadio_por_id(partido.estadio)
            print(f"{i+1}. Partido: {partido.equipo_local} vs {partido.equipo_visitante}, {partido.fecha_hora}, {estadio_nombre}") #fecha_formateada
    else:
        print("No se encontraron partidos para la búsqueda.")

# Función para crear la base de datos
def crear_base_de_datos():
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nombre TEXT,
            cliente_cedula INTEGER,
            cliente_edad INTEGER,
            partido_equipo_local TEXT,
            partido_equipo_visitante TEXT,
            partido_fecha TEXT,
            partido_estadio TEXT,
            tipo TEXT,
            asiento_fila INTEGER,
            asiento_numero INTEGER,
            costo REAL,
            codigo_unico INTEGER  
        )
    """)
    conn.commit()

    cursor.execute("PRAGMA table_info(entradas)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    if "usado" not in column_names:
        cursor.execute("ALTER TABLE entradas ADD COLUMN usado INTEGER DEFAULT 0")
        conn.commit()

    conn.close()

# Función para guardar una entrada en la base de datos
def guardar_entrada(entrada, asiento):
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entradas (
            cliente_nombre, 
            cliente_cedula, 
            cliente_edad, 
            partido_equipo_local, 
            partido_equipo_visitante, 
            partido_fecha, 
            partido_estadio, 
            tipo, 
            asiento_fila, 
            asiento_numero, 
            costo, 
            codigo_unico, 
            usado 
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entrada.cliente.nombre,
        entrada.cliente.cedula,
        entrada.cliente.edad,
        entrada.partido.equipo_local,
        entrada.partido.equipo_visitante,
        entrada.partido.fecha_hora,
        entrada.partido.estadio,
        entrada.tipo,
        asiento.fila, 
        asiento.numero, 
        entrada.costo,
        entrada.codigo_unico,
        0 
    ))
    conn.commit()
    conn.close()

# Función para mostrar las entradas de un cliente
def mostrar_entradas_cliente(cedula):
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM entradas WHERE cliente_cedula = ?
    """, (cedula,))
    entradas = cursor.fetchall()
    conn.close()

    if entradas:
        print("\nTus entradas compradas:")
        for entrada in entradas:
            print(f"Partido: {entrada[4]} vs {entrada[5]}, {entrada[6]}, {entrada[7]}")
            print(f"Tipo: {entrada[8]}, Asiento: Fila {entrada[9]}, Número {entrada[10]}")
            print(f"Costo: {entrada[11]:.2f}")
            print("-" * 20)
    else:
        print("\nNo se encontraron entradas compradas para esta cédula.")

def buscar_entrada_vip_por_cedula(cedula):
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM entradas WHERE cliente_cedula = ? AND tipo = 'VIP'
    """, (cedula,))
    entrada = cursor.fetchone()
    conn.close()

    return entrada

def buscar_estadio_por_codigo(estadio_id):
    # Busca un estadio por su código (id) en la API.
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    for estadio_json in estadios_json:
        if estadio_json["id"] == estadio_id:
            return estadio_json["name"]
    return None

def obtener_restaurantes_y_productos_api():
    # Obtiene la información de los restaurantes y sus productos de la API.
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    restaurantes_productos = []
    for estadio in estadios_json:
        for restaurante in estadio["restaurants"]:
            for producto in restaurante["products"]:
                restaurantes_productos.append({
                    "estadio": estadio["name"],
                    "restaurante": restaurante["name"],
                    "producto": producto["name"],
                    "stock": producto["stock"]
                })
    return restaurantes_productos

# Función para guardar la información de los productos en la base de datos
def guardar_productos_en_base_de_datos(restaurantes_productos):
    """
    Guarda la información de los productos en la base de datos.
    """
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estadio TEXT,
            restaurante TEXT,
            nombre TEXT,
            stock INTEGER
        )
    """)
    conn.commit()

    # Eliminar productos existentes en la tabla
    cursor.execute("DELETE FROM productos")
    conn.commit()

    # Insertar los productos
    for producto in restaurantes_productos:
        cursor.execute("""
            INSERT INTO productos (estadio, restaurante, nombre, stock)
            VALUES (?, ?, ?, ?)
        """, (producto["estadio"], producto["restaurante"], producto["producto"], producto["stock"]))
    conn.commit()
    conn.close()

# Función para actualizar el stock de un producto en la base de datos
def actualizar_stock_producto(estadio, restaurante, nombre, nuevo_stock):
    # Actualiza el stock de un producto en la base de datos.

    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos SET stock = ?
        WHERE estadio = ? AND restaurante = ? AND nombre = ?
    """, (nuevo_stock, estadio, restaurante, nombre))
    conn.commit()
    conn.close()

def obtener_stock_producto(estadio, restaurante, nombre):
    # Obtiene el stock actual de un producto de la base de datos.
    
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT stock FROM productos
            WHERE estadio = ? AND restaurante = ? AND nombre = ?
        """, (estadio, restaurante, nombre))
        stock = cursor.fetchone()
        conn.close()

        if stock:
            return stock[0]
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener el stock: {e}")
        conn.close()
        return None

def actualizar_stock_producto_en_memoria(estadio, restaurante, nombre, nuevo_stock):
    # Actualiza el stock de un producto en la lista productos.
    
    for producto in productos:
        if producto.estadio == estadio and producto.restaurante == restaurante and producto.nombre == nombre:
            producto.stock = nuevo_stock
            break

def generar_codigo_unico():
    while True:
        codigo = random.randint(100000, 999999)
        # Verificar si el código ya existe en la base de datos
        if not codigo_existe_en_base_de_datos(codigo):
            return codigo

def codigo_existe_en_base_de_datos(codigo):
    conn = sqlite3.connect("entradas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM entradas WHERE codigo_unico = ?", (codigo,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def modulo_seguridad():
    while True:
        print("\nMódulo de protocolo/seguridad del estadio:")
        print("1. Validar código de boleto")
        print("2. Volver al menú principal")
        opcion_seguridad = input("Seleccione una opción: ")

        if opcion_seguridad == "1":
            codigo_ingresado = int(input("Ingrese el código del boleto: "))
            
            # Validar el código
            if codigo_existe_en_base_de_datos(codigo_ingresado):
                # Verificar si el código ya fue usado
                conn = sqlite3.connect("entradas.db")
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM entradas WHERE codigo_unico = ? AND usado = 1", (codigo_ingresado,))
                codigo_usado = cursor.fetchone() is not None
                conn.close()

                if codigo_usado:
                    print("El código de boleto ya fue utilizado.")
                else:
                    print("El código de boleto es válido.")
                    # Marcar el código como usado
                    conn = sqlite3.connect("entradas.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE entradas SET usado = 1 WHERE codigo_unico = ?", (codigo_ingresado,))
                    conn.commit()
                    conn.close()
            else:
                print("El código de boleto no es válido.")

        elif opcion_seguridad == "2":
            break

        else:
            print("Opción inválida.")

# Inicialización de variables globales
equipos = []
estadios = []
partidos = []
clientes = []
entradas = []
asientos = []
productos = []
ordenes_restaurante = []

try:
    cargar_equipos_desde_archivo("equipos.json")
except FileNotFoundError:
    print("No se encontró el archivo equipos.json. Se cargarán los equipos desde la API.")
    equipos = cargar_equipos()
    guardar_equipos()
try:
    cargar_estadios_desde_archivo("estadios.json")
except FileNotFoundError:
    print("No se encontró el archivo estadios.json. Se cargarán los estadios desde la API.")
    estadios = cargar_estadios()
    guardar_estadios()
try:
    cargar_partidos_desde_archivo("partidos.json")
except FileNotFoundError:
    print("No se encontró el archivo partidos.json. Se cargarán los partidos desde la API.")
    partidos = cargar_partidos()
    guardar_partidos()
try:
    cargar_clientes_desde_archivo("clientes.json")
except FileNotFoundError:
    print("No se encontró el archivo clientes.json.")
try:
    cargar_entradas_desde_archivo("entradas.json")
except FileNotFoundError:
    print("No se encontró el archivo entradas.json.")
try:
    cargar_asientos_desde_archivo("asientos.json")
except FileNotFoundError:
    print("No se encontró el archivo asientos.json.")
try:
    cargar_productos_desde_archivo("productos.json")
except FileNotFoundError:
    print("No se encontró el archivo productos.json.")
try:
    cargar_ordenes_restaurante_desde_archivo("ordenes_restaurante.json")
except FileNotFoundError:
    print("No se encontró el archivo ordenes_restaurante.json.")

# Menú principal
while True:
    crear_base_de_datos()
    restaurantes_productos = obtener_restaurantes_y_productos_api()
    guardar_productos_en_base_de_datos(restaurantes_productos)
    print("¡Bienvenido al sistema gestión para la Eurocopa Alemania 2024!")
    print("\nMenú principal:")
    print("1. Módulo para aficionados (compra de entradas y servicios en el estadio).")
    print("2. Módulo para protocolo/seguridad del estadio.")
    print("3. Módulo para restaurantes.")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\nIngresaste al módulo para aficionados para la compra entradas/servicios para la Eurocopa Alemania 2024!")
        print("1. Comprar entrada")
        print("2. Comprar en restaurante (Válida para clientes con entrada VIP)")
        print("3. Volver al menú principal")
        opcion_modulo_aficionado = input("Seleccione una opción: ")

        if opcion_modulo_aficionado == "1":
            input("Para continuar requerimos algunos de sus datos personales [Presione ENTER para continuar]")

            # 1. Obtener datos del cliente
            nombre = input("Ingrese su nombre y apellido: ")
            cedula = int(input("Ingrese su cédula de identidad: "))
            edad = int(input("Ingrese su edad: "))
            cliente = crear_cliente(nombre, cedula, edad)

            # 2. Mostrar información de búsqueda de los partidos
            while True:
                print("\nPor favor, busque el partido al que desea asistir:")
                print("1. Buscar todos los partidos de un equipo")
                print("2. Buscar todos los partidos que se jugarán en un estadio específico")
                print("3. Buscar todos los partidos que se jugarán en una fecha determinada")
                print("4. Ver todos los partidos")
                print("5. Volver al menú principal")
                opcion_partido = input("Seleccione una opción: ")

                if opcion_partido == "1":
                    nombre_equipo = input("Ingrese el nombre del equipo: ")
                    partidos_filtrados = buscar_partido_por_equipo_api(nombre_equipo)
                    mostrar_informacion_partidos(partidos_filtrados)

                elif opcion_partido == "2":
                    estadio_nombre = input("Ingrese el nombre del estadio: ")
                    partidos_filtrados = buscar_partido_por_estadio_api(estadio_nombre)
                    mostrar_informacion_partidos(partidos_filtrados)

                elif opcion_partido == "3":
                    fecha_str = input("Ingrese la fecha del partido (AAAA-MM-DD): ")
                    fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
                    partidos_filtrados = buscar_partido_por_fecha_api(fecha)
                    mostrar_informacion_partidos(partidos_filtrados)

                elif opcion_partido == "4":
                    partidos_filtrados = []
                    for i, partido in enumerate(partidos):
                        fecha_formateada = partido.fecha_hora.strftime('%Y-%m-%d')
                        print(f"{i+1}. Partido: {partido.equipo_local['name']} vs {partido.equipo_visitante['name']}, {fecha_formateada}, {estadio_nombre}")
                        partidos_filtrados.append(partido)

                elif opcion_partido == "5":
                    break

                else:
                    print("Opción inválida.")

                # Después de mostrar los partidos, preguntamos si el usuario quiere seleccionar uno
                if partidos_filtrados:
                    seleccionar_partido = input("¿Desea seleccionar un partido de la lista? (s/n): ").lower()
                    if seleccionar_partido == "s":
                        opcion_partido = int(input("Seleccione el número del partido al que desea asistir: "))
                        if 1 <= opcion_partido <= len(partidos_filtrados):
                            partido = partidos_filtrados[opcion_partido - 1]
                            estadio_nombre = obtener_nombre_estadio_por_id(partido.estadio)
                            
                            response = requests.get('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json')
                            stadiums_data = response.json()

                            for stadium_data in stadiums_data:
                                if stadium_data['name'] == estadio_nombre:
                                    # Calcular el número de columnas del estadio
                                    columns_stadium = (stadium_data['capacity'][0] + stadium_data['capacity'][1]) // 10
                                    stadium = Stadium(10, columns_stadium)

                                    # Ocupar asientos aleatoriamente
                                    for _ in range(10):
                                        row = random.randint(0, 9)
                                        column = random.randint(0, columns_stadium - 1)
                                        stadium.occupy_seat(row, column)

                                    # Imprimir el estadio con secciones de 30 columnas
                                    print(f"Estadio: {stadium_data['name']}")
                                    print(f"Ciudad: {stadium_data['city']}")
                                    stadium.print_stadium()
                                    print()

                                    print("Entrada General: $35")
                                    print("Entrada VIP: $75")
                                    print("Los ususarios con entrada VIP podrá disfrutar y adquirir productos de los restaurantes del estadio.")
                                    eleccion_entradas = input("Desea adquirir una entrada General o una VIP?: ")
                                    # return  # Salir de la función después de imprimir el estadiok

                                    if eleccion_entradas == "General":
                                        tipo = "General"
                                        entrada = vender_entrada(cliente, partido, tipo)  # Llama a vender_entrada
                                        break

                                    elif eleccion_entradas == "VIP":
                                        tipo = "VIP"
                                        entrada = vender_entrada(cliente, partido, tipo)  # Llama a vender_entrada
                                        break

                                    else:
                                        print("Opción inválida. Vuelva a intentarlo.")
                                    break
                                
                                else:
                                    print("No se encontró el estadio.")
                            if entrada is not None:
                                print("¡Entrada vendida con éxito!")
                                break
                            else:
                                print("Compra cancelada.")
                                break
                        else:
                            print("Opción inválida.")
                            break
                    else:
                        continue
                else:
                    # Si no hay partidos, vuelve al menú de búsqueda de partidos
                    continue
        elif opcion_modulo_aficionado == "2":
            cedula = int(input("Ingrese su cédula de identidad: "))
            entrada = buscar_entrada_vip_por_cedula(cedula)
            cliente = buscar_cliente_por_cedula(cedula)
        
            if cliente:
                if entrada is not None:  # Check if entrada is not None
                    estadio_id = entrada[7]  # Obtener el código del estadio de la entrada
                    estadio_nombre = buscar_estadio_por_codigo(estadio_id)  # Obtener el nombre del estadio
                    print(f"Bienvenido al módulo de restaurantes del estadio {estadio_nombre}.")

                    restaurantes = obtener_restaurantes_estadio(estadio_nombre)
                    mostrar_restaurantes(restaurantes)

                    if restaurantes:
                        # Pasa el cliente como argumento a la función
                        gestionar_restaurantes_compra(cliente) 
                    else:
                        print("No se encontraron restaurantes en este estadio.")

                else:
                    if not cliente:
                        print("No se encontró un cliente asociado a esta cédula. Por favor, revise sus datos.")
                    elif not entrada:
                        print("Necesitas una entrada VIP para acceder a este módulo.")
                    continue
            
        elif opcion_modulo_aficionado == "3":
                continue
    
    elif opcion == "2":
        modulo_seguridad()
    
    elif opcion == "3":
        gestionar_restaurantes_vendedores()