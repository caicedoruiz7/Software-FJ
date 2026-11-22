# servicios.py
# Clase abstracta Servicio y tres servicios que heredan de ella.
from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioError, CalculoError


class Servicio(Entidad):
    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if nombre is None or str(nombre).strip() == "":
            raise ServicioError("El servicio necesita un nombre")
        # Convertimos la tarifa a número; si falla, encadenamos el error original
        try:
            tarifa = float(tarifa_hora)
        except (ValueError, TypeError) as e:
            raise ServicioError("La tarifa debe ser un número") from e
        if tarifa <= 0:
            raise ServicioError("La tarifa debe ser mayor que cero")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = tarifa
        self._disponible = disponible

    def get_nombre(self):
        return self._nombre

    def get_tarifa_hora(self):
        return self._tarifa_hora

    def esta_disponible(self):
        return self._disponible

    # Métodos que cada servicio hijo DEBE implementar
    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        pass

    # Método con parámetros opcionales (sirve como sobrecarga):
    #   calcular_total(3)             -> sin impuesto ni descuento
    #   calcular_total(3, 0.19)       -> con impuesto
    #   calcular_total(3, 0.19, 0.10) -> con impuesto y descuento
    def calcular_total(self, horas, impuesto=0, descuento=0):
        self.validar_parametros(horas)
        if impuesto < 0 or impuesto > 1:
            raise CalculoError("El impuesto debe estar entre 0 y 1")
        if descuento < 0 or descuento >= 1:
            raise CalculoError("El descuento debe estar entre 0 y 1 (sin incluir 1)")
        costo = self.calcular_costo(horas)
        costo = costo - costo * descuento   # aplica el descuento
        costo = costo + costo * impuesto    # aplica el impuesto
        return round(costo, 2)

    def describir(self):
        return f"Servicio {self._nombre}"


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioError("La capacidad debe ser un entero mayor que cero")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or horas < 1 or horas > 12:
            raise ServicioError("Una sala se reserva de 1 a 12 horas")

    def calcular_costo(self, horas):
        costo = self._tarifa_hora * horas
        if self._capacidad > 20:        # las salas grandes cuestan 10% más
            costo = costo * 1.10
        return costo

    def describir(self):
        return f"Sala {self._nombre} para {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (con depósito fijo)."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, deposito=0, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if tipo_equipo is None or str(tipo_equipo).strip() == "":
            raise ServicioError("Falta el tipo de equipo")
        if deposito < 0:
            raise ServicioError("El depósito no puede ser negativo")
        self._tipo_equipo = tipo_equipo
        self._deposito = deposito

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or horas < 1 or horas > 72:
            raise ServicioError("Un equipo se alquila de 1 a 72 horas")

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas + self._deposito

    def describir(self):
        return f"Equipo {self._nombre} ({self._tipo_equipo})"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías: el nivel senior cuesta 50% más."""

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if especialidad is None or str(especialidad).strip() == "":
            raise ServicioError("Falta la especialidad")
        if nivel not in ("junior", "senior"):
            raise ServicioError("El nivel debe ser 'junior' o 'senior'")
        self._especialidad = especialidad
        self._nivel = nivel

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or horas < 1 or horas > 8:
            raise ServicioError("Una asesoría dura de 1 a 8 horas")

    def calcular_costo(self, horas):
        costo = self._tarifa_hora * horas
        if self._nivel == "senior":
            costo = costo * 1.5
        return costo

    def describir(self):
        return f"Asesoría de {self._especialidad} (nivel {self._nivel})"
