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

class SistemaEuro2024:
    def __init__(self):
        self.equipos = []
        self.estadios = []
        self.partidos = []
        self.clientes = []
        self.entradas = []
        self.restaurantes = []
        self.ventas_restaurante = []
        self.cargar_datos()

    def cargar_datos(self):
        # Cargar datos de equipos desde la API
        with open('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json') as f:
            teams_data = json.load(f)
        for team in teams_data:
            self.equipos.append(Equipo(team['name'], team['fifaCode'], team['group']))

        # Cargar datos de estadios desde la API
        with open('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json') as f:
            stadiums_data = json.load(f)
        for stadium in stadiums_data:
            self.estadios.append(Estadio(stadium['name'], stadium['location']))

        # Cargar datos de partidos desde la API
        with open('https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json') as f:
            matches_data = json.load(f)
        for match in matches_data:
            equipo_local = next((e for e in self.equipos if e.codigo_fifa == match['homeTeam']), None)
            equipo_visitante = next((e for e in self.equipos if e.codigo_fifa == match['awayTeam']), None)
            estadio = next((s for s in self.estadios if s.nombre == match['stadium']), None)
            self.partidos.append(Partido(equipo_local, equipo_visitante, match['date'], match['time'], estadio))

    def registrar_cliente(self, nombre, cedula, edad):
        cliente = Cliente(nombre, cedula, edad)
        self.clientes.append(cliente)
        return cliente

    def vender_entrada(self, cliente, partido, tipo):
        # Verificar si el cliente ya tiene una entrada para el partido
        if any(e.partido == partido and e.cliente == cliente for e in self.entradas):
            print("El cliente ya tiene una entrada para este partido.")
            return
        # Verificar la edad del cliente para la compra de bebidas alcohólicas
        if tipo == 'VIP' and cliente.edad < 18:
            print("El cliente es menor de edad y no puede comprar una entrada VIP.")
            return

        # Seleccionar asiento aleatorio
        asiento = random.randint(1, 100)
        entrada = Entrada(partido, tipo, asiento)
        self.entradas.append(entrada)
        print(f"Entrada vendida para {cliente.nombre} para el partido {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre} en el asiento {asiento}.")

    def generar_reporte_partidos(self):
        print("Reporte de partidos:")
        for partido in self.partidos:
            print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
            print(f"Estadio: {partido.estadio.nombre}")
            print(f"Fecha: {partido.fecha}")
            print(f"Hora: {partido.hora}")
            print("-" * 20)

    def generar_reporte_clientes(self):
        print("Reporte de clientes:")
        for cliente in self.clientes:
            print(f"Cliente: {cliente.nombre}")
            print(f"Cédula: {cliente.cedula}")
            print(f"Edad: {cliente.edad}")
            print("-" * 20)

    def generar_reporte_entradas(self):
        print("Reporte de entradas:")
        for entrada in self.entradas:
            print(f"Partido: {entrada.partido.equipo_local.nombre} vs {entrada.partido.equipo_visitante.nombre}")
            print(f"Tipo: {entrada.tipo}")
            print(f"Asiento: {entrada.asiento}")
            print("-" * 20)

    def buscar_partido(self, filtro):
        if filtro == 'pais':
            nombre_pais = input("Ingrese el nombre del país: ")
            partidos_filtrados = [p for p in self.partidos if p.equipo_local.nombre.lower() == nombre_pais.lower() or p.equipo_visitante.nombre.lower() == nombre_pais.lower()]
        elif filtro == 'estadio':
            nombre_estadio = input("Ingrese el nombre del estadio: ")
            partidos_filtrados = [p for p in self.partidos if p.estadio.nombre.lower() == nombre_estadio.lower()]
        elif filtro == 'fecha':
            fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
            partidos_filtrados = [p for p in self.partidos if p.fecha == fecha]
        else:
            print("Opción de filtro inválida.")
            return

        if partidos_filtrados:
            print("Partidos encontrados:")
            for partido in partidos_filtrados:
                print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
                print(f"Estadio: {partido.estadio.nombre}")
                print(f"Fecha: {partido.fecha}")
                print(f"Hora: {partido.hora}")
                print("-" * 20)
        else:
            print("No se encontraron partidos con los criterios especificados.")

    def generar_reporte_estadios(self):
        print("Reporte de estadios:")
        for estadio in self.estadios:
            print(f"Estadio: {estadio.nombre}")
            print(f"Ubicación: {estadio.ubicacion}")
            print("-" * 20)

    def generar_reporte_equipos(self):
        print("Reporte de equipos:")
        for equipo in self.equipos:
            print(f"Equipo: {equipo.nombre}")
            print(f"Código FIFA: {equipo.codigo_fifa}")
            print(f"Grupo: {equipo.grupo}")
            print("-" * 20)

    def generar_reporte_asistencia(self):
        asistencia = {}
        for partido in self.partidos:
            asistencia[partido] = 0
        for entrada in self.entradas:
            asistencia[entrada.partido] += 1
        print("Reporte de asistencia:")
        for partido, asistentes in asistencia.items():
            print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
            print(f"Asistentes: {asistentes}")
            print("-" * 20)


