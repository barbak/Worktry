
echo | set /p="Launching wt.py from Python ... "
set PATH=%~dp0\wt-python\Scripts;%PATH%
start /wait ^
    wt-python\python.exe .wt\wt.py
echo Done.
