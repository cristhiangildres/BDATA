# Frontend: plantillas HTML y diseño

Las páginas se generan con plantillas **Jinja** (requisito 5), en la carpeta `templates/`, y todo el diseño está en `static/style.css`. Flask busca las plantillas en `templates/` y sirve tal cual los archivos de `static/`. No se usa JavaScript.

---

## Las plantillas

| Plantilla       | Página                 | Qué contiene                                                         |
| --------------- | ---------------------- | -------------------------------------------------------------------- |
| `base.html`     | todas                  | Estructura común: fuentes, CSS, menú, pie y huecos                   |
| `index.html`    | Inicio (`/`)           | Mosaico, 4 cifras, tipos de museos, dónde están y quién los gestiona |
| `analisis.html` | Análisis (`/analisis`) | 4 cifras, 2 gráficas y conclusiones                                  |
| `museos.html`   | Museos (`/museos`)     | Formulario de filtros, gráfica del top 10 y tabla                    |

### Jinja en pocas palabras

| Sintaxis        | Para qué                      | Ejemplo en el proyecto                     |
| --------------- | ----------------------------- | ------------------------------------------ |
| `{{ valor }}`   | Escribe un dato               | `{{ resumen["total_2025"] }}`              |
| `{% for %}`     | Repite                        | Filas de la tabla, opciones de los filtros |
| `{% if %}`      | Muestra u oculta              | Columnas de la vista detallada             |
| `{% extends %}` | Hereda de otra plantilla      | Todas heredan de `base.html`               |
| `{% block %}`   | Hueco que rellena cada página | `cabecera` y `contenido`                   |
| `\|filtro`      | Transforma un valor           | `\|miles`, `\|length`, `\|join(", ")`      |

### `base.html`

Todas las páginas empiezan con `{% extends "base.html" %}` y solo rellenan sus huecos. Así el menú y el pie se escriben una sola vez. Tiene dos huecos: `cabecera`, fuera de `<main>` para que la cabecera grande ocupe todo el ancho, y `contenido`.

### `index.html`

El mosaico de la cabecera se crea con un bucle de Jinja de 48 piezas:

```html
{% for i in range(48) %}
  <span class="tesela c{{ (i * 7 + i // 6) % 5 }} f{{ (i * 3) % 5 }}" style="--i: {{ i }}"></span>
{% endfor %}
```

`c0`…`c4` es el color, `f0`…`f4` la forma y `--i` el número de cada pieza, que el CSS usa para que caigan una detrás de otra. El texto de "qué puedes ver" en cada ámbito está escrito a mano, porque el CSV no lo trae; los números y los ejemplos salen de los datos.

### `museos.html`

El formulario usa `method="get"`, así los filtros viajan en la URL. Cada `<option>` lleva `{% if ... %}selected{% endif %}` para que el formulario recuerde lo elegido después de pulsar "Aplicar". La opción "Todos" tiene `value=""`, que significa sin filtro.

Las columnas extra (barrio, ámbito, titularidad y notas) solo aparecen si `vista == "detalle"`. Es el "mostrar más o menos información" del requisito 3.

### Las gráficas

Llegan como texto base64 y se muestran con `<img src="data:image/png;base64,{{ grafica }}" alt="...">`. Cada una tiene su título en un `<h3>` y un párrafo que explica la conclusión.

---

## El diseño (`style.css`)

Inspirado en el **modernisme** barcelonés y en los carteles de museo.

| Color        | Código    | Uso                                     |
| ------------ | --------- | --------------------------------------- |
| Granate      | `#8b1e3f` | Color principal, ámbito Artes visuales  |
| Ocre         | `#c8963e` | Acentos, ámbito Historia y memoria      |
| Azul mosaico | `#1f4e5f` | Detalles, ámbito Ciencia                |
| Tinta        | `#1f1a17` | Texto, menú, pie y cabecera de la tabla |
| Crema        | `#f4efe6` | Fondo de la página                      |

- **Fuentes:** *Playfair Display* para los títulos y *Source Sans 3* para el texto, cargadas desde Google Fonts.
- **Los colores informan:** cada ámbito tiene su color en las tarjetas de Inicio.
- **Mosaico trencadís:** las piezas tienen formas irregulares con `clip-path` y caen girando al cargar la página (`@keyframes colocar`), cada una 35 ms después de la anterior.
- **Tarjetas:** las de cifras y ámbitos tienen esquinas de 12px y suben al pasar el ratón (`transition` + `transform`). Las de gráficas tienen 6px y no se mueven, para leerlas con calma.
- **Responsive:** las rejillas (`grid` con `auto-fit`) se reorganizan en el móvil, el mosaico pasa debajo del título y la tabla se puede deslizar de lado.
- **Accesibilidad:** borde dorado al navegar con el teclado, texto alternativo en las gráficas y sin animaciones si el usuario tiene activado "reducir movimiento".
- Los estilos de las gráficas están juntos al final, bajo el comentario `/* ===== Estilo gráficas ===== */`.
