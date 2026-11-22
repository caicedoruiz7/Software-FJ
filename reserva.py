# reserva.py
# Clase Reserva: une un cliente, un servicio, la duración y el estado.
from entidad import Entidad
from excepciones import (ReservaError, ServicioError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, ErrorFJ)
from registro import registrar


class Reserva(Entidad):
    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if cliente is None or servicio is None:
            raise ReservaError("La reserva necesita un cliente y un servicio")
        if not servicio.esta_disponible():
            raise ServicioNoDisponibleError(f"{servicio.get_nombre()} no está disponible")
        # Validamos las horas; si falla, encadenamos el error del servicio
        try:
            servicio.validar_parametros(horas)
        except ServicioError as e:
            raise ReservaError("Duración no válida para esta reserva") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        self._costo = None

    def get_estado(self):
        return self._estado

    def get_costo(self):
        return self._costo

    def confirmar(self):
        # Solo se puede confirmar una reserva pendiente
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}")
        self._estado = "CONFIRMADA"
        registrar("INFO", f"Reserva {self.get_id()} confirmada")

    def cancelar(self):
        try:
            if self._estado in ("CANCELADA", "PROCESADA"):
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva en estado {self._estado}")
            self._estado = "CANCELADA"
            registrar("INFO", f"Reserva {self.get_id()} cancelada")
        except OperacionNoPermitidaError as e:
            registrar("ERROR", str(e))
            raise  # volvemos a lanzar el error para que el programa principal lo sepa
        finally:
            registrar("DEBUG", f"Terminó el intento de cancelar la reserva {self.get_id()}")

    def procesar(self, impuesto=0, descuento=0):
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError("Solo se procesan reservas confirmadas")
            total = self._servicio.calcular_total(self._horas, impuesto, descuento)
        except OperacionNoPermitidaError as e:
            registrar("ERROR", str(e))
            raise
        except ErrorFJ as e:
            registrar("ERROR", f"Error al procesar la reserva {self.get_id()}: {e}")
            raise ReservaError("No se pudo procesar la reserva") from e
        else:
            # Esto solo se ejecuta si NO hubo errores
            self._costo = total
            self._estado = "PROCESADA"
            registrar("INFO", f"Reserva {self.get_id()} procesada. Total: {total}")
            return total
        finally:
            registrar("DEBUG", f"Terminó el intento de procesar la reserva {self.get_id()}")

    def describir(self):
        texto = (f"Reserva {self.get_id()} [{self._estado}] - "
                 f"{self._cliente.get_nombre()} - {self._servicio.get_nombre()} ({self._horas} h)")
        if self._costo is not None:
            texto += f" - Total: ${self._costo:,.2f}"
        return texto
