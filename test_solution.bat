@echo off
echo ===================================================
echo    PRUEBA DE SOLUCION PARA CARGA DE IMAGENES
echo ===================================================
echo.

echo Paso 1: Ejecutando test_resources.py en modo desarrollo
python src/test_resources.py
echo.
echo Presione cualquier tecla para continuar con el empaquetado...
pause > nul

echo.
echo Paso 2: Empaquetando test_resources.py con PyInstaller
python test_build.py
echo.
echo Presione cualquier tecla para ejecutar la version empaquetada...
pause > nul

echo.
echo Paso 3: Ejecutando la version empaquetada
dist\TestResources.exe
echo.

echo Paso 4: Empaquetando la aplicacion completa
python build_exe.py
echo.
echo Presione cualquier tecla para finalizar...
pause > nul 