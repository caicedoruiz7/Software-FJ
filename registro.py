# registro.py
# Guarda los errores y eventos en el archivo de logs (eventos.log).
from datetime import datetime


def registrar(nivel, mensaje):
    """Escribe una línea en eventos.log con fecha, nivel y mensaje."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # fecha y hora actual
    # "a" = agregar al final del archivo sin borrar lo anterior
    with open("eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha} | {nivel} | {mensaje}\n")
