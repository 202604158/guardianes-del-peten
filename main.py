"""
Guardianes del Peten - Entrega 4 (ordenar y buscar)
Sistema de monitoreo de fauna de la Reserva de la Biosfera Maya

Nombre completo: Julio Cesar Carias Vargas
Carne: 202604158
Grupo: IS24-FP2
Fecha: 8 de noviembre de 2026

Se ordenan cinco alertas y se buscan tres codigos de animal. Tambien se
ejecutan los siete casos de uso y la demostracion de polimorfismo de la
entrega anterior.
"""

from alerta import Alerta
from animal import Animal
from zona import Zona
from collar import Collar
from guardarrecursos import Guardarrecursos
from servicio_sms import ServicioSMS
from sistema_monitoreo import SistemaMonitoreo

# Las cinco clases hijas, cada una en su propio modulo.
from jaguar import Jaguar
from tapir import Tapir
from guacamaya_roja import GuacamayaRoja
from cocodrilo_de_pantano import CocodriloDePantano
from pavo_ocelado import PavoOcelado


def titulo(texto):
    print()
    print("=" * 74)
    print(texto)
    print("=" * 74)


def paso(texto):
    print(f"\n  > {texto}")


def probar_entrega_4(sistema):
    titulo("ENTREGA 4  ORDENAR ALERTAS POR SELECCION")
    # Lista de prueba separada para no alterar las alertas del CU-5.
    prueba_alertas = SistemaMonitoreo(sistema.servicio_sms, "GR-07")
    prueba_alertas.alertas.extend([
        Alerta("bateria baja", "media", "TAP-014", "2026-11-08 18:45"),
        Alerta("acercamiento a comunidad", "alta", "JAG-001", "2026-11-08 18:30"),
        Alerta("bateria baja", "media", "COC-022", "2026-11-08 07:15"),
        Alerta("acercamiento a comunidad", "alta", "GUA-003", "2026-11-08 09:05"),
        Alerta("bateria baja", "media", "PAV-005", "2026-11-08 12:20"),
    ])

    print("  Antes de ordenar:")
    for alerta in prueba_alertas.alertas:
        print(f"    {alerta}")

    prueba_alertas.ordenar_alertas()
    print("\n  Despues de ordenar:")
    for alerta in prueba_alertas.alertas:
        print(f"    {alerta}")

    titulo("ENTREGA 4  BUSCAR ANIMALES POR CODIGO")
    print("  Orden de registro:", ", ".join(animal.codigo for animal in sistema.animales))
    primero = sistema.buscar_animal("COC-022")
    print("  Orden por codigo: ", ", ".join(animal.codigo for animal in sistema.animales))
    print(f"\n  Primer codigo (COC-022) -> {primero}")
    print(f"\n  Ultimo codigo (TAP-014) -> {sistema.buscar_animal('TAP-014')}")
    print(f"\n  Codigo inexistente (ZZZ-999) -> {sistema.buscar_animal('ZZZ-999')}")


# ----------------------------------------------------------------------
# Carga inicial de la reserva
# ----------------------------------------------------------------------

sms = ServicioSMS()
sistema = SistemaMonitoreo(sms, "GR-07")

sistema.zonas.append(Zona("Laguna del Tigre", "nucleo"))
sistema.zonas.append(Zona("Mirador-Rio Azul", "nucleo"))
sistema.zonas.append(Zona("Carmelita", "amortiguamiento"))
sistema.zonas.append(Zona("Uaxactun", "uso multiple"))
sistema.zonas.append(Zona("San Andres", "uso multiple"))

sistema.collares.append(Collar("COL-01", 85))
sistema.collares.append(Collar("COL-02", 8))
sistema.collares.append(Collar("COL-03", 60))
sistema.collares.append(Collar("COL-04", 45))

sistema.guardarrecursos.append(Guardarrecursos("GR-07", "Mateo Chayax"))
sistema.guardarrecursos.append(Guardarrecursos("GR-12", "Ana Caal"))

rechazos = 0

