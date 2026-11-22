# cliente.py
# Clase Cliente: guarda datos personales de forma privada (encapsulación).
from entidad import Entidad
from excepciones import ClienteError


class Cliente(Entidad):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # Se usan los set_ para que los datos se validen al crear el objeto
        self.set_nombre(nombre)
        self.set_documento(documento)
        self.set_correo(correo)
        self.set_telefono(telefono)

    # ----- nombre -----
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if nombre is None or len(str(nombre).strip()) < 3:
            raise ClienteError("El nombre es obligatorio y debe tener al menos 3 letras")
        self.__nombre = str(nombre).strip()

    # ----- documento -----
    def get_documento(self):
        return self.__documento

    def set_documento(self, documento):
        documento = str(documento).strip()
        if not documento.isdigit() or len(documento) < 5:
            raise ClienteError("El documento debe tener solo números (mínimo 5)")
        self.__documento = documento

    # ----- correo -----
    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        correo = str(correo).strip()
        if "@" not in correo or "." not in correo:
            raise ClienteError("El correo no es válido: " + correo)
        self.__correo = correo

    # ----- teléfono -----
    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or not (7 <= len(telefono) <= 10):
            raise ClienteError("El teléfono debe tener entre 7 y 10 números")
        self.__telefono = telefono

    def describir(self):
        return f"Cliente {self.get_nombre()} (doc {self.get_documento()})"
