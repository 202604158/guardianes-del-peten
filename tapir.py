"""Tapir: clase hija de Animal."""

from animal import Animal


class Tapir(Animal):
    """El tapir es de habitos nocturnos, asi que su dato propio es la franja
    horaria en que se le espera activo: sirve para interpretar sus lecturas."""

    ESPECIE = "tapir"
    EN_PELIGRO = True

    HORARIOS = {"nocturno": (18, 6), "crepuscular": (16, 20)}

    def __init__(self, codigo, nombre, horario_actividad):
        super().__init__(codigo, nombre)
        self.horario_actividad = horario_actividad   # atributo propio

    def esta_activo_a_la_hora(self, hora):
        # Metodo propio. El rango nocturno cruza la medianoche, por eso se
        # trata aparte en lugar de comparar con un solo 'entre'.
        inicio, fin = Tapir.HORARIOS[self.horario_actividad]
        if inicio <= fin:
            return inicio <= hora <= fin
        return hora >= inicio or hora <= fin

    # ------------------------------------------------------------------
    # Implementacion propia del metodo abstracto del padre.
    # ------------------------------------------------------------------
    def describir(self):
        inicio, fin = Tapir.HORARIOS[self.horario_actividad]
        return (
            f"{super().describir()}\n"
            f"      Come: solo plantas. Ramonea hojas, brotes tiernos y "
            f"frutos caidos, y asi dispersa\n"
            f"            semillas por toda la selva.\n"
            f"      Vive: selva humeda y humedales; no se aleja de las "
            f"aguadas, donde se refresca.\n"
            f"      Se mueve: a pie y siempre por las mismas veredas, que "
            f"abre a fuerza de repetirlas.\n"
            f"                Es {self.horario_actividad}: anda de las "
            f"{inicio} a las {fin} horas, y nada bien."
        )
