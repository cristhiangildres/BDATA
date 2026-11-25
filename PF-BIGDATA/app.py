from flask import Flask, render_template, request
from modulos import datos, graficas

app = Flask(__name__)
app.add_template_filter(datos.formatear_numero, "miles")


@app.route("/")
def inicio():
    filas = datos.cargar_museos()
    resumen = datos.resumen_presentacion(filas)
    return render_template("index.html", resumen=resumen)


@app.route("/analisis")
def analisis():
    filas = datos.cargar_museos()
    resumen = datos.resumen_portada(filas)
    anios, totales = datos.totales_por_anio(filas)
    distritos, visitas = datos.ranking(datos.obtener_visitantes(filas, 2025), "Nom_Districte", 10)
    return render_template(
        "analisis.html",
        resumen=resumen,
        grafica_evolucion=graficas.grafica_evolucion(anios, totales),
        grafica_distritos=graficas.grafica_barras(distritos, visitas),
    )


@app.route("/museos")
def museos():
    anio = int(request.args.get("anio", 2025))
    distrito = request.args.get("distrito", "")
    ambito = request.args.get("ambito", "")
    titularidad = request.args.get("titularidad", "")
    orden = request.args.get("orden", "Valor")
    sentido = request.args.get("sentido", "desc")
    vista = request.args.get("vista", "resumen")

    filas = datos.cargar_museos()
    visitantes = datos.obtener_visitantes(filas, anio)
    lista = datos.filtrar(visitantes, distrito, ambito, titularidad)
    lista = datos.ordenar(lista, orden, sentido == "desc")

    nombres, valores = datos.ranking(lista, "Nom_Equipament", 10)
    grafica = graficas.grafica_barras(nombres, valores)

    return render_template(
        "museos.html",
        museos=lista,
        grafica=grafica,
        anios=range(2015, 2026),
        distritos=datos.valores_distintos(visitantes, "Nom_Districte"),
        ambitos=datos.valores_distintos(visitantes, "Ambit"),
        titularidades=datos.valores_distintos(visitantes, "Titularitat"),
        anio=anio,
        distrito=distrito,
        ambito=ambito,
        titularidad=titularidad,
        orden=orden,
        sentido=sentido,
        vista=vista,
    )


if __name__ == "__main__":
    app.run(debug=True)
