@echo off
title Cargando Entorno de Python...

:: 1. Borrar venv si existe (opcional, pero recomendado si falló)
if exist venv (
    echo [INFO] Limpiando entorno anterior...
    rmdir /s /q venv
)

:: 1. Comprobar si existe la carpeta del entorno virtual (venv)
if not exist venv (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
)

:: 2. Activar el entorno virtual
echo [INFO] Activando entorno...
call venv\Scripts\activate

:: 4. LA SOLUCION: Actualizar herramientas de instalacion primero
echo [INFO] Actualizando herramientas fundamentales...
python -m pip install --upgrade pip setuptools wheel

:: 3. Instalar o actualizar las librerías
echo [INFO] Verificando dependencias...
python -m pip install --upgrade pip setuptools wheel
pip install PySide6

:: 4. Ejecutar el script principal
echo [INFO] Iniciando programa...
python main.py

:: Evitar que la ventana se cierre si hay un error
pause