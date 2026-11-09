"""Guardarrecursos: el personal que patrulla la reserva."""


class Guardarrecursos:
    """Articulo 7. El codigo son dos letras mayusculas, un guion y dos
    digitos (GR-07). Sin un codigo valido no se registra nada a su nombre."""

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    @staticmethod
    def codigo_valido(codigo):
        if len(codigo) != 5:
            return False
        if codigo[2] != "-":
            return False
        letras = codigo[0:2]
        digitos = codigo[3:5]
        return letras.isalpha() and letras.isupper() and digitos.isdigit()

    def __str__(self):
        return f"{self.codigo} {self.nombre}"
