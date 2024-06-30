import requests
import json
import datetime
import random
from collections import namedtuple
from functools import reduce
import matplotlib.pyplot as plt
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from itertools import permutations
import sqlite3

class Equipo:
    def __init__(self, nombre, codigo_fifa, grupo):
        self.nombre = nombre
        self.codigo_fifa = codigo_fifa
        self.grupo = grupo

class Estadio:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

class Partido:
    def __init__(self, equipo_local, equipo_visitante, fecha_hora, estadio):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha_hora = fecha_hora
        self.estadio = estadio
        self.asistencia = 0

class Asiento:
    def __init__(self, numero, fila, ocupado):
        self.numero = numero
        self.fila = fila
        self.ocupado = ocupado

class Cliente:
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

class Entrada:
    def __init__(self, cliente, partido, tipo, asiento, costo):
        self.cliente = cliente
        self.partido = partido
        self.tipo = tipo
        self.asiento = asiento
        self.costo = costo

class Producto:
    def __init__(self, nombre, tipo, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio

class OrdenRestaurante:
    def __init__(self, cliente, productos, costo):
        self.cliente = cliente
        self.productos = productos
        self.costo = costo

# Funciones auxiliares para validar números vampiro y números perfectos
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

def es_numero_perfecto(numero):
    if numero <= 1:
        return False
    divisores = [1]
    for i in range(2, numero):
        if numero % i == 0:
            divisores.append(i)
    suma_divisores = reduce(lambda x, y: x + y, divisores)
    return suma_divisores == numero

# Funciones para cargar datos desde la API
def cargar_equipos():
    equipos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
    equipos = []
    for equipo_json in equipos_json:
        nombre = equipo_json["name"]
        codigo_fifa = equipo_json["code"]
        grupo = equipo_json["group"]
        equipos.append(Equipo(nombre, codigo_fifa, grupo))
    return equipos

def cargar_estadios():
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    estadios = []
    for estadio_json in estadios_json:
        nombre = estadio_json["name"]
        ubicacion = estadio_json["city"]
        estadios.append(Estadio(nombre, ubicacion))
    return estadios

def cargar_partidos():
    partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
    partidos = []
    for partido_json in partidos_json:
        equipo_local_codigo_fifa = partido_json["home"]
        equipo_visitante_codigo_fifa = partido_json["away"]
        fecha_hora_str = partido_json["date"]
        # fecha_hora = datetime.datetime.strptime(fecha_hora_str, "%Y-%m-%dT%H:%M:%SZ")
        estadio_nombre = partido_json["stadium_id"]
        partidos.append(Partido(equipo_local_codigo_fifa, equipo_visitante_codigo_fifa, fecha_hora_str, estadio_nombre))
    return partidos

def buscar_equipo_por_codigo_fifa(codigo_fifa):
    for equipo in equipos:
        if equipo.codigo_fifa == codigo_fifa:
            return equipo
    return None

def buscar_estadio_por_nombre(nombre):
    for estadio in estadios:
        if estadio.nombre == nombre:
            return estadio
    return None

def buscar_partido_por_fecha(fecha):
    partidos_filtrados = []
    for partido in partidos:
        if partido.fecha_hora.date() == fecha:
            partidos_filtrados.append(partido)
    return partidos_filtrados

def buscar_partido_por_estadio(estadio):
    partidos_filtrados = []
    for partido in partidos:
        if partido.estadio == estadio:
            partidos_filtrados.append(partido)
    return partidos_filtrados

def buscar_partido_por_equipo(equipo):
    partidos_filtrados = []
    for partido in partidos:
        if partido.equipo_local == equipo or partido.equipo_visitante == equipo:
            partidos_filtrados.append(partido)
    return partidos_filtrados

# Funciones para gestionar las entradas
def crear_cliente(nombre, cedula, edad):
    cliente = Cliente(nombre, cedula, edad)
    clientes.append(cliente)
    guardar_clientes()
    return cliente

def buscar_cliente_por_cedula(cedula):
    for cliente in clientes:
        if cliente.cedula == cedula:
            return cliente
    return None

def crear_entrada(cliente, partido, tipo, asiento, costo):
    entrada = Entrada(cliente, partido, tipo, asiento, costo)
    entradas.append(entrada)
    guardar_entradas()
    return entrada

def calcular_costo_entrada(partido, tipo, cedula):
    costo = 0
    if tipo == "General":
        costo = 35
    elif tipo == "VIP":
        costo = 75
    # if es_numero_vampiro(cedula):
    #     costo *= 0.5
    # costo *= 1.16
    return costo

def actualizar_asiento(asiento):
    for i in range(len(asientos)):
        if asientos[i].numero == asiento.numero and asientos[i].fila == asiento.fila:
            asientos[i] = asiento
            break
    guardar_asientos()

# Funciones para gestionar los restaurantes
def crear_producto(nombre, tipo, precio):
    producto = Producto(nombre, tipo, precio)
    productos.append(producto)
    guardar_productos()
    return producto

def buscar_producto_por_nombre(nombre):
    for producto in productos:
        if producto.nombre == nombre:
            return producto
    return None

def buscar_productos_por_tipo(tipo):
    productos_filtrados = []
    for producto in productos:
        if producto.tipo == tipo:
            productos_filtrados.append(producto)
    return productos_filtrados

def buscar_productos_por_precio(precio_min, precio_max):
    productos_filtrados = []
    for producto in productos:
        if producto.precio >= precio_min and producto.precio <= precio_max:
            productos_filtrados.append(producto)
    return productos_filtrados

def crear_orden_restaurante(cliente, productos):
    costo_total = 0
    for producto in productos:
        costo_total += producto.precio
    orden = OrdenRestaurante(cliente, productos, costo_total)
    ordenes_restaurante.append(orden)
    guardar_ordenes_restaurante()
    return orden

def calcular_descuento_orden(orden):
    if es_numero_perfecto(orden.cliente.cedula):
        return 0.15
    return 0

def realizar_venta_restaurante(cliente, productos):
    orden = crear_orden_restaurante(cliente, productos)
    descuento = calcular_descuento_orden(orden)
    costo_total = orden.costo * (1 - descuento)
    print(f"Su orden tiene un descuento de {descuento * 100}%.")
    print(f"El costo total de su orden es: {costo_total}")
    for producto in productos:
        restar_inventario(producto)

# Funciones para gestionar el inventario
def restar_inventario(producto):
    for i in range(len(productos)):
        if productos[i].nombre == producto.nombre:
            productos[i].precio -= 1
            break
    guardar_productos()

# Funciones para cargar y guardar datos en archivos
def cargar_equipos_desde_archivo(archivo):
    global equipos
    equipos = []
    with open(archivo, "r") as f:
        equipos_json = json.load(f)
        for equipo_json in equipos_json:
            equipos.append(Equipo(equipo_json["nombre"], equipo_json["codigo_fifa"], equipo_json["grupo"]))

def guardar_equipos():
    equipos_json = []
    for equipo in equipos:
        equipos_json.append({"nombre": equipo.nombre, "codigo_fifa": equipo.codigo_fifa, "grupo": equipo.grupo})
    with open("equipos.json", "w") as f:
        json.dump(equipos_json, f)

def cargar_estadios_desde_archivo(archivo):
    global estadios
    estadios = []
    with open(archivo, "r", encoding='utf-8') as f:  
        estadios_json = json.load(f)
        for estadio_json in estadios_json:
            estadios.append(Estadio(estadio_json["name"], estadio_json["city"]))

def guardar_estadios():
    estadios_json = []
    for estadio in estadios:
        estadios_json.append({"nombre": estadio.nombre, "ubicacion": estadio.ubicacion})
    with open("estadios.json", "w") as f:
        json.dump(estadios_json, f)

def cargar_partidos_desde_archivo(archivo):
    global partidos
    partidos = []
    with open(archivo, "r") as f:
        partidos_json = json.load(f)
        for partido_json in partidos_json:
            fecha_hora = datetime.datetime.strptime(partido_json["date"], "%Y-%m-%d")
            partidos.append(Partido(partido_json["home"], partido_json["away"], fecha_hora, partido_json["stadium_id"]))

def guardar_partidos():
    partidos_json = []
    for partido in partidos:
        partidos_json.append({"equipo_local": partido.equipo_local, "equipo_visitante": partido.equipo_visitante, "fecha_hora": partido.fecha_hora.isoformat(), "estadio": partido.estadio})
    with open("partidos.json", "w") as f:
        json.dump(partidos_json, f)

def cargar_clientes_desde_archivo(archivo):
    global clientes
    clientes = []
    with open(archivo, "r") as f:
        clientes_json = json.load(f)
        for cliente_json in clientes_json:
            clientes.append(Cliente(cliente_json["nombre"], cliente_json["cedula"], cliente_json["edad"]))

def guardar_clientes():
    clientes_json = []
    for cliente in clientes:
        clientes_json.append({"nombre": cliente.nombre, "cedula": cliente.cedula, "edad": cliente.edad})
    with open("clientes.json", "w") as f:
        json.dump(clientes_json, f)

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

def guardar_entradas():
    entradas_json = []
    for entrada in entradas:
        entradas_json.append({"cliente_cedula": entrada.cliente.cedula, "partido_fecha_hora": entrada.partido.fecha_hora.isoformat(), "tipo": entrada.tipo, "asiento_numero": entrada.asiento.numero, "asiento_fila": entrada.asiento.fila, "costo": entrada.costo})
    with open("entradas.json", "w") as f:
        json.dump(entradas_json, f)

def cargar_asientos_desde_archivo(archivo):
    global asientos
    asientos = []
    with open(archivo, "r") as f:
        asientos_json = json.load(f)
        for asiento_json in asientos_json:
            asientos.append(Asiento(asiento_json["numero"], asiento_json["fila"], asiento_json["ocupado"]))

def guardar_asientos():
    asientos_json = []
    for asiento in asientos:
        asientos_json.append({"numero": asiento.numero, "fila": asiento.fila, "ocupado": asiento.ocupado})
    with open("asientos.json", "w") as f:
        json.dump(asientos_json, f)

def cargar_productos_desde_archivo(archivo):
    global productos
    productos = []
    with open(archivo, "r") as f:
        productos_json = json.load(f)
        for producto_json in productos_json:
            productos.append(Producto(producto_json["nombre"], producto_json["tipo"], producto_json["precio"]))

def guardar_productos():
    productos_json = []
    for producto in productos:
        productos_json.append({"nombre": producto.nombre, "tipo": producto.tipo, "precio": producto.precio})
    with open("productos.json", "w") as f:
        json.dump(productos_json, f)

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

def guardar_ordenes_restaurante():
    ordenes_restaurante_json = []
    for orden_restaurante in ordenes_restaurante:
        productos_json = []
        for producto in orden_restaurante.productos:
            productos_json.append({"nombre": producto.nombre})
        ordenes_restaurante_json.append({"cliente_cedula": orden_restaurante.cliente.cedula, "productos": productos_json, "costo": orden_restaurante.costo})
    with open("ordenes_restaurante.json", "w") as f:
        json.dump(ordenes_restaurante_json, f)

# Funciones para realizar estadísticas
def calcular_promedio_gasto_vip():
    gastos_vip = []
    for entrada in entradas:
        if entrada.tipo == "VIP":
            gastos_vip.append(entrada.costo)
    promedio = sum(gastos_vip) / len(gastos_vip)
    return promedio

def obtener_estadísticas_partidos():
    partidos_ordenados = sorted(partidos, key=lambda partido: partido.asistencia, reverse=True)
    estadísticas_partidos = []
    for partido in partidos_ordenados:
        equipo_local = buscar_equipo_por_codigo_fifa(partido.equipo_local)
        equipo_visitante = buscar_equipo_por_codigo_fifa(partido.equipo_visitante)
        estadísticas_partidos.append({"partido": f"{equipo_local.nombre} vs {equipo_visitante.nombre}", "estadio": partido.estadio, "boletos_vendidos": partido.asistencia, "asistencia": partido.asistencia})
    return estadísticas_partidos

def obtener_partido_con_mayor_asistencia():
    partido_mayor_asistencia = max(partidos, key=lambda partido: partido.asistencia)
    return partido_mayor_asistencia

def obtener_partido_con_mayor_boletos_vendidos():
    partido_mayor_boletos_vendidos = max(partidos, key=lambda partido: partido.asistencia)
    return partido_mayor_boletos_vendidos

def obtener_productos_mas_vendidos():
    productos_vendidos = {}
    for orden in ordenes_restaurante:
        for producto in orden.productos:
            if producto.nombre in productos_vendidos:
                productos_vendidos[producto.nombre] += 1
            else:
                productos_vendidos[producto.nombre] = 1
    productos_mas_vendidos = sorted(productos_vendidos.items(), key=lambda item: item[1], reverse=True)
    return productos_mas_vendidos[:3]

def obtener_clientes_con_mas_boletos():
    clientes_boletos = {}
    for entrada in entradas:
        if entrada.cliente.cedula in clientes_boletos:
            clientes_boletos[entrada.cliente.cedula] += 1
        else:
            clientes_boletos[entrada.cliente.cedula] = 1
    clientes_mas_boletos = sorted(clientes_boletos.items(), key=lambda item: item[1], reverse=True)
    return clientes_mas_boletos[:3]

def generar_graficos(estadísticas_partidos, productos_mas_vendidos, clientes_mas_boletos):
    # Gráfico de partidos ordenados por asistencia
    partidos = [estadistica["partido"] for estadistica in estadísticas_partidos]
    asistencias = [estadistica["asistencia"] for estadistica in estadísticas_partidos]
    plt.figure(figsize=(10, 5))
    plt.bar(partidos, asistencias)
    plt.title("Partidos ordenados por asistencia")
    plt.xlabel("Partido")
    plt.ylabel("Asistencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Gráfico de productos más vendidos
    productos = [producto[0] for producto in productos_mas_vendidos]
    cantidades = [producto[1] for producto in productos_mas_vendidos]
    plt.figure(figsize=(10, 5))
    plt.pie(cantidades, labels=productos, autopct="%1.1f%%")
    plt.title("Productos más vendidos")
    plt.show()

    # Gráfico de clientes con más boletos
    clientes = [cliente[0] for cliente in clientes_mas_boletos]
    cantidades = [cliente[1] for cliente in clientes_mas_boletos]
    plt.figure(figsize=(10, 5))
    plt.bar(clientes, cantidades)
    plt.title("Clientes con más boletos")
    plt.xlabel("Cliente")
    plt.ylabel("Cantidad de boletos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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

def obtener_nombre_equipo_por_codigo_fifa(codigo_fifa):
    equipos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json").json()
    for equipo_json in equipos_json:
        if equipo_json["code"] == codigo_fifa:
            return equipo_json["name"]
    return None

def buscar_partido_por_estadio(estadio_nombre):
    partidos_filtrados = []
    for partido in partidos:
        estadio = buscar_estadio_por_nombre(partido.estadio)
        if estadio is not None and estadio.nombre == estadio_nombre:
            partidos_filtrados.append(partido)
    return partidos_filtrados

def obtener_nombre_estadio_por_id(estadio_id):
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    for estadio_json in estadios_json:
        if estadio_json["id"] == estadio_id:
            return estadio_json["name"]
    return None
#------------------------------------
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

        # Mostrar el costo al cliente
        subtotal = costo
        # iva = (16 * costo)
        descuento = 0
        if es_numero_vampiro(cliente.cedula):
            descuento = 0.5
            # costo *= 0.5
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
            print("¡Disfrute del partido!")
            asiento = Asiento(columna_real, fila, True)
            entrada = Entrada(cliente, partido, tipo, asiento, costo) 
            guardar_entrada(entrada, asiento)
        else:
            print("Compra cancelada.")
            # Liberar el asiento
            stadium.seats[fila - 1][columna_real].vacate()
    else:
        print("Asiento inválido o ocupado. Por favor, seleccione otro asiento.")

    return entrada

#-------------------------------
def obtener_restaurantes_estadio(estadio_nombre):
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()

    for estadio in estadios_json:
        if estadio["name"] == estadio_nombre:
            return estadio["restaurants"]

    return []

def mostrar_restaurantes(restaurantes):
    if not restaurantes:
        print("No se encontraron restaurantes en este estadio.")
        return

    print("Restaurantes disponibles:")
    for i, restaurante in enumerate(restaurantes):
        print(f"{i+1}. {restaurante['name']}")

def mostrar_productos_restaurante(restaurante):
    productos = restaurante["products"]

    if not productos:
        print("No se encontraron productos en este restaurante.")
        return

    print("Todos los productos disponibles en este establecimiento:")
    for i, producto in enumerate(productos):
        print(f"{i+1}. {producto['name']} - {producto['adicional']} - ${producto['price']}")

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
#--------------------------------
class Seat:
    def __init__(self, row, column, seat_type):
        self.row = row
        self.column = column
        self.occupied = False
        self.seat_type = seat_type

    def occupy(self):
        self.occupied = True

    def vacate(self):
        self.occupied = False

class Stadium:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.seats = [[Seat(row, column, "regular") for column in range(columns)] for row in range(rows)]

    def print_stadium(self):
        # Calcular cuántas secciones se necesitan
        num_sections = (self.columns + 29) // 30

        # Imprimir cada sección
        for section in range(num_sections):
            start_column = section * 30
            end_column = min(start_column + 30, self.columns)

            # Imprimir encabezado de la sección
            print(f"\nSección {chr(ord('A') + section)}")
            print("   ", end="")
            # Imprimir numeración de columnas comenzando en 1 para cada sección
            for column in range(start_column, end_column):
                # La numeración comienza en 1 y se ajusta al índice de la columna
                print(f"{column - start_column + 1:2d} ", end=" ") 
            print()

            # Imprimir asientos
            for row in range(self.rows):
                print(f"{row + 1:2d} ", end="")
                for column in range(start_column, end_column):
                    seat = self.seats[row][column]
                    if seat.occupied:
                        print("[X]", end=" ")
                    else:
                        print("[ ]", end=" ")
                print()
    
    def occupy_seat(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.seats[row][column].occupy()
            return True
        else:
            return False

    def save_occupied_seats(self):
        # Guarda la información de los asientos ocupados en un archivo
        with open("occupied_seats.json", "w") as f:
            occupied_seats = []
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.seats[row][column].occupied:
                        occupied_seats.append({"row": row, "column": column})
            json.dump(occupied_seats, f)

    def load_occupied_seats(self):
        # Carga la información de los asientos ocupados desde un archivo
        try:
            with open("occupied_seats.json", "r") as f:
                occupied_seats_data = json.load(f)
                for seat_data in occupied_seats_data:
                    self.seats[seat_data["row"]][seat_data["column"]].occupy()
        except FileNotFoundError:
            pass

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

#------------------------
def mostrar_informacion_partidos(partidos_filtrados):
    if partidos_filtrados:
        for i, partido in enumerate(partidos_filtrados):
            # fecha_formateada = partido.fecha_hora.strftime('%Y-%m-%d')
            estadio_nombre = obtener_nombre_estadio_por_id(partido.estadio)
            print(f"{i+1}. Partido: {partido.equipo_local} vs {partido.equipo_visitante}, {partido.fecha_hora}, {estadio_nombre}") #fecha_formateada
    else:
        print("No se encontraron partidos para la búsqueda.")
#--------------
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
            costo REAL
        )
    """)
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
            costo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entrada.cliente.nombre,
        entrada.cliente.cedula,
        entrada.cliente.edad,
        entrada.partido.equipo_local,
        entrada.partido.equipo_visitante,
        entrada.partido.fecha_hora.strftime("%Y-%m-%d"),
        entrada.partido.estadio,
        entrada.tipo,
        asiento.fila,  # Usa el atributo fila del asiento
        asiento.numero,  # Usa el atributo numero del asiento
        entrada.costo
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
        print("2. Comprar en restaurante")
        print("3. Volver al menú principal")
        opcion_modulo_aficionado = input("Seleccione una opción: ")

        if opcion_modulo_aficionado == "1":
            input("Para continuar requerimos algunos de sus datos personales [Presione ENTER para continuar]")

            # 1. Obtener datos del cliente
            nombre = input("Ingrese su nombre y apellido: ")
            cedula = int(input("Ingrese su cédula de identidad: "))
            edad = int(input("Ingrese su edad: "))
            cliente = crear_cliente(nombre, cedula, edad)

            # 2. Mostrar información de los partidos
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
        elif opcion_modulo_aficionado == "3":
            continue
    elif opcion == "2":
        # Mostrar entradas compradas
        cedula = int(input("Ingrese su cédula: "))
        mostrar_entradas_cliente(cedula)

    # # 5. Calcular costo de la entrada
    # costo = calcular_costo_entrada(partido, tipo, cliente.cedula)

    # # 6. Mostrar costo de la entrada al cliente
    # subtotal = costo / 1.16
    # descuento = 0
    # if es_numero_vampiro(cedula):
    #     descuento = 0.5
    #     costo *= 0.5
    #     print("¡Felicidades! Su cédula es un número vampiro, por lo que tiene un 50% de descuento.")

    # iva = costo * 0.16
    # print(f"Subtotal: ${subtotal:.2f}")
    # print(f"Descuento: ${subtotal * descuento:.2f}")
    # print(f"IVA (16%): ${iva:.2f}")
    # print(f"Total: ${costo:.2f}")

    # # 7. Confirmar pago
    # pagar = input("¿Desea proceder a pagar la entrada? (s/n): ").lower()
    # if pagar == "s":
    #     # Vender la entrada y actualizar la asistencia
    #     entrada = vender_entrada(cliente, partido, tipo)
    #     if entrada is not None:
    #         print("Pago exitoso.")
    #     else:
    #         print("Compra cancelada.")

    # else:
    #     print("Compra cancelada.")



    # if opcion == "2":
    #     # gestionar_venta_entradas()
    #     print_stadiums_from_api()

    # elif opcion == "3":
    #     # Gestión de restaurantes
    #     gestionar_restaurantes()

    # elif opcion == "6":
    #     # Indicadores de gestión
    #     while True:
    #         print("\nIndicadores de gestión:")
    #         print("1. Promedio de gasto de clientes VIP en un partido")
    #         print("2. Estadísticas de partidos")
    #         print("3. Productos más vendidos")
    #         print("4. Clientes con más boletos")
    #         print("5. Generar gráficos")
    #         print("6. Volver al menú principal")
    #         opcion_indicadores = input("Seleccione una opción: ")

    #         if opcion_indicadores == "1":
    #             print(f"Promedio de gasto de clientes VIP en un partido: {calcular_promedio_gasto_vip()}")

    #         elif opcion_indicadores == "2":
    #             estadisticas_partidos = obtener_estadisticas_partidos()
    #             for estadistica in estadisticas_partidos:
    #                 print(estadistica)

    #         elif opcion_indicadores == "3":
    #             productos_mas_vendidos = obtener_productos_mas_vendidos()
    #             for i, producto in enumerate(productos_mas_vendidos):
    #                 print(f"{i+1}. {producto[0]}: {producto[1]} unidades")

    #         elif opcion_indicadores == "4":
    #             clientes_mas_boletos = obtener_clientes_con_mas_boletos()
    #             for i, cliente in enumerate(clientes_mas_boletos):
    #                 print(f"{i+1}. {cliente[0]}: {cliente[1]} boletos")

    #         elif opcion_indicadores == "5":
    #             estadisticas_partidos = obtener_estadisticas_partidos()
    #             productos_mas_vendidos = obtener_productos_mas_vendidos()
    #             clientes_mas_boletos = obtener_clientes_con_mas_boletos()
    #             generar_graficos(estadisticas_partidos, productos_mas_vendidos, clientes_mas_boletos)

    #         elif opcion_indicadores == "6":
    #             break

    #         else:
    #             print("Opción inválida.")

    # elif opcion == "7":
    #     # Salir
    #     print("¡Hasta luego!")
    #     break

    # else:
    #     print("Opción inválida.")