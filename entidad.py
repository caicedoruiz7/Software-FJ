# entidad.py
# Clase abstracta general: Cliente, Servicio y Reserva heredan de ella.
from abc import ABC, abstractmethod


class Entidad(ABC):
    contador = 0  # lleva la cuenta para dar un id a cada objeto

    def __init__(self):
        Entidad.contador += 1
        self._id = Entidad.contador  # id único

    def get_id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija debe decir cómo se describe."""
        pass
