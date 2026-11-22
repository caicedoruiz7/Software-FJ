# main.py
# Programa principal de Software FJ: simula más de 10 operaciones
# (válidas e inválidas). El programa sigue funcionando aunque haya errores.
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ErrorFJ
from registro import registrar

# Listas internas (no usamos base de datos)
clientes = []
servicios = []
reservas = []


def registrar_cliente(nombre, documento, correo, telefono):
    """Crea un cliente y lo guarda en la lista. Devuelve None si hay error."""
    try:
        # Revisamos que el documento no esté repetido
        for c in clientes:
            if c.get_documento() == str(documento).strip():
                raise ErrorFJ(f"Ya existe un cliente con documento {documento}")
        cliente = Cliente(nombre, documento, correo, telefono)
    except ErrorFJ as e:
        registrar("ERROR", f"registrar_cliente: {e}")
        print("   ERROR:", e)
        return None
    else:
        clientes.append(cliente)
        registrar("INFO", f"Cliente registrado: {cliente.describir()}")
        print("   OK:", cliente.describir())
        return cliente
    finally:
        registrar("DEBUG", "Terminó registrar_cliente")


def crear_servicio(clase, **datos):
    """Crea un servicio de la clase indicada. Devuelve None si hay error."""
    try:
        servicio = clase(**datos)
    except TypeError as e:
        # Faltan parámetros al crear el objeto
        registrar("ERROR", f"crear_servicio: parámetros incorrectos ({e})")
        print("   ERROR: faltan parámetros del servicio")
        return None
    except ErrorFJ as e:
        registrar("ERROR", f"crear_servicio: {e} | causa: {e.__cause__}")
        print("   ERROR:", e)
        return None
    else:
        servicios.append(servicio)
        registrar("INFO", f"Servicio creado: {servicio.describir()}")
        print("   OK:", servicio.describir())
        return servicio


def crear_reserva(documento, servicio, horas):
    """Busca al cliente por documento y crea la reserva."""
    try:
        cliente = None
        for c in clientes:
            if c.get_documento() == str(documento):
                cliente = c
        if cliente is None:
            raise ErrorFJ(f"No existe un cliente con documento {documento}")
        reserva = Reserva(cliente, servicio, horas)
    except ErrorFJ as e:
        registrar("ERROR", f"crear_reserva: {e} | causa: {e.__cause__}")
        print("   ERROR:", e)
        return None
    else:
        reservas.append(reserva)
        registrar("INFO", f"Reserva creada: {reserva.describir()}")
        print("   OK:", reserva.describir())
        return reserva


def ejecutar(reserva, accion, **datos):
    """Ejecuta confirmar, cancelar o procesar sin que el programa se caiga."""
    try:
        getattr(reserva, accion)(**datos)
    except ErrorFJ as e:
        print(f"   ERROR al {accion}:", e)
        return False
    print(f"   OK: {accion} -> {reserva.describir()}")
    return True


def main():
    registrar("INFO", "=== Programa iniciado ===")

    print("\n--- CLIENTES ---")
    print("1. Cliente válido (Ana)")
    registrar_cliente("Ana Gómez", "1010202030", "ana@correo.com", "3105551234")
    print("2. Cliente con correo inválido")
    registrar_cliente("Luis Pérez", "55512345", "luis-sin-arroba", "3001112233")
    print("3. Cliente sin nombre")
    registrar_cliente(None, "77788899", "x@correo.com", "3001112233")
    print("4. Cliente con documento repetido")
    registrar_cliente("Ana Repetida", "1010202030", "otra@correo.com", "3112223344")
    print("5. Cliente válido (Carlos)")
    registrar_cliente("Carlos Ruiz", "80123456", "carlos@correo.com", "3201234567")

    print("\n--- SERVICIOS ---")
    print("6. Sala válida")
    sala = crear_servicio(ReservaSala, nombre="Sala Ejecutiva", tarifa_hora=80000, capacidad=25)
    print("7. Sala con capacidad negativa")
    crear_servicio(ReservaSala, nombre="Sala Mala", tarifa_hora=50000, capacidad=-5)
    print("8. Equipo válido")
    equipo = crear_servicio(AlquilerEquipo, nombre="Proyector", tarifa_hora=15000,
                            tipo_equipo="Video", deposito=50000)
    print("9. Asesoría senior válida")
    asesoria = crear_servicio(AsesoriaEspecializada, nombre="Asesoría Datos",
                              tarifa_hora=120000, especialidad="Analítica", nivel="senior")
    print("10. Equipo con tarifa que no es número")
    crear_servicio(AlquilerEquipo, nombre="Cámara", tarifa_hora="abc", tipo_equipo="Foto")
    print("11. Asesoría con parámetros faltantes")
    crear_servicio(AsesoriaEspecializada, nombre="Asesoría incompleta")
    print("12. Sala no disponible")
    sala_cerrada = crear_servicio(ReservaSala, nombre="Sala en Mantenimiento",
                                  tarifa_hora=60000, capacidad=10, disponible=False)

    print("\n--- RESERVAS ---")
    print("13. Reserva válida de Ana en la sala")
    r1 = crear_reserva("1010202030", sala, 3)
    print("14. Confirmar y procesar con IVA 19% y descuento 10%")
    ejecutar(r1, "confirmar")
    ejecutar(r1, "procesar", impuesto=0.19, descuento=0.10)
    print("15. Reserva con duración excesiva (50 h)")
    crear_reserva("1010202030", sala, 50)
    print("16. Reserva de un servicio no disponible")
    crear_reserva("80123456", sala_cerrada, 2)
    print("17. Reserva de un cliente que no existe")
    crear_reserva("99999999", sala, 2)
    print("18. Reserva válida de Carlos con el equipo")
    r2 = crear_reserva("80123456", equipo, 24)
    print("19. Procesar sin confirmar")
    ejecutar(r2, "procesar")
    print("20. Cancelar la reserva y luego cancelar otra vez")
    ejecutar(r2, "cancelar")
    ejecutar(r2, "cancelar")
    print("21. Asesoría: descuento inválido (150%) y luego procesar bien")
    r3 = crear_reserva("1010202030", asesoria, 2)
    ejecutar(r3, "confirmar")
    ejecutar(r3, "procesar", descuento=1.5)
    ejecutar(r3, "procesar", impuesto=0.19)

    print("\n--- POLIMORFISMO: cada servicio calcula distinto (2 horas) ---")
    for s in servicios:
        print(f"   {s.describir()}: ${s.calcular_total(2):,.2f}")

    print("\n--- RESUMEN ---")
    print(f"Clientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas: {len(reservas)}")
    registrar("INFO", "=== Programa finalizado ===")
    print("Revisa eventos.log para ver todos los errores y eventos.")


if __name__ == "__main__":
    main()
