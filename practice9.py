import requests
import json
import random

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
    def __init__(self, equipo_local, equipo_visitante, fecha, hora, estadio):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.fecha = fecha
        self.hora = hora
        self.estadio = estadio

class Cliente:
    def __init__(self, nombre, cedula, edad):
        self.nombre = nombre
        self.cedula = cedula
        self.edad = edad

class Entrada:
    def __init__(self, partido, tipo, asiento):
        self.partido = partido
        self.tipo = tipo
        self.asiento = asiento

class Restaurante:
    def __init__(self, nombre, tipo, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio

class VentaRestaurante:
    def __init__(self, cliente, productos):
        self.cliente = cliente
        self.productos = productos

# Cargar datos de la API
def cargar_datos():
    equipos = []
    estadios = []
    partidos = []
    restaurantes = []

    # Equipos
    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
    response_equipos = requests.get(url_equipos)
    data_equipos = json.loads(response_equipos.text)

    for equipo in data_equipos:
        equipos.append(Equipo(equipo["nombre"], equipo["codigo_fifa"], equipo["grupo"]))

    # Estadios
    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    response_estadios = requests.get(url_estadios)
    data_estadios = json.loads(response_estadios.text)

    for estadio in data_estadios:
        estadios.append(Estadio(estadio["nombre"], estadio["ubicacion"]))

    # Partidos
    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
    response_partidos = requests.get(url_partidos)
    data_partidos = json.loads(response_partidos.text)

    for partido in data_partidos:
        equipo_local = next((e for e in equipos if e.codigo_fifa == partido["equipo_local"]), None)
        equipo_visitante = next((e for e in equipos if e.codigo_fifa == partido["equipo_visitante"]), None)
        estadio = next((s for s in estadios if s.nombre == partido["estadio"]), None)
        partidos.append(Partido(equipo_local, equipo_visitante, partido["fecha"], partido["hora"], estadio))

    # Restaurantes
    restaurantes.append(Restaurante("Hamburguesa", "Comida", 10))
    restaurantes.append(Restaurante("Pizza", "Comida", 15))
    restaurantes.append(Restaurante("Cerveza", "Bebida", 5))
    restaurantes.append(Restaurante("Refresco", "Bebida", 3))

    return equipos, estadios, partidos, restaurantes

# Gestión de partidos y estadios
def gestionar_partidos_estadios(equipos, estadios, partidos):
    while True:
        print("\n--- Gestión de Partidos y Estadios ---")
        print("1. Buscar partidos por país")
        print("2. Buscar partidos por estadio")
        print("3. Buscar partidos por fecha")
        print("4. Ver información de un partido")
        print("5. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            pais = input("Ingrese el nombre del país: ")
            partidos_pais = [p for p in partidos if p.equipo_local.nombre == pais or p.equipo_visitante.nombre == pais]
            if partidos_pais:
                print("\nPartidos del país", pais)
                for p in partidos_pais:
                    print(f"{p.equipo_local.nombre} vs {p.equipo_visitante.nombre} - {p.fecha} - {p.hora} - {p.estadio.nombre}")
            else:
                print("No se encontraron partidos para este país.")

        elif opcion == "2":
            nombre_estadio = input("Ingrese el nombre del estadio: ")
            partidos_estadio = [p for p in partidos if p.estadio.nombre == nombre_estadio]
            if partidos_estadio:
                print("\nPartidos en el estadio", nombre_estadio)
                for p in partidos_estadio:
                    print(f"{p.equipo_local.nombre} vs {p.equipo_visitante.nombre} - {p.fecha} - {p.hora}")
            else:
                print("No se encontraron partidos en este estadio.")

        elif opcion == "3":
            fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
            partidos_fecha = [p for p in partidos if p.fecha == fecha]
            if partidos_fecha:
                print("\nPartidos en la fecha", fecha)
                for p in partidos_fecha:
                    print(f"{p.equipo_local.nombre} vs {p.equipo_visitante.nombre} - {p.hora} - {p.estadio.nombre}")
            else:
                print("No se encontraron partidos en esta fecha.")

        elif opcion == "4":
            codigo_partido = input("Ingrese el código del partido: ")
            partido = next((p for p in partidos if p.equipo_local.codigo_fifa == codigo_partido or p.equipo_visitante.codigo_fifa == codigo_partido), None)
            if partido:
                print("\nInformación del partido:")
                print(f"Equipo Local: {partido.equipo_local.nombre}")
                print(f"Equipo Visitante: {partido.equipo_visitante.nombre}")
                print(f"Fecha: {partido.fecha}")
                print(f"Hora: {partido.hora}")
                print(f"Estadio: {partido.estadio.nombre}")
            else:
                print("No se encontró el partido.")

        elif opcion == "5":
            break

        else:
            print("Opción inválida.")

# Gestión de venta de entradas
def gestionar_venta_entradas(equipos, estadios, partidos):
    clientes = []
    entradas = []
    while True:
        print("\n--- Gestión de Venta de Entradas ---")
        print("1. Comprar entrada")
        print("2. Ver información de la entrada")
        print("3. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del cliente: ")
            cedula = input("Ingrese la cédula del cliente: ")
            edad = int(input("Ingrese la edad del cliente: "))
            cliente = Cliente(nombre, cedula, edad)
            clientes.append(cliente)

            # Mostrar partidos disponibles
            print("\nPartidos disponibles:")
            for i, p in enumerate(partidos):
                print(f"{i+1}. {p.equipo_local.nombre} vs {p.equipo_visitante.nombre} - {p.fecha} - {p.hora} - {p.estadio.nombre}")

            partido_index = int(input("Ingrese el número del partido: ")) - 1
            partido = partidos[partido_index]

            # Mostrar tipos de entrada
            print("\nTipos de entrada:")
            print("1. General - $35")
            print("2. VIP - $75")

            tipo_entrada = int(input("Ingrese el número de la entrada: "))

            if tipo_entrada == 1:
                tipo = "General"
                precio = 35
            elif tipo_entrada == 2:
                tipo = "VIP"
                precio = 75
            else:
                print("Opción inválida.")
                continue

            # Generar asiento aleatorio
            asiento = random.randint(1, 100)
            entrada = Entrada(partido, tipo, asiento)
            entradas.append(entrada)

            # Calcular descuento
            descuento = 0
            if int(cedula) == int(str(cedula)[::-1]):  # Número vampiro
                descuento = 0.5

            # Calcular precio final
            precio_final = precio * (1 - descuento) + precio * 0.16  # IVA

            print("\nCompra exitosa:")
            print(f"Nombre del cliente: {cliente.nombre}")
            print(f"Cédula: {cliente.cedula}")
            print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
            print(f"Tipo de entrada: {tipo}")
            print(f"Asiento: {asiento}")
            print(f"Precio: ${precio_final:.2f}")

        elif opcion == "2":
            cedula = input("Ingrese la cédula del cliente: ")
            entrada = next((e for e in entradas if e.partido.equipo_local.codigo_fifa == cedula or e.partido.equipo_visitante.codigo_fifa == cedula), None)
            if entrada:
                print("\nInformación de la entrada:")
                print(f"Partido: {entrada.partido.equipo_local.nombre} vs {entrada.partido.equipo_visitante.nombre}")
                print(f"Tipo de entrada: {entrada.tipo}")
                print(f"Asiento: {entrada.asiento}")
            else:
                print("No se encontró la entrada.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Gestión de asistencia a partidos
def gestionar_asistencia_partidos(entradas):
    asistencia = {}
    while True:
        print("\n--- Gestión de Asistencia a Partidos ---")
        print("1. Registrar asistencia")
        print("2. Ver asistencia de un partido")
        print("3. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            codigo_partido = input("Ingrese el código del partido: ")
            entrada = next((e for e in entradas if e.partido.equipo_local.codigo_fifa == codigo_partido or e.partido.equipo_visitante.codigo_fifa == codigo_partido), None)
            if entrada:
                if entrada.partido in asistencia:
                    asistencia[entrada.partido] += 1
                else:
                    asistencia[entrada.partido] = 1
                print("Asistencia registrada.")
            else:
                print("No se encontró la entrada.")

        elif opcion == "2":
            codigo_partido = input("Ingrese el código del partido: ")
            partido = next((p for p in partidos if p.equipo_local.codigo_fifa == codigo_partido or p.equipo_visitante.codigo_fifa == codigo_partido), None)
            if partido in asistencia:
                print(f"Asistencia del partido {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}: {asistencia[partido]}")
            else:
                print("No se encontró asistencia para este partido.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Gestión de restaurantes
def gestionar_restaurantes(restaurantes):
    while True:
        print("\n--- Gestión de Restaurantes ---")
        print("1. Ver menú del restaurante")
        print("2. Buscar producto")
        print("3. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            print("\nMenú del restaurante:")
            for r in restaurantes:
                print(f"{r.nombre} - {r.tipo} - ${r.precio:.2f}")

        elif opcion == "2":
            nombre_producto = input("Ingrese el nombre del producto: ")
            producto = next((r for r in restaurantes if r.nombre == nombre_producto), None)
            if producto:
                print(f"Producto encontrado: {producto.nombre} - {producto.tipo} - ${producto.precio:.2f}")
            else:
                print("Producto no encontrado.")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Gestión de venta de restaurantes
def gestionar_venta_restaurantes(clientes, restaurantes):
    ventas = []
    while True:
        print("\n--- Gestión de Venta de Restaurantes ---")
        print("1. Comprar producto")
        print("2. Ver ventas")
        print("3. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            cedula = input("Ingrese la cédula del cliente: ")
            cliente = next((c for c in clientes if c.cedula == cedula), None)
            if cliente:
                if cliente.edad >= 18:
                    print("\nMenú del restaurante:")
                    for i, r in enumerate(restaurantes):
                        print(f"{i+1}. {r.nombre} - {r.tipo} - ${r.precio:.2f}")

                    productos = []
                    while True:
                        opcion_producto = input("Ingrese el número del producto (0 para terminar): ")
                        if opcion_producto == "0":
                            break
                        producto_index = int(opcion_producto) - 1
                        producto = restaurantes[producto_index]
                        productos.append(producto)

                    venta = VentaRestaurante(cliente, productos)
                    ventas.append(venta)

                    # Calcular subtotal
                    subtotal = sum(p.precio for p in productos)

                    # Calcular descuento
                    descuento = 0
                    if int(cedula) == int(str(cedula)[::-1]):  # Número vampiro
                        descuento = 0.15

                    # Calcular total
                    total = subtotal * (1 - descuento)

                    print("\nCompra exitosa:")
                    print(f"Nombre del cliente: {cliente.nombre}")
                    print(f"Cédula: {cliente.cedula}")
                    print(f"Subtotal: ${subtotal:.2f}")
                    print(f"Descuento: ${subtotal * descuento:.2f}")
                    print(f"Total: ${total:.2f}")
                else:
                    print("El cliente no puede comprar bebidas alcohólicas.")
            else:
                print("Cliente no encontrado.")

        elif opcion == "2":
            for i, venta in enumerate(ventas):
                print(f"\nVenta {i+1}:")
                print(f"Cliente: {venta.cliente.nombre}")
                print(f"Productos: {', '.join(p.nombre for p in venta.productos)}")
                print(f"Total: ${sum(p.precio for p in venta.productos):.2f}")

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

# Indicadores de gestión (Estadísticas)
def indicadores_gestion(equipos, estadios, partidos, clientes, entradas, ventas):
    while True:
        print("\n--- Indicadores de Gestión ---")
        print("1. Promedio de gasto de cliente VIP")
        print("2. Asistencia de partidos")
        print("3. Partidos con mayor asistencia")
        print("4. Partidos con mayor boletos vendidos")
        print("5. Productos más vendidos en el restaurante")
        print("6. Clientes con más boletos comprados")
        print("7. Gráficos de estadísticas")
        print("8. Regresar al menú principal")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            gasto_vip = 0
            cantidad_vip = 0
            for entrada in entradas:
                if entrada.tipo == "VIP":
                    gasto_vip += 35  # Precio de la entrada VIP
                    cantidad_vip += 1
            promedio_gasto_vip = gasto_vip / cantidad_vip if cantidad_vip > 0 else 0
            print(f"Promedio de gasto de cliente VIP: ${promedio_gasto_vip:.2f}")

        elif opcion == "2":
            asistencia_partidos = {}
            for entrada in entradas:
                partido = entrada.partido
                if partido in asistencia_partidos:
                    asistencia_partidos[partido] += 1
                else:
                    asistencia_partidos[partido] = 1

            print("\nAsistencia de partidos:")
            for partido, asistencia in asistencia_partidos.items():
                print(f"{partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} - Asistencia: {asistencia}")

        elif opcion == "3":
            asistencia_partidos = {}
            for entrada in entradas:
                partido = entrada.partido
                if partido in asistencia_partidos:
                    asistencia_partidos[partido] += 1
                else:
                    asistencia_partidos[partido] = 1

            partido_max_asistencia = max(asistencia_partidos, key=asistencia_partidos.get)
            print(f"Partido con mayor asistencia: {partido_max_asistencia.equipo_local.nombre} vs {partido_max_asistencia.equipo_visitante.nombre} - Asistencia: {asistencia_partidos[partido_max_asistencia]}")

        elif opcion == "4":
            boletos_vendidos_partidos = {}
            for entrada in entradas:
                partido = entrada.partido
                if partido in boletos_vendidos_partidos:
                    boletos_vendidos_partidos[partido] += 1
                else:
                    boletos_vendidos_partidos[partido] = 1

            partido_max_boletos = max(boletos_vendidos_partidos, key=boletos_vendidos_partidos.get)
            print(f"Partido con mayor boletos vendidos: {partido_max_boletos.equipo_local.nombre} vs {partido_max_boletos.equipo_visitante.nombre} - Boletos vendidos: {boletos_vendidos_partidos[partido_max_boletos]}")

        elif opcion == "5":
            productos_vendidos = {}
            for venta in ventas:
                for producto in venta.productos:
                    if producto in productos_vendidos:
                        productos_vendidos[producto] += 1
                    else:
                        productos_vendidos[producto] = 1

            productos_mas_vendidos = sorted(productos_vendidos.items(), key=lambda x: x[1], reverse=True)[:3]
            print("\nProductos más vendidos en el restaurante:")
            for producto, cantidad in productos_mas_vendidos:
                print(f"{producto.nombre} - Cantidad: {cantidad}")

        elif opcion == "6":
            boletos_comprados_clientes = {}
            for entrada in entradas:
                cliente = next((c for c in clientes if c.cedula == entrada.partido.equipo_local.codigo_fifa or c.cedula == entrada.partido.equipo_visitante.codigo_fifa), None)
                if cliente:
                    if cliente in boletos_comprados_clientes:
                        boletos_comprados_clientes[cliente] += 1
                    else:
                        boletos_comprados_clientes[cliente] = 1

            clientes_mas_boletos = sorted(boletos_comprados_clientes.items(), key=lambda x: x[1], reverse=True)[:3]
            print("\nClientes con más boletos comprados:")
            for cliente, cantidad in clientes_mas_boletos:
                print(f"{cliente.nombre} - Cantidad: {cantidad}")

        elif opcion == "7":
            print("Opción de gráficos (Bono) no implementada.")

        elif opcion == "8":
            break

        else:
            print("Opción inválida.")

# Menú principal
if __name__ == "__main__":
    equipos, estadios, partidos, restaurantes = cargar_datos()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Gestión de Partidos y Estadios")
        print("2. Gestión de Venta de Entradas")
        print("3. Gestión de Asistencia a Partidos")
        print("4. Gestión de Restaurantes")
        print("5. Gestión de Venta de Restaurantes")
        print("6. Indicadores de Gestión")
        print("7. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            gestionar_partidos_estadios(equipos, estadios, partidos)
        elif opcion == "2":
            gestionar_venta_entradas(equipos, estadios, partidos)
        elif opcion == "3":
            gestionar_asistencia_partidos(entradas)
        elif opcion == "4":
            gestionar_restaurantes(restaurantes)
        elif opcion == "5":
            gestionar_venta_restaurantes(clientes, restaurantes)
        elif opcion == "6":
            indicadores_gestion(equipos, estadios, partidos, clientes, entradas, ventas)
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")