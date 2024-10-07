# callbacks/callbacks.py

## Descripción

Este archivo define y registra los callbacks necesarios para manejar la interactividad de la aplicación Dash. Los callbacks son funciones que responden a las interacciones del usuario, actualizando dinámicamente los componentes de la interfaz en función de las entradas proporcionadas.

## Estructura del Código

### Importaciones

- **`from dash.dependencies import Input, Output, State, ALL`**: Importa las clases necesarias para definir las dependencias de los callbacks, incluyendo entradas, salidas y estados.
- **`from dash import html, dcc`**: Importa componentes de Dash para construir elementos HTML y componentes interactivos.
- **`from models.character import CharacterStats`**: Importa la clase `CharacterStats`, que maneja las estadísticas del personaje.
- **`from data.class_stats import class_stats`**: Importa el diccionario `class_stats` que contiene las estadísticas base de cada clase de personaje.
- **`from data.weapon_stats import weapon_stats`**: Importa el diccionario `weapon_stats` que contiene las estadísticas de las armas disponibles.
- **`import dash_bootstrap_components as dbc`**: Importa componentes de Bootstrap para estilizar y estructurar la interfaz de usuario.

### Función Principal: `register_callbacks(app)`

Esta función se encarga de registrar todos los callbacks necesarios para la aplicación. Al ser llamada en `app.py`, asegura que las interacciones del usuario se manejen correctamente.

```python
def register_callbacks(app):
    @app.callback(
        [
            Output('weapon1_left', 'options'),
            Output('weapon1_right', 'options'),
            Output('weapon2_left', 'options'),
            Output('weapon2_right', 'options'),
            Output('weapon1_left', 'disabled'),
            Output('weapon1_right', 'disabled'),
            Output('weapon2_left', 'disabled'),
            Output('weapon2_right', 'disabled'),
            Output('stats-table', 'data'),
            Output('movement-table', 'data'),
            Output('defense-table', 'data'),
            Output('utility-table', 'data'),
            Output('results_output', 'children'),  # Nuevo Output
        ],
        [
            Input('input-clase', 'value'),
            Input('stats-table', 'data'),
            Input('movement-table', 'data'),
            Input('weapon1_left', 'value'),
            Input('weapon1_right', 'value'),
            Input('weapon2_left', 'value'),
            Input('weapon2_right', 'value'),
            Input('combat_type', 'value'),
            Input('combination_select', 'value'),
            Input('result_type_select', 'value'),  # Nuevo Input
        ],
    )
    def actualizar_estadisticas(
        clase_seleccionada, stats_rows, movement_rows,
        weapon1_left, weapon1_right, weapon2_left, weapon2_right,
        combat_type, combination_select, result_type_select
    ):
        # Lógica del callback
        ...
```

#### Decorador `@app.callback`

- **Outputs**:
  - `weapon1_left.options`: Opciones disponibles para el dropdown del arma izquierda.
  - `weapon1_right.options`: Opciones disponibles para el dropdown del arma derecha.
  - `weapon2_left.options`: Opciones disponibles para el segundo arma izquierda (opcional).
  - `weapon2_right.options`: Opciones disponibles para el segundo arma derecha (opcional).
  - `weapon1_left.disabled`: Estado deshabilitado del dropdown del arma izquierda.
  - `weapon1_right.disabled`: Estado deshabilitado del dropdown del arma derecha.
  - `weapon2_left.disabled`: Estado deshabilitado del segundo arma izquierda.
  - `weapon2_right.disabled`: Estado deshabilitado del segundo arma derecha.
  - `stats-table.data`: Datos actualizados para la tabla de estadísticas principales.
  - `movement-table.data`: Datos actualizados para la tabla de movimiento.
  - `defense-table.data`: Datos actualizados para la tabla de defensa.
  - `utility-table.data`: Datos actualizados para la tabla de utilidad.
  - `results_output.children`: Contenido actualizado para la sección de resultados.