if __name__ == "__main__":
    sistema = SistemaEuro2024()
    while True:
        print("\n--- Menú ---")
        print("1. Registrar cliente")
        print("2. Vender entrada")
        print("3. Generar reporte de partidos")
        print("4. Generar reporte de clientes")
        print("5. Generar reporte de entradas")
        print("6. Buscar partido")
        print("7. Generar reporte de estadios")
        print("8. Generar reporte de equipos")
        print("9. Generar reporte de asistencia")
        print("10. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del cliente: ")
            cedula = input("Ingrese la cédula del cliente: ")
            edad = int(input("Ingrese la edad del cliente: "))
            sistema.registrar_cliente(nombre, cedula, edad)
        elif opcion == '2':
            nombre = input("Ingrese el nombre del cliente: ")
            cedula = input("Ingrese la cédula del cliente: ")
            cliente = next((c for c in sistema.clientes if c.nombre == nombre and c.cedula == cedula), None)
            if cliente is None:
                print("Cliente no encontrado.")
                continue
            print("Seleccione un partido:")
            for i, partido in enumerate(sistema.partidos):
                print(f"{i+1}. {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
            partido_index = int(input("Ingrese el número del partido: ")) - 1
            if partido_index < 0 or partido_index >= len(sistema.partidos):
                print("Partido inválido.")
                continue
            partido = sistema.partidos[partido_index]
            print("Seleccione el tipo de entrada:")
            print("1. General")
            print("2. VIP")
            tipo_index = int(input("Ingrese el número del tipo de entrada: ")) - 1
            if tipo_index < 0 or tipo_index >= 2:
                print("Tipo de entrada inválido.")
                continue
            tipo = 'General' if tipo_index == 0 else 'VIP'
            sistema.vender_entrada(cliente, partido, tipo)
        elif opcion == '3':
            sistema.generar_reporte_partidos()
        elif opcion == '4':
            sistema.generar_reporte_clientes()
        elif opcion == '5':
            sistema.generar_reporte_entradas()
        elif opcion == '6':
            print("Seleccione el filtro de búsqueda:")
            print("1. País")
            print("2. Estadio")
            print("3. Fecha")
            filtro_index = int(input("Ingrese el número del filtro: ")) - 1
            if filtro_index < 0 or filtro_index >= 3:
                print("Filtro inválido.")
                continue
            filtro = 'pais' if filtro_index == 0 else 'estadio' if filtro_index == 1 else 'fecha'
            sistema.buscar_partido(filtro)
        elif opcion == '7':
            sistema.generar_reporte_estadios()
        elif opcion == '8':
            sistema.generar_reporte_equipos()
        elif opcion == '9':
            sistema.generar_reporte_asistencia()
        elif opcion == '10':
            break
        else:
            print("Opción inválida.")