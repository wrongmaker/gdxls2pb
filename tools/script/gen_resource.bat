set PythonEnv=%cd%\..\venv\windows\Scripts\python.exe

cd pyscript
%PythonEnv% gen_resource.py
cd ..\

pause