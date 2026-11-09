"""GuacamayaRoja: clase hija de Animal."""

from animal import Animal


class GuacamayaRoja(Animal):
    """La guacamaya roja anida en cavidades y su temporada reproductiva es
    el dato que mas condiciona el monitoreo: un nido activo no se perturba."""

    ESPECIE = "guacamaya roja"
    EN_PELIGRO = True

    def __init__(self, codigo, nombre, pichones_en_nido):
        super().__init__(codigo, nombre)
        self.pichones_en_nido = pichones_en_nido     # atributo propio

    def tiene_nidada_activa(self):
        # Metodo propio: con pichones en el nido, acercarse al arbol es
        # suficiente para que la pareja lo abandone.
        return self.pichones_en_nido > 0

    # ------------------------------------------------------------------
    # Implementacion propia del metodo abstracto del padre. Es la unica
    # especie que vuela, asi que su ficha habla de altura y no de rutas.
    # ------------------------------------------------------------------
    def describir(self):
        if self.tiene_nidada_activa():
            nido = (f"Cuida {self.pichones_en_nido} pichones, asi que su "
                    f"arbol no se toca")
        else:
            nido = "Sin nidada este ciclo, la pareja anda suelta"
        return (
            f"{super().describir()}\n"
            f"      Come: semillas, frutos y nueces de palma, que abre con "
            f"el pico como si fuera pinza.\n"
            f"      Vive: en lo alto del dosel. Anida en huecos de arboles "
            f"muertos en pie, que son\n"
            f"            contados en la reserva.\n"
            f"      Se mueve: volando y en pareja, gritando todo el "
            f"camino.\n"
            f"                {nido}."
        )
