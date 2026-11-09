"""PavoOcelado: clase hija de Animal. Es la especie que agregue en la
Entrega 1; es endemica de Peten y la peninsula de Yucatan."""

from animal import Animal


class PavoOcelado(Animal):
    """Su dato propio es el mes en que entra en epoca reproductiva, cuando
    los machos se exponen mas y la caza furtiva aumenta."""

    ESPECIE = "pavo ocelado"
    EN_PELIGRO = True            # decision del programa, igual que el art. 2

    MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre")

    def __init__(self, codigo, nombre, mes_apareamiento):
        super().__init__(codigo, nombre)
        self.mes_apareamiento = mes_apareamiento     # atributo propio

    def esta_en_epoca_reproductiva(self, mes):
        # Metodo propio: la epoca abarca el mes de apareamiento y el
        # siguiente, por eso se compara contra los dos.
        siguiente = self.mes_apareamiento % 12 + 1
        return mes == self.mes_apareamiento or mes == siguiente

    # ------------------------------------------------------------------
    # Implementacion propia del metodo abstracto del padre. Al ser la
    # unica especie endemica, su ficha empieza por ahi.
    # ------------------------------------------------------------------
    def describir(self):
        mes = PavoOcelado.MESES[self.mes_apareamiento - 1]
        siguiente = PavoOcelado.MESES[self.mes_apareamiento % 12]
        return (
            f"{super().describir()}\n"
            f"      Come: de todo un poco. Semillas, frutos caidos, hojas "
            f"tiernas e insectos que\n"
            f"            escarba del suelo.\n"
            f"      Vive: solo aqui. Es endemico de Peten y Yucatan; "
            f"prefiere bosque bajo y los\n"
            f"            bordes de las milpas.\n"
            f"      Se mueve: caminando en grupo casi todo el dia; vuela "
            f"tramos cortos y duerme\n"
            f"                en las ramas altas. Su epoca reproductiva va "
            f"de {mes} a {siguiente}."
        )
