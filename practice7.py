import requests
import json
import datetime
from collections import namedtuple
from functools import reduce
import matplotlib.pyplot as plt

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

# Obtener datos del API
def obtener_datos_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos del API: {response.status_code}")
        return None

# Cargar datos de equipos
def cargar_equipos():
    equipos_json = obtener_datos_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json")
    equipos = []
    for equipo in equipos_json:
        equipos.append(Equipo(equipo["nombre"], equipo["codigo_fifa"], equipo["grupo"]))
    return equipos

# Cargar datos de estadios
def cargar_estadios():
    estadios_json = obtener_datos_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
    estadios = []
    for estadio in estadios_json:
        estadios.append(Estadio(estadio["nombre"], estadio["ubicacion"]))
    return estadios

# Cargar datos de partidos
def cargar_partidos(equipos, estadios):
    partidos_json = obtener_datos_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json")
    partidos = []
    for partido in partidos_json:
        equipo_local = next((equipo for equipo in equipos if equipo.codigo_fifa == partido["equipo_local"]), None)
        equipo_visitante = next((equipo for equipo in equipos if equipo.codigo_fifa == partido["equipo_visitante"]), None)
        estadio = next((estadio for estadio in estadios if estadio.nombre == partido["estadio"]), None)
        fecha_hora = datetime.datetime.strptime(partido["fecha_hora"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        partidos.append(Partido(equipo_local, equipo_visitante, fecha_hora, estadio))
    return partidos

# Gestion de partidos y estadios
def gestion_partidos_y_estadios(equipos, estadios, partidos):
    while True:
        print("\nGestion de Partidos y Estadios")
        print("1. Buscar partidos")
        print("2. Ver información de un partido")
        print("3. Ver información de un estadio")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Buscar partidos
            while True:
                print("\nOpciones de búsqueda:")
                print("1. Buscar partidos por país")
                print("2. Buscar partidos por estadio")
                print("3. Buscar partidos por fecha")
                print("4. Volver a la gestión de partidos")

                opcion_busqueda = input("Seleccione una opción: ")

                if opcion_busqueda == "1":
                    pais = input("Ingrese el nombre del país: ")
                    partidos_filtrados = [partido for partido in partidos if partido.equipo_local.nombre == pais or partido.equipo_visitante.nombre == pais]
                    if partidos_filtrados:
                        print("\nPartidos encontrados:")
                        for partido in partidos_filtrados:
                            print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} - {partido.fecha_hora} - {partido.estadio.nombre}")
                    else:
                        print("No se encontraron partidos para ese país.")

                elif opcion_busqueda == "2":
                    estadio_nombre = input("Ingrese el nombre del estadio: ")
                    partidos_filtrados = [partido for partido in partidos if partido.estadio.nombre == estadio_nombre]
                    if partidos_filtrados:
                        print("\nPartidos encontrados:")
                        for partido in partidos_filtrados:
                            print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} - {partido.fecha_hora} - {partido.estadio.nombre}")
                    else:
                        print("No se encontraron partidos para ese estadio.")

                elif opcion_busqueda == "3":
                    fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
                    partidos_filtrados = [partido for partido in partidos if partido.fecha_hora.startswith(fecha)]
                    if partidos_filtrados:
                        print("\nPartidos encontrados:")
                        for partido in partidos_filtrados:
                            print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} - {partido.fecha_hora} - {partido.estadio.nombre}")
                    else:
                        print("No se encontraron partidos para esa fecha.")

                elif opcion_busqueda == "4":
                    break

                else:
                    print("Opción inválida.")

        elif opcion == "2":
            # Ver información de un partido
            partido_index = int(input("Ingrese el índice del partido (comenzando desde 1): ")) - 1
            if 0 <= partido_index < len(partidos):
                partido = partidos[partido_index]
                print(f"\nInformación del partido:")
                print(f"Equipo local: {partido.equipo_local.nombre}")
                print(f"Equipo visitante: {partido.equipo_visitante.nombre}")
                print(f"Fecha y hora: {partido.fecha_hora}")
                print(f"Estadio: {partido.estadio.nombre}")
            else:
                print("Índice de partido inválido.")

        elif opcion == "3":
            # Ver información de un estadio
            estadio_index = int(input("Ingrese el índice del estadio (comenzando desde 1): ")) - 1
            if 0 <= estadio_index < len(estadios):
                estadio = estadios[estadio_index]
                print(f"\nInformación del estadio:")
                print(f"Nombre: {estadio.nombre}")
                print(f"Ubicación: {estadio.ubicacion}")
            else:
                print("Índice de estadio inválido.")

        elif opcion == "4":
            break

        else:
            print("Opción inválida.")

