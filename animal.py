"""Animal: clase padre ABSTRACTA de todas las especies monitoreadas."""

from abc import ABC, abstractmethod


class Animal(ABC):
    """Reune lo que TODA especie monitoreada comparte, sin importar cual sea.

    Desde la Entrega 3 es abstracta: nadie es 'animal a secas' en la reserva,
    todo animal registrado es de una especie concreta. Heredar de ABC y marcar
    describir() con @abstractmethod hace que Python se niegue a construir un
    Animal suelto y obliga a cada hija a decir como se describe ella.
    """

    ESPECIE = "sin especie"      # cada hija pone su nombre
    EN_PELIGRO = False           # cada hija dice si esta en peligro (art. 2)

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.collar = None       # articulo 4: un animal, un collar a la vez

    # ------------------------------------------------------------------
    # Articulo 1. El formato del codigo es el mismo para toda especie:
    # tres letras mayusculas, un guion y tres digitos (JAG-001).
    # ------------------------------------------------------------------
    @staticmethod
    def codigo_valido(codigo):
        if len(codigo) != 7:
            return False
        if codigo[3] != "-":
            return False
        letras = codigo[0:3]
        digitos = codigo[4:7]
        return letras.isalpha() and letras.isupper() and digitos.isdigit()

    # ------------------------------------------------------------------
    # Articulo 2. La REGLA es la misma para todas las especies: se consulta
    # el estado de conservacion en lugar de escribirlo a mano. Lo que cambia
    # es el DATO, y ese lo pone cada hija en EN_PELIGRO.
    # ------------------------------------------------------------------
    def esta_en_peligro(self):
        # Python busca EN_PELIGRO primero en la instancia, despues en la
        # clase del objeto y por ultimo en Animal. Por eso un Jaguar
        # responde True sin que este metodo sepa que existe el jaguar.
        return self.EN_PELIGRO

    def nombre_especie(self):
        return self.ESPECIE

    # ------------------------------------------------------------------
    # Articulo 4. Llevar o no collar no depende de la especie.
    # ------------------------------------------------------------------
    def tiene_collar(self):
        return self.collar is not None

    # ------------------------------------------------------------------
    # METODO ABSTRACTO. Ninguna hija puede dejar de responderlo.
    #
    # En Python un metodo abstracto SI puede traer cuerpo: lo abstracto
    # obliga a redefinirlo, no prohibe reutilizarlo. Aprovecho eso para
    # dejar aqui la linea de identificacion, que es identica para las cinco
    # especies, y que cada hija la pide con super().describir() en vez de
    # volver a escribirla. Lo que cada una agrega despues -que come, donde
    # vive, como se mueve- es asunto suyo y de nadie mas.
    # ------------------------------------------------------------------
    @abstractmethod
    def describir(self):
        collar = self.collar.codigo if self.tiene_collar() else "sin collar"
        estado = "en peligro" if self.esta_en_peligro() else "sin riesgo"
        return (f"{self.codigo} {self.nombre} | {self.nombre_especie()} "
                f"({estado}) | {collar}")

    def __str__(self):
        # Al delegar en describir(), imprimir un animal muestra siempre la
        # version de su propia especie: eso es polimorfismo.
        return self.describir()
