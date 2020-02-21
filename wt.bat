
@echo Launching wt.py from Python ....
set PATH=%~dp0\wt-python;%~dp0\wt-python\Scripts;%PATH%
python.exe .wt\wt.py -nc
@echo Done.
pause