# Gestion de venta de entradas
def gestion_venta_entradas(clientes, partidos, estadios):
    while True:
        print("\nGestion de Venta de Entradas")
        print("1. Comprar entrada")
        print("2. Ver historial de entradas")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Comprar entrada
            while True:
                print("\nDatos del cliente:")
                nombre = input("Nombre: ")
                cedula = input("Cédula: ")
                edad = int(input("Edad: "))
                cliente = Cliente(nombre, cedula, edad)

                # Verificar si el cliente ya existe
                cliente_existente = next((cliente for cliente in clientes if cliente.cedula == cedula), None)
                if cliente_existente:
                    cliente = cliente_existente
                else:
                    clientes.append(cliente)

                # Mostrar partidos disponibles
                print("\nPartidos disponibles:")
                for i, partido in enumerate(partidos):
                    print(f"{i+1}. {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} - {partido.fecha_hora} - {partido.estadio.nombre}")

                while True:
                    partido_index = int(input("Ingrese el índice del partido: ")) - 1
                    if 0 <= partido_index < len(partidos):
                        partido = partidos[partido_index]
                        break
                    else:
                        print("Índice de partido inválido.")

                # Mostrar tipos de entradas
                print("\nTipos de entradas:")
                print("1. General: $35")
                print("2. VIP: $75")

                while True:
                    tipo_entrada = input("Ingrese el tipo de entrada (1 o 2): ")
                    if tipo_entrada == "1":
                        tipo_entrada = "General"
                        costo = 35
                        break
                    elif tipo_entrada == "2":
                        tipo_entrada = "VIP"
                        costo = 75
                        break
                    else:
                        print("Opción inválida.")

                # Mostrar asientos disponibles
                print("\nAsientos disponibles:")
                asientos = []
                for fila in range(1, 11):
                    for numero in range(1, 51):
                        asiento = Asiento(numero, fila, False)
                        asientos.append(asiento)

                # Buscar asientos ocupados
                for entrada in entradas:
                    if entrada.partido == partido:
                        asientos[entrada.asiento.numero - 1].ocupado = True

                # Mostrar asientos disponibles
                for i, asiento in enumerate(asientos):
                    if not asiento.ocupado:
                        print(f"{i+1}. Asiento {asiento.numero} - Fila {asiento.fila}")

                while True:
                    asiento_index = int(input("Ingrese el índice del asiento: ")) - 1
                    if 0 <= asiento_index < len(asientos) and not asientos[asiento_index].ocupado:
                        asiento = asientos[asiento_index]
                        break
                    else:
                        print("Asiento inválido.")

                # Calcular costo de la entrada
                if cliente.cedula == "123456789":
                    costo = costo * 0.5
                    print("¡Felicidades! Tu entrada tiene un 50% de descuento por ser un número vampiro.")
                costo = costo * 1.16
                print(f"Costo total de la entrada: ${costo:.2f}")

                # Confirmar compra
                confirmar = input("¿Desea confirmar la compra? (s/n): ")
                if confirmar == "s":
                    entrada = Entrada(cliente, partido, tipo_entrada, asiento, costo)
                    entradas.append(entrada)
                    print("¡Compra exitosa!")
                    break
                else:
                    print("Compra cancelada.")

        elif opcion == "2":
            # Ver historial de entradas
            if entradas:
                print("\nHistorial de entradas:")
                for i, entrada in enumerate(entradas):
                    print(f"{i+1}. Partido: {entrada.partido.equipo_local.nombre} vs {entrada.partido.equipo_visitante.nombre} - {entrada.partido.fecha_hora} - {entrada.partido.estadio.nombre}")
                    print(f"  Tipo de entrada: {entrada.tipo}")
                    print(f"  Asiento: {entrada.asiento.numero} - Fila {entrada.asiento.fila}")
                    print(f"  Costo: ${entrada.costo:.2f}")
            else:
                print("No se han comprado entradas.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Gestion de asistencia a partidos
def gestion_asistencia_a_partidos(partidos):
    while True:
        print("\nGestion de Asistencia a Partidos")
        print("1. Registrar asistencia a un partido")
        print("2. Ver asistencia de un partido")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Registrar asistencia a un partido
            partido_index = int(input("Ingrese el índice del partido (comenzando desde 1): ")) - 1
            if 0 <= partido_index < len(partidos):
                partido = partidos[partido_index]
                while True:
                    try:
                        asistencia = int(input("Ingrese la cantidad de asistentes: "))
                        if asistencia >= 0:
                            partido.asistencia = asistencia
                            print("Asistencia registrada correctamente.")
                            break
                        else:
                            print("La asistencia debe ser un número positivo.")
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
            else:
                print("Índice de partido inválido.")

        elif opcion == "2":
            # Ver asistencia de un partido
            partido_index = int(input("Ingrese el índice del partido (comenzando desde 1): ")) - 1
            if 0 <= partido_index < len(partidos):
                partido = partidos[partido_index]
                print(f"\nAsistencia del partido: {partido.asistencia}")
            else:
                print("Índice de partido inválido.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Gestion de restaurantes
def gestion_restaurantes(productos):
    while True:
        print("\nGestion de Restaurantes")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Ver todos los productos")
        print("4. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Agregar producto
            nombre = input("Nombre del producto: ")
            tipo = input("Tipo de producto (alimento o bebida): ")
            while True:
                try:
                    precio = float(input("Precio del producto: "))
                    if precio >= 0:
                        break
                    else:
                        print("El precio debe ser un número positivo.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
            producto = Producto(nombre, tipo, precio)
            productos.append(producto)
            print("Producto agregado correctamente.")

        elif opcion == "2":
            # Buscar producto
            criterio = input("Ingrese el criterio de búsqueda (nombre, tipo o rango de precio): ")
            if criterio == "nombre":
                nombre = input("Ingrese el nombre del producto: ")
                productos_filtrados = [producto for producto in productos if producto.nombre.lower() == nombre.lower()]
            elif criterio == "tipo":
                tipo = input("Ingrese el tipo de producto (alimento o bebida): ")
                productos_filtrados = [producto for producto in productos if producto.tipo.lower() == tipo.lower()]
            elif criterio == "rango de precio":
                while True:
                    try:
                        precio_minimo = float(input("Ingrese el precio mínimo: "))
                        precio_maximo = float(input("Ingrese el precio máximo: "))
                        if precio_minimo >= 0 and precio_maximo >= 0 and precio_minimo <= precio_maximo:
                            break
                        else:
                            print("Los precios deben ser números positivos y el precio mínimo debe ser menor o igual al precio máximo.")
                    except ValueError:
                        print("Por favor, ingrese números válidos.")
                productos_filtrados = [producto for producto in productos if precio_minimo <= producto.precio <= precio_maximo]
            else:
                print("Criterio de búsqueda inválido.")

            if productos_filtrados:
                print("\nProductos encontrados:")
                for producto in productos_filtrados:
                    print(f"Nombre: {producto.nombre}")
                    print(f"Tipo: {producto.tipo}")
                    print(f"Precio: ${producto.precio:.2f}")
            else:
                print("No se encontraron productos que coincidan con la búsqueda.")

        elif opcion == "3":
            # Ver todos los productos
            if productos:
                print("\nTodos los productos:")
                for producto in productos:
                    print(f"Nombre: {producto.nombre}")
                    print(f"Tipo: {producto.tipo}")
                    print(f"Precio: ${producto.precio:.2f}")
            else:
                print("No hay productos registrados.")

        elif opcion == "4":
            break

        else:
            print("Opción inválida.")

# Gestion de venta de restaurantes
def gestion_venta_restaurantes(clientes, productos, entradas):
    while True:
        print("\nGestion de Venta de Restaurantes")
        print("1. Hacer pedido")
        print("2. Ver historial de pedidos")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Hacer pedido
            cedula = input("Ingrese la cédula del cliente: ")
            cliente = next((cliente for cliente in clientes if cliente.cedula == cedula), None)
            if cliente:
                # Verificar si el cliente tiene entrada VIP
                entrada_vip = next((entrada for entrada in entradas if entrada.cliente == cliente and entrada.tipo == "VIP"), None)
                if entrada_vip:
                    # Mostrar productos disponibles
                    print("\nProductos disponibles:")
                    for i, producto in enumerate(productos):
                        print(f"{i+1}. {producto.nombre} - ${producto.precio:.2f}")

                    # Seleccionar productos
                    productos_pedido = []
                    while True:
                        print("\nIngrese el índice del producto que desea agregar al pedido (0 para finalizar):")
                        producto_index = int(input("Índice del producto: ")) - 1
                        if 0 <= producto_index < len(productos):
                            productos_pedido.append(productos[producto_index])
                        elif producto_index == -1:
                            break
                        else:
                            print("Índice de producto inválido.")

                    # Calcular costo del pedido
                    costo_pedido = reduce(lambda total, producto: total + producto.precio, productos_pedido, 0)
                    if cliente.cedula == "123456789":
                        costo_pedido = costo_pedido * 0.85
                        print("¡Felicidades! Tu pedido tiene un 15% de descuento por ser un número perfecto.")
                    costo_pedido = costo_pedido * 1.16

                    # Confirmar pedido
                    print(f"\nCosto total del pedido: ${costo_pedido:.2f}")
                    confirmar = input("¿Desea confirmar el pedido? (s/n): ")
                    if confirmar == "s":
                        orden_restaurante = OrdenRestaurante(cliente, productos_pedido, costo_pedido)
                        ordenes_restaurante.append(orden_restaurante)
                        print("¡Pedido realizado correctamente!")
                    else:
                        print("Pedido cancelado.")
                else:
                    print("El cliente no tiene una entrada VIP.")
            else:
                print("Cliente no encontrado.")

        elif opcion == "2":
            # Ver historial de pedidos
            if ordenes_restaurante:
                print("\nHistorial de pedidos:")
                for i, orden in enumerate(ordenes_restaurante):
                    print(f"{i+1}. Cliente: {orden.cliente.nombre}")
                    print(f"  Productos:")
                    for producto in orden.productos:
                        print(f"    {producto.nombre} - ${producto.precio:.2f}")
                    print(f"  Costo total: ${orden.costo:.2f}")
            else:
                print("No se han realizado pedidos.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Indicadores de gestión
def indicadores_de_gestion(entradas, partidos, ordenes_restaurante):
    # 1. Promedio de gasto de un cliente VIP en un partido
    gasto_vip_partido = 0
    cantidad_entradas_vip = 0
    for entrada in entradas:
        if entrada.tipo == "VIP":
            gasto_vip_partido += entrada.costo
            cantidad_entradas_vip += 1
    promedio_gasto_vip_partido = gasto_vip_partido / cantidad_entradas_vip if cantidad_entradas_vip > 0 else 0
    print(f"\nPromedio de gasto de un cliente VIP en un partido: ${promedio_gasto_vip_partido:.2f}")

    # 2. Tabla de asistencia a los partidos de mejor a peor
    partidos_ordenados = sorted(partidos, key=lambda partido: partido.asistencia, reverse=True)
    print("\nTabla de asistencia a los partidos de mejor a peor:")
    print("-------------------------------------------------------------------------------------")
    print(f"|{'Partido':20}|{'Estadio':20}|{'Asistencia':10}|")
    print("-------------------------------------------------------------------------------------")
    for partido in partidos_ordenados:
        print(f"|{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}: {partido.fecha_hora}: {partido.estadio.nombre}|")
    print("-------------------------------------------------------------------------------------")

    # 3. Partido con mayor asistencia
    partido_mayor_asistencia = max(partidos, key=lambda partido: partido.asistencia)
    print(f"\nPartido con mayor asistencia: {partido_mayor_asistencia.equipo_local.nombre} vs {partido_mayor_asistencia.equipo_visitante.nombre} - {partido_mayor_asistencia.fecha_hora} - {partido_mayor_asistencia.estadio.nombre} - Asistencia: {partido_mayor_asistencia.asistencia}")

    # 4. Partido con mayor boletos vendidos
    partido_mayor_boletos_vendidos = max(partidos, key=lambda partido: sum(1 for entrada in entradas if entrada.partido == partido))
    print(f"\nPartido con mayor boletos vendidos: {partido_mayor_boletos_vendidos.equipo_local.nombre} vs {partido_mayor_boletos_vendidos.equipo_visitante.nombre} - {partido_mayor_boletos_vendidos.fecha_hora} - {partido_mayor_boletos_vendidos.estadio.nombre}")

    # 5. Top 3 productos más vendidos en el restaurante
    productos_mas_vendidos = sorted(productos, key=lambda producto: sum(1 for orden in ordenes_restaurante for item in orden.productos if item == producto), reverse=True)
    print("\nTop 3 productos más vendidos en el restaurante:")
    for i, producto in enumerate(productos_mas_vendidos[:3]):
        print(f"{i+1}. {producto.nombre} - {producto.tipo} - Precio: ${producto.precio:.2f}")

    # 6. Top 3 clientes (clientes que más compraron boletos)
    clientes_mas_entradas = sorted(clientes, key=lambda cliente: sum(1 for entrada in entradas if entrada.cliente == cliente), reverse=True)
    print("\nTop 3 clientes (clientes que más compraron boletos):")
    for i, cliente in enumerate(clientes_mas_entradas[:3]):
        print(f"{i+1}. {cliente.nombre} - Cédula: {cliente.cedula}")

    # 7. Gráficos con las estadísticas (Bonus)
    # (Pendiente de implementar la parte de gráficos)

# Menu principal
def menu_principal():
    equipos = cargar_equipos()
    estadios = cargar_estadios()
    partidos = cargar_partidos(equipos, estadios)
    clientes = []
    entradas = []
    productos = []
    ordenes_restaurante = []

    while True:
        print("\nMenu Principal")
        print("1. Gestion de partidos y estadios")
        print("2. Gestion de venta de entradas")
        print("3. Gestion de asistencia a partidos")
        print("4. Gestion de restaurantes")
        print("5. Gestion de venta de restaurantes")
        print("6. Indicadores de gestion")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestion_partidos_y_estadios(equipos, estadios, partidos)
        elif opcion == "2":
            gestion_venta_entradas(clientes, partidos, estadios)
        elif opcion == "3":
            gestion_asistencia_a_partidos(partidos)
        elif opcion == "4":
            gestion_restaurantes(productos)
        elif opcion == "5":
            gestion_venta_restaurantes(clientes, productos, entradas)
        elif opcion == "6":
            indicadores_de_gestion(entradas, partidos, ordenes_restaurante)
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()