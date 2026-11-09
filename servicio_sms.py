"""ServicioSMS: el servicio externo de mensajes de texto contratado."""


class ServicioSMS:
    """Actor secundario. El sistema lo invoca, nunca al reves. Lo pidio el
    Ing. Pop: que las alertas no dependan de que alguien vea un WhatsApp."""

    def __init__(self):
        self.mensajes_enviados = []

    def enviar(self, codigo_guardarrecursos, texto):
        self.mensajes_enviados.append((codigo_guardarrecursos, texto))
        print(f"      [SMS -> {codigo_guardarrecursos}] {texto}")
        return True
