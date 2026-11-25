# Museus BCN: dashboard de los museos de Barcelona

Dashboard web hecho con **Flask** que presenta y analiza los datos de los museos y centros de exposiciones de Barcelona entre **2015 y 2025**: cuántos hay, de qué tipo son, dónde están y cuánta gente los visita.

Proyecto final BIGDATA Desenvolupament d'Aplicacions Web.

- **Web publicada:** _(https://cristhiangildres.pythonanywhere.com/)_
- **Repositorio:** _(https://github.com/cristhiangildres/BDATA/tree/dfc8057f485bb1a73f6a07e2664b4febf8c852af/PF-BIGDATA)_

---

## 1. Los datos

- **Fuente:**
[Open Data BCN: Dades de museus i exposicions de la ciutat de Barcelona](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/dades-museus-exposicions)
- **Autor:** Institut de Cultura, Ajuntament de Barcelona
- **Licencia:** CC BY 4.0 (se puede usar citando la fuente)
- **Archivos:** 11 CSV, uno por año, guardados en `data/museos/` con los nombres `museos_BCN_2015.csv` … `museos_BCN_2025.csv`.

### Cómo están organizados

Los CSV no tienen una columna "visitantes". Cada museo ocupa **varias filas, una por cada dato** que se mide de él. La columna `Indicador` dice qué se mide y la columna `Valor` dice cuánto.

Ejemplo: así aparece **CosmoCaixa** en el CSV de 2025 (4 filas, una por indicador):

| Indicador                       | Qué mide                          | Valor     |
| ------------------------------- | --------------------------------- | --------- |
| `Visitants`                     | Visitantes totales del año        | 1.190.965 |
| `Visites_Exposicions_Temporals` | Visitas a exposiciones temporales | 65.982    |
| `Num_Exposicions_Temporals`     | Número de exposiciones temporales | 2         |
| `Fons_Colleccio`                | Piezas de la colección            | 9.240     |

El resto de columnas (año, nombre, distrito, barrio, titularidad, ámbito, coordenadas…) se repiten igual en las 4 filas del mismo museo.

Por eso, para saber cuántos visitantes tiene un museo, hay que quedarse con su fila de `Visitants` y leer el número de la columna `Valor`.

### Detalle de los CSV

Características de los 11 archivos y cómo se tienen en cuenta en el código:

| Qué se comprobó    | Resultado                            | Qué se hizo en el código            |
| ------------------ | ------------------------------------ | ----------------------------------- |
| Columnas           | Mismas 16 columnas en los 11 años    | Se juntan todos en una sola lista   |
| Codificación       | UTF-8                                | Se abren con `encoding="utf-8"`     |
| Separador          | Comas                                | Se leen con `csv.DictReader`        |
| Columna `Valor`    | Todos son números enteros            | Se convierten con `int()`           |
| Notas              | Espacios y saltos de línea sobrantes | Se limpian con `.strip()`           |
| Nombres de archivo | Dos formatos distintos en la web     | Renombrados a `museos_BCN_AAAA.csv` |

En total hay **1.652 filas** entre los 11 años.

---

## 2. `app.py`: las rutas

Solo contiene las rutas (requisito 6): recoge lo que pide el usuario, llama a `modulos/` y envía el resultado a una plantilla con `render_template`.

| Ruta        | Función      | Qué muestra                                     | Plantilla       |
| ----------- | ------------ | ----------------------------------------------- | --------------- |
| `/`         | `inicio()`   | Presentación de los museos de Barcelona         | `index.html`    |
| `/analisis` | `analisis()` | Cifras de visitantes, 2 gráficas y conclusiones | `analisis.html` |
| `/museos`   | `museos()`   | Tabla con filtros, orden y gráfica del top 10   | `museos.html`   |

- `app.add_template_filter(datos.formatear_numero, "miles")` permite escribir `{{ numero|miles }}` en las plantillas: `5027015` → `5.027.015`.
- `app.run(debug=True)` solo arranca el servidor en local. En PythonAnywhere se arranca desde el archivo WSGI.

### `inicio()`

Carga los datos, pide `datos.resumen_presentacion()` y envía el resultado a `index.html`.

### `analisis()`

Pide a `datos.py` las cifras (`resumen_portada`), los totales por año y el ranking de distritos de 2025. Con ellos crea las 2 gráficas en `graficas.py` y lo envía todo a `analisis.html`.

### `museos()`

Lee los filtros de la URL con `request.args.get(nombre, por_defecto)`. El formulario usa **GET**, así que la URL refleja lo elegido: `/museos?anio=2020&distrito=Gràcia`.

| Parámetro                           | Qué indica            | Por defecto          |
| ----------------------------------- | --------------------- | -------------------- |
| `anio`                              | Año                   | `2025`               |
| `distrito`, `ambito`, `titularidad` | Filtros               | `""` (sin filtro)    |
| `orden`                             | Columna para ordenar  | `Valor` (visitantes) |
| `sentido`                           | `desc` o `asc`        | `desc`               |
| `vista`                             | `resumen` o `detalle` | `resumen`            |

Después se queda con los visitantes del año, filtra, ordena y crea la gráfica del top 10 con la lista ya filtrada. Envía también los filtros elegidos para que el formulario los recuerde.

---

## Documentación

La explicación del resto del código está en la carpeta `docs/`:

- [Backend: `datos.py` y `graficas.py`](docs/BACKEND.md)
- [Frontend: plantillas HTML y diseño](docs/FRONTEND.md)
