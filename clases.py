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
        num_sections = (self.columns + 29) // 30
        for section in range(num_sections):
            start_column = section * 30
            end_column = min(start_column + 30, self.columns)
            print(f"\nSección {chr(ord('A') + section)}")
            print("   ", end="")
            for column in range(start_column, end_column):
                print(f"{column - start_column + 1:2d} ", end=" ") 
            print()
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
        with open("occupied_seats.json", "w") as f:
            occupied_seats = []
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.seats[row][column].occupied:
                        occupied_seats.append({"row": row, "column": column})
            json.dump(occupied_seats, f)
    def load_occupied_seats(self):
        try:
            with open("occupied_seats.json", "r") as f:
                occupied_seats_data = json.load(f)
                for seat_data in occupied_seats_data:
                    self.seats[seat_data["row"]][seat_data["column"]].occupy()
        except FileNotFoundError:
            pass