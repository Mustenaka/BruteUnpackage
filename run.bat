@echo off
rem Set the relative path
set "relative_path=rarlib\libunrar.dll"

rem Get the absolute path
for /f "delims=" %%A in ('cd') do set "absolute_path=%%A\%relative_path%"

rem Check if the file exists
if exist "%absolute_path%" (
    rem Add the path to the user's environment variables
    echo export UNRAR_LIB_PATH="%absolute_path%" >> %USERPROFILE%\.bashrc
    rem Make the environment variable take effect immediately
    call %USERPROFILE%\.bashrc
    echo Successfully set UNRAR_LIB_PATH environment variable to: "%absolute_path%"
) else (
    echo File "%absolute_path%" does not exist. Please ensure the path is correct.
)

rem Run the Python script
python main.py %*
