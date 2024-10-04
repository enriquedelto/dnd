import os

def generate_directory_tree(root_dir, ignore_dirs):
    tree_lines = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Convertir dirpath a ruta relativa
        rel_dirpath = os.path.relpath(dirpath, root_dir)

        # Normalizar las rutas en dirnames
        dirnames[:] = [d for d in dirnames if os.path.normpath(os.path.join(rel_dirpath, d)) not in ignore_dirs]

        level = rel_dirpath.count(os.sep)
        indent = '    ' * level
        tree_lines.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = '    ' * (level + 1)
        for f in filenames:
            tree_lines.append(f"{subindent}{f}")
    return '\n'.join(tree_lines)

def collect_files(root_dir, ignore_dirs):
    files_content = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Convertir dirpath a ruta relativa
        rel_dirpath = os.path.relpath(dirpath, root_dir)

        # Normalizar las rutas en dirnames
        dirnames[:] = [d for d in dirnames if os.path.normpath(os.path.join(rel_dirpath, d)) not in ignore_dirs]

        # Ignorar archivos en directorios a ignorar
        if os.path.normpath(rel_dirpath) in ignore_dirs and rel_dirpath != '.':
            continue

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(filepath, root_dir)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                files_content.append(f"{relative_path}\n\n{content}\n\n---")
            except Exception as e:
                print(f"No se pudo leer el archivo {filepath}: {e}")
    return '\n'.join(files_content)

def main():
    # Reemplaza con la ruta de tu proyecto, utilizando una cadena raw
    root_dir = r'D:\vscode\paridas\darkanddarker'  

    # Lista de carpetas a ignorar, con rutas relativas y utilizando barras diagonales
    ignore_dirs = [
        'callbacks/__pycache__',
        'components/__pycache__',
        'data/__pycache__',
        'models/__pycache__',
        'dnd',
        '.git'
    ]

    # Normalizar las rutas en ignore_dirs
    ignore_dirs = [os.path.normpath(path) for path in ignore_dirs]

    # Generar el árbol de directorios
    directory_tree = generate_directory_tree(root_dir, ignore_dirs)

    # Recopilar el contenido de los archivos
    files_content = collect_files(root_dir, ignore_dirs)

    # Combinar todo en un solo archivo de texto
    with open('proyecto_unido.txt', 'w', encoding='utf-8') as output_file:
        output_file.write("Árbol de directorios:\n")
        output_file.write(directory_tree)
        output_file.write("\n\nContenido de los archivos:\n\n")
        output_file.write(files_content)

if __name__ == "__main__":
    main()
