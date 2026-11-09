"""Jaguar: clase hija de Animal."""

from animal import Animal


class Jaguar(Animal):
    """El jaguar es el unico felino grande de la reserva y el que mas
    territorio recorre, por eso su dato propio es el area de campeo."""

    ESPECIE = "jaguar"
    EN_PELIGRO = True            # lo fija el articulo 2 del expediente

    def __init__(self, codigo, nombre, territorio_km2):
        super().__init__(codigo, nombre)      # el padre arma codigo y nombre
        self.territorio_km2 = territorio_km2  # atributo propio

    def es_territorio_amplio(self):
        # Metodo propio: un jaguar con mas de 50 km2 de campeo cruza zonas
        # con frecuencia, asi que sus lecturas hay que mirarlas distinto.
        return self.territorio_km2 >= 50

    # ------------------------------------------------------------------
    # Implementacion propia del metodo abstracto del padre. Pide la linea
    # de identificacion con super() y escribe lo que solo sabe un jaguar.
    # ------------------------------------------------------------------
    def describir(self):
        amplitud = "amplio" if self.es_territorio_amplio() else "reducido"
        return (
            f"{super().describir()}\n"
            f"      Come: carne. Caza pecaries, venados y crias de tapir; "
            f"es el depredador tope de la selva.\n"
            f"      Vive: selva alta y cerrada, siempre a poca distancia "
            f"de una aguada o un rio.\n"
            f"      Se mueve: solo y casi siempre de noche. Patrulla un "
            f"territorio {amplitud} de {self.territorio_km2} km2,\n"
            f"                nada sin problema y trepa a los arboles."
        )
