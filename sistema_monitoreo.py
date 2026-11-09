"""SistemaMonitoreo: la clase central. Guarda los arreglos de objetos y
expone un metodo por cada caso de uso del expediente."""

from alerta import Alerta
from animal import Animal
from cambio_bateria import CambioBateria
from collar import Collar
from guardarrecursos import Guardarrecursos
from lectura import Lectura


class SistemaMonitoreo:

    def __init__(self, servicio_sms, codigo_guardarrecursos_de_turno):
        # Los arreglos de objetos del sistema.
        self.zonas = []
        self.animales = []
        self.collares = []
        self.guardarrecursos = []
        self.lecturas = []
        self.alertas = []
        self.cambios_bateria = []
        self._animales_ordenados = False
        # Actor secundario y destinatario de las alertas del articulo 6.
        self.servicio_sms = servicio_sms
        self.codigo_guardarrecursos_de_turno = codigo_guardarrecursos_de_turno

    # ------------------------------------------------------------------
    # Ordenamiento por seleccion y busquedas por codigo o nombre.
    # ------------------------------------------------------------------

    @staticmethod
    def _ordenar_por_seleccion(elementos, clave):
        for posicion in range(len(elementos) - 1):
            menor = posicion
            for candidato in range(posicion + 1, len(elementos)):
                if clave(elementos[candidato]) < clave(elementos[menor]):
                    menor = candidato
            if menor != posicion:
                elementos[posicion], elementos[menor] = (
                    elementos[menor], elementos[posicion])

    def ordenar_alertas(self):
        def nivel(alerta):
            if alerta.prioridad == "alta":
                return 1
            return 2

        # Las horas ISO (AAAA-MM-DD HH:MM) se pueden comparar como texto.
        self._ordenar_por_seleccion(
            self.alertas, lambda alerta: (nivel(alerta), alerta.hora))

    def buscar_animal(self, codigo):
        if not isinstance(codigo, str):
            return None

        # Una alta nueva obliga a ordenar antes de la siguiente busqueda.
        if not self._animales_ordenados:
            self._ordenar_por_seleccion(
                self.animales, lambda animal: animal.codigo)
            self._animales_ordenados = True

        inicio = 0
        fin = len(self.animales) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            animal = self.animales[medio]
            if animal.codigo == codigo:
                return animal
            if animal.codigo < codigo:
                inicio = medio + 1
            else:
                fin = medio - 1
        return None

    def buscar_collar(self, codigo):
        for collar in self.collares:
            if collar.codigo == codigo:
                return collar
        return None

    def buscar_zona(self, nombre):
        # Articulo 5: una zona solo cuenta si esta registrada aqui.
        for zona in self.zonas:
            if zona.nombre == nombre:
                return zona
        return None

    def buscar_guardarrecursos(self, codigo):
        for persona in self.guardarrecursos:
            if persona.codigo == codigo:
                return persona
        return None

    def listar_alertas_pendientes(self):
        # Recorre el arreglo de alertas y devuelve solo las del articulo 8
        # que todavia nadie atendio.
        pendientes = []
        for alerta in self.alertas:
            if alerta.esta_pendiente():
                pendientes.append(alerta)
        return pendientes

    def hora_ultima_lectura(self, codigo_animal):
        # Apoyo del articulo 10: la hora de la ultima lectura guardada.
        ultima = None
        for lectura in self.lecturas:
            if lectura.codigo_animal == codigo_animal:
                if ultima is None or lectura.hora > ultima:
                    ultima = lectura.hora
        return ultima

    # ------------------------------------------------------------------
    # Caso de uso 1 - Registrar animal (Anexo A)
    # ------------------------------------------------------------------

    def registrar_animal(self, animal):
        # Cambio de la Entrega 2: antes este metodo recibia el nombre de la
        # especie y construia el Animal. Ahora recibe el objeto ya armado
        # (un Jaguar, un Tapir, ...), porque la especie dejo de ser un dato
        # que se busca en un catalogo y paso a ser la clase del objeto.

        # Guarda nueva: solo entran objetos que hereden de Animal. Esto
        # reemplaza a la revision del catalogo de especies de la Entrega 1.
        if not isinstance(animal, Animal):
            print(f"    RECHAZADO - '{animal}' no es un Animal: solo se "
                  f"registran objetos de una clase hija de Animal")
            return False

        # Rombo 1: el formato del codigo (articulo 1).
        if not Animal.codigo_valido(animal.codigo):
            print(f"    RECHAZADO - codigo invalido: '{animal.codigo}' no "
                  f"cumple el articulo 1 (formato AAA-999)")
            return False

        # Rombo 2: el codigo ya existe (articulo 1, unicidad).
        # Revisar duplicados sin reordenar la lista durante una guarda.
        if any(registrado.codigo == animal.codigo for registrado in self.animales):
            print(f"    RECHAZADO - codigo repetido: {animal.codigo} ya esta "
                  f"registrado (articulo 1)")
            return False

        # Guardar el animal en la lista.
        self.animales.append(animal)
        self._animales_ordenados = False
        # Cambio de la Entrega 3: describir() ahora devuelve la ficha
        # completa de varias lineas, asi que aqui solo se confirma el alta.
        print(f"    OK - animal registrado: {animal.codigo} "
              f"{animal.nombre} ({animal.nombre_especie()})")
        return True

    # ------------------------------------------------------------------
    # Caso de uso 2 - Asignar collar (Anexo B)
    # ------------------------------------------------------------------

    def asignar_collar(self, codigo_collar, codigo_animal):
        # Buscar el collar y el animal.
        collar = self.buscar_collar(codigo_collar)
        animal = self.buscar_animal(codigo_animal)

        # Rombo 1: existen los dos.
        if collar is None or animal is None:
            print(f"    RECHAZADO - no existen: collar '{codigo_collar}' "
                  f"o animal '{codigo_animal}'")
            return False

        # Rombo 2: el collar esta libre (articulo 4).
        if not collar.esta_libre():
            print(f"    RECHAZADO - el collar {codigo_collar} ya esta "
                  f"asignado a {collar.animal.codigo} (articulo 4)")
            return False

        # Rombo 3: el animal ya tiene collar (articulo 4).
        if animal.tiene_collar():
            print(f"    RECHAZADO - el animal {codigo_animal} ya lleva el "
                  f"collar {animal.collar.codigo} (articulo 4)")
            return False

        # Asignar el collar al animal y confirmar la asignacion.
        collar.animal = animal
        animal.collar = collar
        print(f"    OK - collar {codigo_collar} asignado a {codigo_animal} "
              f"({animal.nombre})")
        return True

    # ------------------------------------------------------------------
    # Caso de uso 3 - Reportar posicion (Anexo C)
    # ------------------------------------------------------------------

    def reportar_posicion(self, codigo_collar, nombre_zona, hora):
        # Recibir del collar su codigo, la zona y la hora. Buscar el collar.
        collar = self.buscar_collar(codigo_collar)

        # Guarda de apoyo: el anexo dice "buscar el collar", y esa busqueda
        # puede fallar; sin collar no hay nada que reportar.
        if collar is None:
            print(f"    RECHAZADA - el collar '{codigo_collar}' no existe")
            return False
        if collar.animal is None:
            print(f"    RECHAZADA - el collar {codigo_collar} no esta "
                  f"asignado a ningun animal (articulo 4)")
            return False

        animal = collar.animal

        # Rombo 1: la bateria es de 10 % o mas (articulo 3).
        if not collar.puede_reportar():
            self.alertas.append(
                Alerta("bateria baja", "media", animal.codigo, hora))
            print(f"    RECHAZADA - bateria {collar.bateria}% < 10% "
                  f"(articulo 3). Alerta 'bateria baja' creada, prioridad media")
            return False

        # Rombo 2: la zona esta registrada (articulo 5).
        zona = self.buscar_zona(nombre_zona)
        if zona is None:
            print(f"    RECHAZADA - la zona '{nombre_zona}' no esta "
                  f"registrada (articulo 5)")
            return False

        # Rombo extra: cronologia de las lecturas (articulo 10, propio).
        ultima = self.hora_ultima_lectura(animal.codigo)
        if ultima is not None and hora < ultima:
            print(f"    RECHAZADA - la hora {hora} es anterior a la ultima "
                  f"lectura de {animal.codigo} ({ultima}) (articulo 10)")
            return False

        # Guardar la lectura.
        self.lecturas.append(
            Lectura(animal.codigo, zona, hora, "collar"))
        print(f"    OK - lectura guardada: {animal.codigo} en "
              f"{zona.nombre} a las {hora}")

        # Rombo 3: animal en peligro y zona de uso multiple (articulo 6).
        if animal.esta_en_peligro() and zona.es_uso_multiple():
            self.alertas.append(
                Alerta("acercamiento a comunidad", "alta", animal.codigo, hora))
            print(f"      ALERTA ALTA - {animal.nombre} ({animal.codigo}) "
                  f"en {zona.nombre} (articulo 6)")
            self.servicio_sms.enviar(
                self.codigo_guardarrecursos_de_turno,
                f"{animal.nombre} en {zona.nombre} a las {hora}")

        return True

    # ------------------------------------------------------------------
    # Caso de uso 4 - Registrar avistamiento (Anexo D)
    # ------------------------------------------------------------------

    def registrar_avistamiento(self, codigo_gr, codigo_animal,
                               nombre_zona, hora):
        # Rombo 1: el codigo del guardarrecursos es valido (articulo 7).
        if not Guardarrecursos.codigo_valido(codigo_gr):
            print(f"    RECHAZADO - codigo invalido: '{codigo_gr}' no cumple "
                  f"el articulo 7 (formato AA-99)")
            return False
        if self.buscar_guardarrecursos(codigo_gr) is None:
            print(f"    RECHAZADO - el guardarrecursos {codigo_gr} no esta "
                  f"registrado (articulo 7)")
            return False

        # Rombo 2: existen el animal y la zona.
        animal = self.buscar_animal(codigo_animal)
        zona = self.buscar_zona(nombre_zona)
        if animal is None or zona is None:
            print(f"    RECHAZADO - no existen: animal '{codigo_animal}' "
                  f"o zona '{nombre_zona}'")
            return False

        # Guardar la lectura como avistamiento. Un avistamiento no pasa por
        # un collar, asi que no le aplica el articulo 3.
        self.lecturas.append(
            Lectura(animal.codigo, zona, hora, "avistamiento", codigo_gr))
        print(f"    OK - avistamiento guardado: {animal.codigo} en "
              f"{zona.nombre} a las {hora} por {codigo_gr}")
        return True

    # ------------------------------------------------------------------
    # Caso de uso 5 - Atender alerta (Anexo E)
    # ------------------------------------------------------------------

    def atender_alerta(self, posicion, codigo_gr):
        # El articulo 7 manda: sin codigo valido no se registra nada a su
        # nombre, y atender una alerta deja el nombre registrado.
        if not Guardarrecursos.codigo_valido(codigo_gr):
            print(f"    RECHAZADO - codigo invalido: '{codigo_gr}' "
                  f"(articulo 7)")
            return False

        # Consultar las alertas pendientes y elegir una.
        if posicion < 0 or posicion >= len(self.alertas):
            print(f"    RECHAZADO - no existe la alerta numero {posicion}")
            return False
        alerta = self.alertas[posicion]

        # Rombo 1: ya fue atendida (articulo 8).
        if not alerta.esta_pendiente():
            print(f"    SIN CAMBIOS - esa alerta ya la atendio "
                  f"{alerta.atendida_por} (articulo 8)")
            return False

        # Marcarla como atendida y guardar quien la atendio.
        alerta.marcar_atendida(codigo_gr)
        print(f"    OK - alerta '{alerta.tipo}' de {alerta.codigo_animal} "
              f"atendida por {codigo_gr}")
        return True

    # ------------------------------------------------------------------
    # Caso de uso 6 - Consultar movimientos (Anexo F)
    # ------------------------------------------------------------------

    def consultar_movimientos(self, codigo_animal):
        # Rombo 1: existe el animal.
        animal = self.buscar_animal(codigo_animal)
        if animal is None:
            print(f"    SIN RESULTADOS - el animal '{codigo_animal}' "
                  f"no existe")
            return []

        # El anexo pide recorrer el arreglo lectura por lectura, no filtrarlo
        # de un solo: por eso el indice y el while.
        movimientos = []
        indice = 0
        while indice < len(self.lecturas):          # ¿quedan lecturas?
            lectura = self.lecturas[indice]         # tomar la siguiente
            if lectura.codigo_animal == codigo_animal:   # ¿es de ese animal?
                movimientos.append(lectura)
            indice = indice + 1

        # Mostrar la lista de movimientos.
        print(f"    Movimientos de {animal.codigo} ({animal.nombre}): "
              f"{len(movimientos)}")
        for lectura in movimientos:
            print(f"      - {lectura}")
        return movimientos

    # ------------------------------------------------------------------
    # Caso de uso 7 - Registrar cambio de bateria (el caso de uso escondido)
    # ------------------------------------------------------------------

    def registrar_cambio_bateria(self, codigo_collar, codigo_gr,
                                 nivel_nuevo, hora):
        # Rombo 1: el codigo del guardarrecursos es valido (articulo 7).
        if not Guardarrecursos.codigo_valido(codigo_gr):
            print(f"    RECHAZADO - codigo invalido: '{codigo_gr}' "
                  f"(articulo 7)")
            return False
        if self.buscar_guardarrecursos(codigo_gr) is None:
            print(f"    RECHAZADO - el guardarrecursos {codigo_gr} no esta "
                  f"registrado (articulo 7)")
            return False

        # Rombo 2: existe el collar.
        collar = self.buscar_collar(codigo_collar)
        if collar is None:
            print(f"    RECHAZADO - el collar '{codigo_collar}' no existe")
            return False

        # Rombo 3: el nivel nuevo cumple el articulo 3 (articulo 9).
        if not Collar.nivel_valido(nivel_nuevo):
            print(f"    RECHAZADO - nivel {nivel_nuevo} invalido: debe estar "
                  f"entre 10 y 100 (articulos 3 y 9)")
            return False

        # Actualizar el collar y dejar el cambio anotado en la bitacora.
        nivel_anterior = collar.bateria
        collar.bateria = nivel_nuevo
        self.cambios_bateria.append(
            CambioBateria(collar.codigo, codigo_gr,
                          nivel_anterior, nivel_nuevo, hora))
        print(f"    OK - collar {codigo_collar}: {nivel_anterior}% -> "
              f"{nivel_nuevo}% registrado por {codigo_gr} a las {hora}")
        return True
