import os
import csv

CARPETA_MUSEOS = os.path.join(os.path.dirname(__file__), "..", "data", "museos")


def cargar_museos():
    filas = []

    for año in range(2015, 2026):
        nombre_archivo = "museos_BCN_" + str(año) + ".csv"
        ruta = os.path.join(CARPETA_MUSEOS, nombre_archivo)

        archivo = open(ruta, encoding="utf-8")
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["Any"] = int(fila["Any"])
            fila["Valor"] = int(fila["Valor"])

            fila["Notes_Dades"] = fila["Notes_Dades"].strip()
            fila["Notes_Equipament"] = fila["Notes_Equipament"].strip()

            filas.append(fila)

        archivo.close()

    return filas


def obtener_visitantes(filas, año):
    resultado = []
    for fila in filas:
        if fila["Indicador"] == "Visitants" and fila["Any"] == año:
            resultado.append(fila)
    return resultado


def filtrar(filas, distrito, ambito, titularidad):
    resultado = []
    for fila in filas:
        if distrito == "" or fila["Nom_Districte"] == distrito:
            if ambito == "" or fila["Ambit"] == ambito:
                if titularidad == "" or fila["Titularitat"] == titularidad:
                    resultado.append(fila)
    return resultado


def ordenar(filas, columna, descendente):
    return sorted(filas, key=lambda fila: fila[columna], reverse=descendente)


def valores_distintos(filas, columna):
    valores = []
    for fila in filas:
        if fila[columna] not in valores:
            valores.append(fila[columna])
    valores.sort()
    return valores


def total_visitantes(filas):
    total = 0
    for fila in filas:
        total = total + fila["Valor"]
    return total


def porcentaje(parte, total):
    return round(parte * 100 / total, 1)


def formatear_numero(numero):
    texto = "{:,}".format(numero)
    return texto.replace(",", ".")


def resumen_portada(filas):
    visitantes_2019 = obtener_visitantes(filas, 2019)
    visitantes_2020 = obtener_visitantes(filas, 2020)
    visitantes_2025 = obtener_visitantes(filas, 2025)

    total_2019 = total_visitantes(visitantes_2019)
    total_2020 = total_visitantes(visitantes_2020)
    total_2025 = total_visitantes(visitantes_2025)

    top3 = ordenar(visitantes_2025, "Valor", True)[:3]
    total_top3 = total_visitantes(top3)

    distritos, visitas = ranking(visitantes_2025, "Nom_Districte", 2)

    resumen = {
        "total_2025": total_2025,
        "num_museos_2025": len(visitantes_2025),
        "top3": top3,
        "porcentaje_top3": porcentaje(total_top3, total_2025),
        "caida_covid": porcentaje(total_2019 - total_2020, total_2019),
        "recuperacion": porcentaje(total_2025 - total_2019, total_2019),
        "distritos_top2": distritos,
        "porcentaje_distritos_top2": porcentaje(visitas[0] + visitas[1], total_2025),
    }
    return resumen


def totales_por_anio(filas):
    anios = []
    totales = []
    for anio in range(2015, 2026):
        visitantes = obtener_visitantes(filas, anio)
        anios.append(anio)
        totales.append(total_visitantes(visitantes))
    return anios, totales


def ranking(filas, columna, cantidad):
    sumas = {}
    for fila in filas:
        nombre = fila[columna]
        if nombre not in sumas:
            sumas[nombre] = 0
        sumas[nombre] = sumas[nombre] + fila["Valor"]

    pares = sorted(sumas.items(), key=lambda par: par[1], reverse=True)[:cantidad]

    nombres = []
    valores = []
    for nombre, valor in pares:
        nombres.append(nombre)
        valores.append(valor)
    return nombres, valores


def contar(filas, columna):
    cuentas = {}
    for fila in filas:
        nombre = fila[columna]
        if nombre not in cuentas:
            cuentas[nombre] = 0
        cuentas[nombre] = cuentas[nombre] + 1
    return cuentas


def total_indicador(filas, indicador, anio):
    total = 0
    for fila in filas:
        if fila["Indicador"] == indicador and fila["Any"] == anio:
            total = total + fila["Valor"]
    return total


def resumen_presentacion(filas):
    museos = obtener_visitantes(filas, 2025)
    ambitos = contar(museos, "Ambit")
    distritos = contar(museos, "Nom_Districte")

    ejemplos = {}
    for ambito in ambitos:
        lista = filtrar(museos, "", ambito, "")
        lista = ordenar(lista, "Valor", True)
        nombres = []
        for museo in lista[:4]:
            nombres.append(museo["Nom_Equipament"])
        ejemplos[ambito] = nombres

    resumen = {
        "num_museos": len(museos),
        "num_distritos": len(distritos),
        "exposiciones": total_indicador(filas, "Num_Exposicions_Temporals", 2025),
        "piezas": total_indicador(filas, "Fons_Colleccio", 2025),
        "ambitos": ambitos,
        "ejemplos": ejemplos,
        "museos_ciutat_vella": distritos["Ciutat Vella"],
        "titularidades": contar(museos, "Titularitat"),
    }
    return resumen
