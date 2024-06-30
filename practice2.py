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

# Funciones auxiliares para validar números vampiro y números perfectos
def es_numero_vampiro(cedula):
    cedula_str = str(cedula)
    largo = len(cedula_str)
    if largo % 2 != 0:
        return False
    mitad1 = cedula_str[:largo // 2]
    mitad2 = cedula_str[largo // 2:]
    for divisor in range(1, int(mitad1) + 1):
        if divisor * int(mitad2) == cedula and divisor != 1 and divisor != int(mitad1):
            return True
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
        codigo_fifa = equipo_json["fifa_code"]
        grupo = equipo_json["group"]
        equipos.append(Equipo(nombre, codigo_fifa, grupo))
    return equipos

def cargar_estadios():
    estadios_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json").json()
    estadios = []
    for estadio_json in estadios_json:
        nombre = estadio_json["name"]
        ubicacion = estadio_json["location"]
        estadios.append(Estadio(nombre, ubicacion))
    return estadios

def cargar_partidos():
    partidos_json = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json").json()
    partidos = []
    for partido_json in partidos_json:
        equipo_local_codigo_fifa = partido_json["home_team_fifa_code"]
        equipo_visitante_codigo_fifa = partido_
