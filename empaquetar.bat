@echo off
echo =========================================
echo  Empaquetador de Conciliacion Bancaria
echo =========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en la ruta del sistema.
    echo Por favor instale Python 3.9 o superior y asegúrese de que esté en la ruta del sistema.
    pause
    exit /b 1
)

echo Instalando dependencias necesarias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Ejecutando proceso de empaquetado...
echo.

REM Ejecutar PyInstaller con el archivo spec
pyinstaller --clean ConciliacionBancaria.spec

if errorlevel 1 (
    echo.
    echo ERROR: Ocurrió un problema durante el empaquetado.
    pause
    exit /b 1
)

echo.
echo =========================================
echo Proceso completado correctamente!
echo.
echo El ejecutable se encuentra en la carpeta dist/
echo =========================================
echo.

pause 