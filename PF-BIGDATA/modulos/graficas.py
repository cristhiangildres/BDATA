import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def figura_a_base64(figura):
    memoria = io.BytesIO()
    figura.savefig(memoria, format="png", bbox_inches="tight", transparent=True)
    plt.close(figura)
    return base64.b64encode(memoria.getvalue()).decode("utf-8")


def grafica_evolucion(anios, totales):
    millones = []
    for total in totales:
        millones.append(total / 1000000)

    figura, ejes = plt.subplots(figsize=(9, 4.5))
    ejes.fill_between(anios, millones, color="#8b1e3f", alpha=0.12)
    ejes.vlines(anios, 0, millones, color="#8b1e3f", linestyles="dashed", alpha=0.5)
    ejes.plot(anios, millones, color="#8b1e3f", marker="o")
    ejes.plot(2020, millones[5], color="#c8963e", marker="o", markersize=12)
    ejes.annotate("COVID-19", xy=(2020, millones[5]), xytext=(2020.25, 1.5))
    ejes.set_xticks(anios)
    ejes.set_ylim(0)
    ejes.set_ylabel("Millones de visitantes")
    return figura_a_base64(figura)


def grafica_barras(nombres, valores):
    figura, ejes = plt.subplots(figsize=(9, 5))
    ejes.barh(nombres, valores, color="#8b1e3f")
    ejes.invert_yaxis()
    ejes.set_xlabel("Visitantes")
    return figura_a_base64(figura)
