# Backend: `datos.py` y `graficas.py`

La lógica de la aplicación está en la carpeta `modulos/`, separada de las rutas de `app.py` (requisito 6). No usa pandas: los CSV se leen con el módulo `csv` de Python y se trabajan con listas, diccionarios y bucles.

---

## `datos.py`: leer y calcular

| Función                                         | Qué hace                                                  |
| ----------------------------------------------- | --------------------------------------------------------- |
| `cargar_museos()`                               | Lee los 11 CSV y devuelve una lista con las 1.652 filas   |
| `obtener_visitantes(filas, año)`                | Solo las filas de `Visitants` de ese año                  |
| `filtrar(filas, distrito, ambito, titularidad)` | Filas que cumplen los 3 filtros (`""` = sin filtro)       |
| `ordenar(filas, columna, descendente)`          | Ordena por una columna                                    |
| `valores_distintos(filas, columna)`             | Valores sin repetir, para los desplegables                |
| `total_visitantes(filas)`                       | Suma los visitantes                                       |
| `porcentaje(parte, total)`                      | Porcentaje con 1 decimal                                  |
| `formatear_numero(numero)`                      | `5027015` → `"5.027.015"`                                 |
| `totales_por_anio(filas)`                       | Dos listas: años y total de cada año                      |
| `ranking(filas, columna, cantidad)`             | **Suma** visitantes por columna y devuelve los N primeros |
| `contar(filas, columna)`                        | **Cuenta** museos por cada valor de una columna           |
| `total_indicador(filas, indicador, anio)`       | Suma un indicador en un año (exposiciones, piezas…)       |
| `resumen_portada(filas)`                        | Diccionario con las cifras de Análisis                    |
| `resumen_presentacion(filas)`                   | Diccionario con los datos de Inicio                       |

### `cargar_museos()`

Recorre los años de 2015 a 2025 y abre cada `museos_BCN_AAAA.csv` con `csv.DictReader`, que convierte cada fila en un diccionario (`fila["Valor"]`, `fila["Ambit"]`…). Convierte el año y el valor a número con `int()` y limpia las notas con `.strip()`.

La carpeta de los CSV se calcula desde el propio archivo (`os.path.dirname(__file__)`), así funciona igual en local y en PythonAnywhere.

### `ordenar()`

Usa `sorted(filas, key=lambda fila: fila[columna], reverse=descendente)`. Para ordenar por dos columnas se llama dos veces, primero con la secundaria: `sorted` mantiene el orden anterior cuando hay empates.

### `ranking()` y `contar()`

Las dos agrupan con un diccionario (`{"Eixample": ..., "Ciutat Vella": ...}`):

- `ranking` suma los **visitantes**: sirve para saber qué distrito o museo recibe más visitas.
- `contar` suma **1 por fila**: sirve para saber cuántos museos hay de cada ámbito o distrito.

### `resumen_portada()` y `resumen_presentacion()`

Reúnen en un diccionario todas las cifras de una página, así cada ruta de `app.py` solo hace una llamada. Los porcentajes que calculan:

| Cifra                           | Cálculo                  | Resultado |
| ------------------------------- | ------------------------ | --------- |
| Caída por el COVID              | (2019 − 2020) / 2019     | −78,4 %   |
| Recuperación                    | (2025 − 2019) / 2019     | +7,7 %    |
| Peso del top 3                  | top 3 / total 2025       | 39,8 %    |
| Peso de Eixample + Ciutat Vella | 2 distritos / total 2025 | 59,3 %    |

Se compara con **2019** porque es el último año antes de la pandemia: así se ve si las visitas han vuelto al nivel anterior.

---

## `graficas.py`: las gráficas con matplotlib

| Función                             | Qué hace                                              |
| ----------------------------------- | ----------------------------------------------------- |
| `figura_a_base64(figura)`           | Convierte la gráfica en texto para meterla en el HTML |
| `grafica_evolucion(anios, totales)` | Líneas de visitantes por año                          |
| `grafica_barras(nombres, valores)`  | Barras horizontales (distritos y top 10)              |

### `figura_a_base64()`

Guarda la gráfica como PNG **en memoria** (`io.BytesIO`), sin crear archivos, y la convierte en texto base64. La plantilla la muestra con `<img src="data:image/png;base64,...">`. El fondo es transparente para que el color lo ponga el CSS.

### `grafica_evolucion()`

Línea de visitantes por año en millones, con el área rellena, una línea vertical en cada año (`vlines`) y el punto de 2020 resaltado con la etiqueta "COVID-19". El eje Y empieza en 0 para no exagerar la caída.

### `grafica_barras()`

Barras horizontales (`barh`) con la más grande arriba (`invert_yaxis`). En horizontal se leen bien los nombres largos de museos y distritos.

`matplotlib.use("Agg")` hace que matplotlib dibuje sin abrir ventanas, necesario en un servidor.
