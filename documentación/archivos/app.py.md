# app.py

## Descripción

Este archivo es el punto de entrada principal de la aplicación Dash. Inicializa la aplicación, establece el layout y registra los callbacks necesarios para proporcionar la funcionalidad interactiva.

## Estructura del Código

### Importaciones

- **`from dash import Dash`**: Importa la clase `Dash` para crear la instancia principal de la aplicación.
- **`import dash_bootstrap_components as dbc`**: Importa componentes de Bootstrap para estilizar y estructurar la interfaz de usuario.
- **`from components import create_layout`**: Importa la función `create_layout` desde el módulo `components`, que genera el layout de la aplicación.
- **`from callbacks import register_callbacks`**: Importa la función `register_callbacks` desde el módulo `callbacks`, que registra todos los callbacks necesarios para la interactividad.

### Inicialización de la Aplicación

```python
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
```

- **Descripción**: Crea una instancia de la aplicación Dash.
- **Detalles**:
  - `__name__`: Indica el nombre del módulo actual.
  - `external_stylesheets`: Aplica estilos externos, en este caso, el tema de Bootstrap para una mejor apariencia.

### Establecimiento del Layout

```python
app.layout = create_layout(app)
```

- **Descripción**: Establece el layout de la aplicación utilizando la función `create_layout`.
- **Detalles**:
  - El layout define la estructura y los componentes visuales de la aplicación.
  - Se pasa la instancia `app` a la función `create_layout` por si es necesario en el layout.

### Registro de Callbacks

```python
register_callbacks(app)
```

- **Descripción**: Registra los callbacks que manejan la lógica interactiva de la aplicación.
- **Detalles**:
  - Los callbacks son funciones que actualizan la interfaz en respuesta a las acciones del usuario.
  - Se aseguran de que los componentes de la interfaz estén sincronizados y muestren información actualizada.

### Ejecución del Servidor

```python
if __name__ == '__main__':
    app.run_server(debug=True)
```

- **Descripción**: Inicia el servidor de la aplicación cuando se ejecuta el script directamente.
- **Detalles**:
  - `debug=True`: Activa el modo de depuración, que proporciona información detallada de errores y recarga automática al cambiar el código.
  - La aplicación se ejecutará en `http://127.0.0.1:8050/` por defecto.

## Dependencias

- **Dash**: Framework principal para construir aplicaciones web interactivas en Python.
- **Dash Bootstrap Components**: Biblioteca que integra Bootstrap con Dash para facilitar el diseño de la interfaz.

## Archivos Relacionados

- **`components/layout.py`**: Contiene la función `create_layout` que define la estructura de la interfaz.
- **`callbacks/callbacks.py`**: Define los callbacks que gestionan la lógica de actualización de la aplicación.
- **`assets/styles.css`**: Archivo de estilos personalizados para la aplicación (actualmente vacío).

## Estructura del Proyecto

```
├── app.py
├── assets/
│   └── styles.css
├── components/
│   ├── __init__.py
│   └── layout.py
├── callbacks/
│   ├── __init__.py
│   └── callbacks.py
├── data/
│   ├── __init__.py
│   ├── class_stats.py
│   └── weapon_stats.py
├── models/
│   ├── __init__.py
│   └── character.py
```

## Enlaces Relacionados

- **[components/layout.py](components/layout.md)**: Detalles sobre cómo se construye el layout de la aplicación.
- **[callbacks/callbacks.py](callbacks/callbacks.md)**: Información sobre los callbacks y la lógica de actualización.
- **[models/character.py](models/character.md)**: Define la clase `CharacterStats` utilizada para calcular las estadísticas del personaje.
- **[data/class_stats.py](data/class_stats.md)**: Contiene las estadísticas base de las diferentes clases de personajes.
- **[data/weapon_stats.py](data/weapon_stats.md)**: Incluye las estadísticas de las armas disponibles en la aplicación.
