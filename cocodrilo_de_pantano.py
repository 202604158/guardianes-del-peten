"""CocodriloDePantano: clase hija de Animal."""

from animal import Animal


class CocodriloDePantano(Animal):
    """Unica especie del expediente que NO esta en peligro. Su dato propio
    es el largo, que es como se estima la edad de un cocodrilo en campo."""

    ESPECIE = "cocodrilo de pantano"
    EN_PELIGRO = False           # articulo 2: el cocodrilo no esta en peligro

    def __init__(self, codigo, nombre, largo_m):
        super().__init__(codigo, nombre)
        self.largo_m = largo_m                       # atributo propio

    def es_adulto(self):
        # Metodo propio: a partir de 2 metros se considera adulto.
        return self.largo_m >= 2.0

    # ------------------------------------------------------------------
    # Implementacion propia del metodo abstracto del padre. Es el unico
    # que vive entre el agua y la orilla, y su ficha lo dice asi.
    # ------------------------------------------------------------------
    def describir(self):
        edad = "adulto" if self.es_adulto() else "juvenil"
        if self.es_adulto():
            presa = "peces, tortugas, aves y mamiferos que bajan a beber"
        else:
            presa = "peces chicos, cangrejos e insectos"
        return (
            f"{super().describir()}\n"
            f"      Come: {presa}.\n"
            f"            Caza al acecho, quieto y casi sumergido.\n"
            f"      Vive: lagunas, pantanos y rios de corriente lenta; "
            f"sale a las orillas de lodo\n"
            f"            a asolearse.\n"
            f"      Se mueve: nadando con la cola, que le sirve de remo.\n"
            f"                Mide {self.largo_m} m, o sea que es un "
            f"ejemplar {edad}."
        )
