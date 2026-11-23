"""Pila de anotaciones de patrulla (LIFO)."""


class BitacoraPatrulla:
    def __init__(self):
        self._entradas = []

    def registrar(self, entrada):
        self._entradas.append(entrada)

    def deshacer(self):
        if self.esta_vacia():
            return None
        return self._entradas.pop()

    def ultima(self):
        if self.esta_vacia():
            return None
        return self._entradas[-1]

    def esta_vacia(self):
        return len(self._entradas) == 0

    def mostrar(self):
        for indice in range(len(self._entradas) - 1, -1, -1):
            print(self._entradas[indice])
