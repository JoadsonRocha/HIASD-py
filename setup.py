from cx_Freeze import setup, Executable
import sys
import os

# Configurações básicas
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Para não mostrar console no Windows

# Arquivos e pastas adicionais
arquivos = [
    'hinos.json',
    'logo.png',
    'background.png',
    ('hinos', 'hinos')  # (pasta_origem, pasta_destino)
]

# Dependências
build_options = {
    'packages': ['tkinter', 'PIL'],
    'include_files': arquivos,
    'excludes': [],
    'optimize': 2
}

# Configuração do executável
executables = [
    Executable(
        'HIASD.py',
        base=base,
        icon='logo.ico',  # Opcional (converta o PNG para ICO)
        copyright="Copyright 2024 Seu Nome",
        shortcut_name="Hinário Adventista",
        shortcut_dir="DesktopFolder"
    )
]

setup(
    name='Hinário Adventista',
    version='1.0',
    description='Player de Hinos Adventistas',
    author='Joadson Rocha',
    options={'build_exe': build_options},
    executables=executables
)