- **Inputs**:
  - `input-clase.value`: Clase seleccionada por el usuario.
  - `stats-table.data`: Datos actuales de la tabla de estadísticas.
  - `movement-table.data`: Datos actuales de la tabla de movimiento.
  - `weapon1_left.value`: Arma seleccionada en el dropdown del arma izquierda.
  - `weapon1_right.value`: Arma seleccionada en el dropdown del arma derecha.
  - `weapon2_left.value`: Arma seleccionada en el segundo arma izquierda (opcional).
  - `weapon2_right.value`: Arma seleccionada en el segundo arma derecha (opcional).
  - `combat_type.value`: Tipo de combate seleccionado.
  - `combination_select.value`: Combinación de ataques seleccionada.
  - `result_type_select.value`: Tipo de resultado seleccionado (nuevo input).

### Función Callback: `actualizar_estadisticas`

Esta función maneja la lógica para actualizar las estadísticas del personaje en función de las entradas del usuario.

#### Parámetros

- **`clase_seleccionada`**: Clase de personaje seleccionada por el usuario.
- **`stats_rows`**: Datos actuales de la tabla de estadísticas principales.
- **`movement_rows`**: Datos actuales de la tabla de movimiento.
- **`weapon1_left`**: Arma seleccionada en el arma izquierda.
- **`weapon1_right`**: Arma seleccionada en el arma derecha.
- **`weapon2_left`**: Arma seleccionada en el segundo arma izquierda (opcional).
- **`weapon2_right`**: Arma seleccionada en el segundo arma derecha (opcional).
- **`combat_type`**: Tipo de combate seleccionado.
- **`combination_select`**: Combinación de ataques seleccionada.
- **`result_type_select`**: Tipo de resultado seleccionado (nuevo input).

#### Descripción de la Función

1. **Obtención de Atributos Base**:
   - Recupera las estadísticas base de la clase seleccionada desde `class_stats`.

2. **Procesamiento de la Tabla de Estadísticas**:
   - Si no hay datos en `stats_rows`, inicializa las estadísticas con los valores base.
   - Si hay datos, aplica los encantamientos (`Add`) proporcionados por el usuario.

3. **Procesamiento de la Tabla de Movimiento**:
   - Inicializa y actualiza los valores de movimiento (`movement_add`, `movement_bonus`, `peso_arma`, `peso_armadura`) basados en las entradas del usuario.

4. **Cálculo del Peso de las Armas Seleccionadas**:
   - Suma el peso de todas las armas seleccionadas.

5. **Creación de una Instancia de `CharacterStats`**:
   - Utiliza las estadísticas y pesos calculados para crear una instancia de `CharacterStats`, que maneja los cálculos de estadísticas derivadas.

6. **Actualización de las Tablas de Estadísticas y Movimiento**:
   - Actualiza los valores en las tablas principales y de movimiento basándose en las estadísticas calculadas.

7. **Actualización de Opciones y Estados de las Armas**:
   - Filtra las opciones disponibles para las armas en función de las selecciones actuales, asegurando que no se seleccionen armas incompatibles (por ejemplo, armas de dos manos que deshabilitan el otro dropdown).

8. **Preparación de Datos para las Categorías**:
   - Prepara los datos para las tablas de defensa y utilidad basándose en las estadísticas calculadas.

9. **Generación del Contenido de Resultados**:
   - Dependiendo del tipo de resultado seleccionado (`result_type_select`), genera el contenido correspondiente:
     - **`damage`**: Muestra los resultados de daño.
     - **`movement_speed`**: Muestra la velocidad de movimiento total y con arma.
     - **Otros**: Solicita al usuario que seleccione un tipo de resultado.

10. **Retorno de los Valores Actualizados**:
    - Devuelve una tupla con todos los valores actualizados para los Outputs definidos en el decorador.

#### Funciones Auxiliares

- **`filtrar_opciones(seleccion_opuesta)`**:
  - **Descripción**: Filtra las opciones de armas disponibles para un dropdown específico basado en la selección opuesta.
  - **Parámetro**:
    - `seleccion_opuesta`: Arma seleccionada en el dropdown opuesto.
  - **Retorno**:
    - Lista de opciones filtradas que solo incluye armas de una mano si se ha seleccionado una arma de una mano en el dropdown opuesto.
    - Retorna una lista vacía si se ha seleccionado una arma de dos manos, deshabilitando así el otro dropdown.

    ```python
    def filtrar_opciones(seleccion_opuesta):
        if seleccion_opuesta:
            weapon_opuesta = weapon_stats[seleccion_opuesta]
            if weapon_opuesta['Manos'] == 2:
                return []
            else:
                return [
                    {'label': weapon['Nombre'], 'value': weapon_name}
                    for weapon_name, weapon in weapon_stats.items()
                    if weapon['Manos'] == 1
                ]
        else:
            return all_weapon_options
    ```

