"""Alerta: un aviso que el sistema genera y alguien debe atender."""


class Alerta:
    """Articulo 8. Toda alerta nace pendiente, se atiende una sola vez y
    queda registrado que guardarrecursos la atendio. Esto resuelve lo que
    cuenta el expediente: dos guardarrecursos salieron por la misma alerta."""

    def __init__(self, tipo, prioridad, codigo_animal, hora):
        self.tipo = tipo
        self.prioridad = prioridad                 # "alta" o "media"
        self.codigo_animal = codigo_animal
        self.hora = hora
        self.atendida = False                      # nace pendiente
        self.atendida_por = None

    def esta_pendiente(self):
        return not self.atendida

    def marcar_atendida(self, codigo_guardarrecursos):
        # Articulo 8: el metodo no pregunta, solo actua. Quien decide si se
        # puede atender es atender_alerta(), que ya reviso esta_pendiente().
        self.atendida = True
        self.atendida_por = codigo_guardarrecursos

    def __str__(self):
        estado = "pendiente"
        if self.atendida:
            estado = f"atendida por {self.atendida_por}"
        return f"[{self.prioridad}] {self.tipo} - {self.codigo_animal} - {self.hora} - {estado}"