titulo("CARGA INICIAL")
print(f"  Zonas: {len(sistema.zonas)} | Collares: {len(sistema.collares)} | "
      f"Guardarrecursos: {len(sistema.guardarrecursos)}")

# ----------------------------------------------------------------------
# CU-1 - Registrar animal: ahora se construye un objeto de la clase hija
# ----------------------------------------------------------------------

titulo("CU-1  REGISTRAR ANIMAL  (una clase hija por especie)")

balam = Jaguar("JAG-001", "Balam", 65)
tziquin = Tapir("TAP-014", "Tziquin", "nocturno")
kanil = GuacamayaRoja("GUA-003", "Kanil", 2)
ixchel = CocodriloDePantano("COC-022", "Ixchel", 2.4)
kukul = PavoOcelado("PAV-005", "Kukul", 3)

paso("Camino feliz: se registra un animal de cada especie")
for animal in [balam, tziquin, kanil, ixchel, kukul]:
    sistema.registrar_animal(animal)

paso("Alterno 1: formato de codigo invalido (articulo 1)")
if not sistema.registrar_animal(Jaguar("jag001", "Balam", 65)):
    rechazos += 1

paso("Alterno 2: codigo repetido (articulo 1)")
if not sistema.registrar_animal(Jaguar("JAG-001", "Otro jaguar", 30)):
    rechazos += 1

paso("Alterno 3: el objeto no hereda de Animal")
if not sistema.registrar_animal("JAG-999"):
    rechazos += 1

probar_entrega_4(sistema)

# ----------------------------------------------------------------------
# CU-2 - Asignar collar
# ----------------------------------------------------------------------

titulo("CU-2  ASIGNAR COLLAR")

paso("Camino feliz: tres collares a tres animales")
sistema.asignar_collar("COL-01", "JAG-001")
sistema.asignar_collar("COL-02", "TAP-014")
sistema.asignar_collar("COL-03", "GUA-003")

paso("Alterno 1: el collar ya esta ocupado (articulo 4)")
if not sistema.asignar_collar("COL-01", "COC-022"):
    rechazos += 1

paso("Alterno 2: el animal ya lleva collar (articulo 4)")
if not sistema.asignar_collar("COL-04", "JAG-001"):
    rechazos += 1

# ----------------------------------------------------------------------
# El ciclo que no pregunta: un solo for, sin un solo if por especie
# ----------------------------------------------------------------------

titulo("EL CICLO QUE NO PREGUNTA  (polimorfismo)")
print("  Un unico for recorre la lista y llama describir(). No hay ningun")
print("  if por especie ni isinstance: cada objeto responde con la version")
print("  de su propia clase.")

for animal in sistema.animales:
    print(f"\n  {animal.describir()}")

# ----------------------------------------------------------------------
# Lo que ya no se puede hacer: construir un Animal a secas
# ----------------------------------------------------------------------

titulo("INTENTO DE CREAR UN Animal DIRECTO")
print("  Animal es abstracta y describir() es su metodo abstracto, asi que")
print("  Python se niega a construir un animal sin especie.")

paso("Se intenta: Animal(\"ANI-000\", \"generico\")")
try:
    generico = Animal("ANI-000", "generico")
    print(f"    Se creo el objeto: {generico}")
except TypeError as error:
    print(f"    {type(error).__name__}: {error}")
    rechazos += 1

# ----------------------------------------------------------------------
# CU-3 - Reportar posicion
# ----------------------------------------------------------------------

titulo("CU-3  REPORTAR POSICION")

paso("Camino feliz: lectura normal en zona de amortiguamiento")
sistema.reportar_posicion("COL-01", "Carmelita", "2026-10-15 06:40")

paso("Camino feliz con articulo 6: jaguar en zona de uso multiple")
sistema.reportar_posicion("COL-01", "Uaxactun", "2026-10-15 18:30")

paso("Alterno 1: bateria por debajo del 10 % (articulo 3)")
if not sistema.reportar_posicion("COL-02", "Carmelita", "2026-10-15 19:00"):
    rechazos += 1

