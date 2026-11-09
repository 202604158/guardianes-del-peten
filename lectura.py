"""Lectura: una posicion de un animal en un momento dado."""


class Lectura:
    """Dos origenes posibles: la reporta el collar (Anexo C) o la anota un
    guardarrecursos como avistamiento (Anexo D). La hora va en formato
    ISO 'AAAA-MM-DD HH:MM' para poder compararla como texto."""

    def __init__(self, codigo_animal, zona, hora, origen, codigo_guardarrecursos=None):
        self.codigo_animal = codigo_animal
        self.zona = zona
        self.hora = hora
        self.origen = origen                       # "collar" o "avistamiento"
        self.codigo_guardarrecursos = codigo_guardarrecursos

    def __str__(self):
        quien = ""
        if self.codigo_guardarrecursos is not None:
            quien = f" por {self.codigo_guardarrecursos}"
        return f"{self.hora} - {self.zona.nombre} ({self.origen}{quien})"
