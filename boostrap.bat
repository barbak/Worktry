@echo off

if exist python-3.7.4-embed-win32.zip (
    echo python-3.7.4-embed-win32.zip already downloaded.
) else (
    echo | set /p="Downloading Python ... "
    powershell -Command ^
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ^
            Invoke-WebRequest ^
                -Uri https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-win32.zip ^
                -OutFile python-3.7.4-embed-win32.zip
    echo Done.
)

if exist getpip.py (
    echo getpip.py already downloaded.
) else (
    echo | set /p="Downloading getpip.py ... "
    powershell -Command ^
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ^
        Invoke-WebRequest ^
            -Uri https://bootstrap.pypa.io/get-pip.py ^
            -OutFile getpip.py
    echo Done.
)

if exist wt-python (
    echo | set /p="Removing previous python install in wt-python... "
    rmdir /s /q wt-python
    echo Done.
)

echo | set /p="Unzipping Python ... "
powershell -Command Expand-Archive python-3.7.4-embed-win32.zip -DestinationPath wt-python
echo Done.

echo Installing pip ...
wt-python\python.exe getpip.py --no-warn-script-location
echo Done.

echo Executing python boostrap script ...
wt-python\python boostrap
echo Done.

pause
