"""CambioBateria: la bitacora de los cambios de bateria de los collares."""


class CambioBateria:
    """Articulo 9. Existe como clase propia justamente por el caso de
    Tziquin: el cambio se hizo pero no quedo registrado en ninguna parte,
    y la oficina siguio una semana creyendo que el collar estaba muerto."""

    def __init__(self, codigo_collar, codigo_guardarrecursos,
                 nivel_anterior, nivel_nuevo, hora):
        self.codigo_collar = codigo_collar
        self.codigo_guardarrecursos = codigo_guardarrecursos
        self.nivel_anterior = nivel_anterior
        self.nivel_nuevo = nivel_nuevo
        self.hora = hora

    def __str__(self):
        return (f"{self.hora} - collar {self.codigo_collar}: "
                f"{self.nivel_anterior}% -> {self.nivel_nuevo}% "
                f"(por {self.codigo_guardarrecursos})")
