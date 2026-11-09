"""Collar: un collar GPS asignable a un animal."""


class Collar:
    """Articulo 3. La bateria va de 0 a 100 y con menos de 10 el collar
    no puede reportar. Articulo 4: un collar se asigna a un solo animal."""

    BATERIA_MINIMA = 10

    def __init__(self, codigo, bateria):
        self.codigo = codigo
        self.bateria = bateria
        self.animal = None

    def puede_reportar(self):
        # Articulo 3: esta es la guarda que usa Reportar posicion.
        return self.bateria >= Collar.BATERIA_MINIMA

    def esta_libre(self):
        # Articulo 4: libre significa que ningun animal lo lleva puesto.
        return self.animal is None

    @staticmethod
    def nivel_valido(nivel):
        # Articulo 3 aplicado al articulo 9: el nivel nuevo tras un cambio
        # de bateria tiene que caer en el rango y dejar al collar operativo.
        if not isinstance(nivel, int):
            return False
        return Collar.BATERIA_MINIMA <= nivel <= 100

    def __str__(self):
        animal = self.animal.codigo if self.animal is not None else "libre"
        return f"{self.codigo} - bateria {self.bateria}% - {animal}"
