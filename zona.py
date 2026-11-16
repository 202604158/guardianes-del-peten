"""Zona: una zona registrada de la Reserva de la Biosfera Maya."""


class Zona:
    """Articulo 5. Solo existen tres tipos de zona y solo se aceptan
    lecturas en zonas que esten registradas en el sistema."""

    TIPOS_VALIDOS = ("nucleo", "amortiguamiento", "uso multiple")

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.subzonas = []
        self.animales = []

    def agregar_subzona(self, zona):
        # R5: validar antes de incorporar una zona al mapa.
        if not zona.es_tipo_valido():
            print(f"    RECHAZADA - tipo de zona invalido: {zona.tipo} (R5)")
            return False
        self.subzonas.append(zona)
        return True

    def ubicar(self, animal):
        self.animales.append(animal)

    def mostrar(self, nivel=0):
        print(f"{'  ' * nivel}{self}")
        for subzona in self.subzonas:
            subzona.mostrar(nivel + 1)

    def contar_animales(self):
        total = len(self.animales)
        for subzona in self.subzonas:
            total += subzona.contar_animales()
        return total

    def buscar_sector(self, nombre):
        if self.nombre == nombre:
            return self
        for subzona in self.subzonas:
            encontrado = subzona.buscar_sector(nombre)
            if encontrado is not None:
                return encontrado
        return None

    def es_tipo_valido(self):
        return self.tipo in Zona.TIPOS_VALIDOS

    def es_uso_multiple(self):
        # Lo usa el articulo 6 para decidir si hay acercamiento a comunidad.
        return self.tipo == "uso multiple"

    def __str__(self):
        return f"{self.nombre} [{self.tipo}]"
