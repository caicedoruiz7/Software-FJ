# excepciones.py
# Aquí están las excepciones personalizadas del sistema.

class ErrorFJ(Exception):
    """Excepción base: todas las demás heredan de esta."""
    pass


class ClienteError(ErrorFJ):
    """Se usa cuando los datos de un cliente no son válidos."""
    pass


class ServicioError(ErrorFJ):
    """Se usa cuando los datos de un servicio no son válidos."""
    pass


class ServicioNoDisponibleError(ErrorFJ):
    """Se usa cuando el servicio existe pero no está disponible."""
    pass


class ReservaError(ErrorFJ):
    """Se usa cuando una reserva está mal hecha."""
    pass


class OperacionNoPermitidaError(ErrorFJ):
    """Se usa cuando se hace algo que el estado de la reserva no permite."""
    pass


class CalculoError(ErrorFJ):
    """Se usa cuando un cálculo de costos no tiene sentido."""
    pass
