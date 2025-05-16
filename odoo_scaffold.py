import os
import sys

from template import MODULE_TEMPLATE

def create_module(module_name, target_path):
    camel_name = ''.join(word.capitalize() for word in module_name.split('_'))
    module_path = os.path.join(target_path, module_name)
    if os.path.exists(module_path):
        print(f"❌ El módulo '{module_name}' ya existe en '{target_path}'")
        return

    os.makedirs(module_path)
    for relative_path, content in MODULE_TEMPLATE.items():
        file_path = os.path.join(module_path, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            try:
                f.write(content.format(module_name=module_name, camel_name=camel_name))
            except KeyError as e:
                print(f"❌ Error al procesar '{relative_path}': {e}")
                raise


    print(f"✅ Módulo '{module_name}' creado en: {module_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python odoo_scaffold.py nombre_modulo ruta_destino")
        sys.exit(1)

    module_name = sys.argv[1]
    if not module_name.isidentifier():
        print("❌ El nombre del módulo contiene caracteres no válidos.")
        sys.exit(1)
    target_path = os.path.abspath(sys.argv[2])
    create_module(module_name, target_path)