paso("Alterno 2: zona no registrada (articulo 5)")
if not sistema.reportar_posicion("COL-03", "El Remate", "2026-10-15 19:10"):
    rechazos += 1

paso("Alterno 3: lectura con hora anterior a la ultima (articulo 10)")
if not sistema.reportar_posicion("COL-01", "Carmelita", "2026-10-15 05:00"):
    rechazos += 1

# ----------------------------------------------------------------------
# CU-4 - Registrar avistamiento
# ----------------------------------------------------------------------

titulo("CU-4  REGISTRAR AVISTAMIENTO")

paso("Camino feliz: Don Mateo ve al cocodrilo, que no lleva collar")
sistema.registrar_avistamiento("GR-07", "COC-022", "Laguna del Tigre",
                               "2026-10-16 09:15")

paso("Alterno 1: codigo de guardarrecursos invalido (articulo 7)")
if not sistema.registrar_avistamiento("gr7", "COC-022", "Laguna del Tigre",
                                      "2026-10-16 09:20"):
    rechazos += 1

# ----------------------------------------------------------------------
# CU-5 - Atender alerta
# ----------------------------------------------------------------------

titulo("CU-5  ATENDER ALERTA")

paso("Alertas pendientes en el sistema")
for i in range(len(sistema.alertas)):
    if sistema.alertas[i].esta_pendiente():
        print(f"      indice {i}: {sistema.alertas[i]}")

posicion_alta = -1
for i in range(len(sistema.alertas)):
    if sistema.alertas[i].prioridad == "alta":
        posicion_alta = i

paso("Camino feliz: GR-07 atiende la alerta de acercamiento")
sistema.atender_alerta(posicion_alta, "GR-07")

paso("Alterno 1: otro guardarrecursos intenta atender la misma (articulo 8)")
if not sistema.atender_alerta(posicion_alta, "GR-12"):
    rechazos += 1

# ----------------------------------------------------------------------
# CU-6 - Consultar movimientos
# ----------------------------------------------------------------------

titulo("CU-6  CONSULTAR MOVIMIENTOS")

paso("Camino feliz: la historia de Balam, zona por zona")
sistema.consultar_movimientos("JAG-001")

paso("Alterno 1: el animal no existe")
sistema.consultar_movimientos("ZZZ-999")

# ----------------------------------------------------------------------
# CU-7 - Registrar cambio de bateria (el caso de uso escondido)
# ----------------------------------------------------------------------

titulo("CU-7  REGISTRAR CAMBIO DE BATERIA  (caso de uso escondido)")

paso("Alterno 1: nivel nuevo por debajo del minimo (articulos 3 y 9)")
if not sistema.registrar_cambio_bateria("COL-02", "GR-07", 5,
                                        "2026-10-17 11:00"):
    rechazos += 1

paso("Camino feliz: Don Mateo cambia la bateria del collar de Tziquin")
sistema.registrar_cambio_bateria("COL-02", "GR-07", 95, "2026-10-17 11:10")

paso("Y ahora ese collar si puede reportar (articulo 3)")
sistema.reportar_posicion("COL-02", "San Andres", "2026-10-17 12:00")

# ----------------------------------------------------------------------
# Resumen
# ----------------------------------------------------------------------

titulo("RESUMEN DEL ESTADO DEL SISTEMA")
print(f"  Animales registrados ....... {len(sistema.animales)}")
print(f"  Lecturas guardadas ......... {len(sistema.lecturas)}")
print(f"  Alertas generadas .......... {len(sistema.alertas)}")
print(f"  Cambios de bateria ......... {len(sistema.cambios_bateria)}")
print(f"  Mensajes SMS enviados ...... {len(sms.mensajes_enviados)}")
print(f"  Intentos rechazados ........ {rechazos}")

print("\n  Especies registradas (la clase del objeto ES la especie):")
for animal in sistema.animales:
    print(f"    [{type(animal).__name__}] {animal.codigo} {animal.nombre}")
print()
