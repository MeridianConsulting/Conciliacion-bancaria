@echo off
echo ===================================================
echo    PRUEBA DE CARGA DE IMAGENES EN MODO DESARROLLO
echo ===================================================
echo.

echo Paso 1: Ejecutando test_dev_mode.py
python test_dev_mode.py
echo.
echo Presione cualquier tecla para continuar...
pause > nul

echo.
echo Paso 2: Ejecutando la aplicacion en modo desarrollo
python src/main.py
echo.
echo Presione cualquier tecla para finalizar...
pause > nul 