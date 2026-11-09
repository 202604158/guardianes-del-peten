"""Zona: una zona registrada de la Reserva de la Biosfera Maya."""


class Zona:
    """Articulo 5. Solo existen tres tipos de zona y solo se aceptan
    lecturas en zonas que esten registradas en el sistema."""

    TIPOS_VALIDOS = ("nucleo", "amortiguamiento", "uso multiple")

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def es_tipo_valido(self):
        return self.tipo in Zona.TIPOS_VALIDOS

    def es_uso_multiple(self):
        # Lo usa el articulo 6 para decidir si hay acercamiento a comunidad.
        return self.tipo == "uso multiple"

    def __str__(self):
        return f"{self.nombre} [{self.tipo}]"