## Dependencias

- **Dash**: Framework principal para construir aplicaciones web interactivas.
- **Dash Bootstrap Components**: Biblioteca que integra Bootstrap con Dash para facilitar el diseño de la interfaz.
- **Models**:
  - **`CharacterStats`**: Clase que maneja las estadísticas del personaje.
- **Data**:
  - **`class_stats`**: Diccionario con estadísticas base de cada clase.
  - **`weapon_stats`**: Diccionario con estadísticas de las armas disponibles.

## Archivos Relacionados

- **`app.py`**: Punto de entrada de la aplicación que inicializa Dash, establece el layout y registra los callbacks.
- **`components/layout.py`**: Define el layout de la aplicación utilizando componentes de Dash y Bootstrap.
- **`models/character.py`**: Define la clase `CharacterStats` utilizada para calcular y manejar las estadísticas del personaje.
- **`data/class_stats.py`**: Contiene las estadísticas base de las diferentes clases de personajes.
- **`data/weapon_stats.py`**: Incluye las estadísticas de las armas disponibles en la aplicación.

## Detalles Adicionales

- **Manejo de Armas de Dos Manos**:
  - Si el usuario selecciona un arma que requiere dos manos (`Manos: 2`), los dropdowns de armas opuestos se deshabilitan para evitar selecciones incompatibles.

- **Actualización Dinámica de Tablas**:
  - Las tablas de estadísticas, movimiento, defensa y utilidad se actualizan en tiempo real conforme el usuario modifica las entradas, proporcionando una retroalimentación inmediata sobre las estadísticas del personaje.

- **Resultados Personalizables**:
  - La sección de resultados permite al usuario seleccionar el tipo de información que desea ver (`Daño` o `Velocidad de Movimiento`), mostrando contenido relevante basado en la selección.

## Notas Adicionales

- **Mantenimiento de Datos**:
  - Asegúrate de que los diccionarios `class_stats` y `weapon_stats` estén actualizados con todas las clases y armas necesarias para la aplicación.

- **Extensibilidad**:
  - Puedes agregar más tipos de resultados en el callback `actualizar_estadisticas` siguiendo el patrón existente, ampliando así la funcionalidad de la aplicación.

- **Depuración**:
  - En caso de errores en los callbacks, verifica que la cantidad y el orden de los `Input` y `Output` en el decorador coincidan con los parámetros y retornos de la función `actualizar_estadisticas`.

## Ejemplo de Uso

Supongamos que un usuario selecciona la clase **Bárbaro**, elige **Arming Sword** en el arma izquierda y **Bare Hands** en el arma derecha. La función `actualizar_estadisticas`:

1. Obtendrá las estadísticas base para la clase Bárbaro.
2. Aplicará los encantamientos proporcionados en las tablas de estadísticas y movimiento.
3. Calculará el peso total de las armas seleccionadas.
4. Creará una instancia de `CharacterStats` para calcular las estadísticas derivadas.
5. Actualizará las tablas de estadísticas, movimiento, defensa y utilidad con los nuevos valores.
6. Filtrará las opciones de armas disponibles para asegurar que no se seleccionen armas incompatibles.
7. Generará el contenido de resultados basado en el tipo de resultado seleccionado por el usuario.

## Enlaces Relacionados

- **[app.py](app.md)**: Punto de entrada de la aplicación.
- **[components/layout.py](components/layout.md)**: Detalles sobre cómo se construye el layout de la aplicación.
- **[models/character.py](models/character.md)**: Define la clase `CharacterStats` utilizada para calcular las estadísticas del personaje.
- **[data/class_stats.py](data/class_stats.md)**: Contiene las estadísticas base de las diferentes clases de personajes.
- **[data/weapon_stats.py](data/weapon_stats.md)**: Incluye las estadísticas de las armas disponibles en la aplicación.

## Contacto y Soporte

Si encuentras problemas o tienes preguntas sobre este archivo, por favor contacta al desarrollador del proyecto o consulta las otras secciones de la documentación para obtener más información.