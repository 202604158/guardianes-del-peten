"""Cola de alertas en orden de llegada (FIFO)."""


class ColaAlertas:
    def __init__(self):
        self._alertas = []

    def encolar(self, alerta):
        self._alertas.append(alerta)

    def atender(self):
        if self.esta_vacia():
            return None
        return self._alertas.pop(0)

    def siguiente(self):
        if self.esta_vacia():
            return None
        return self._alertas[0]

    def esta_vacia(self):
        return len(self._alertas) == 0

    def tamanio(self):
        return len(self._alertas)
