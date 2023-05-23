
@ECHO OFF
:start
SET choice=
SET /p choice=Open abaqus GUI? [Y/N]: 
IF NOT '%choice%'=='' SET choice=%choice:~0,1%
IF '%choice%'=='Y' GOTO yes
IF '%choice%'=='y' GOTO yes
IF '%choice%'=='N' GOTO no
IF '%choice%'=='n' GOTO no
IF '%choice%'=='' GOTO no
ECHO "%choice%" is not valid
ECHO.
GOTO start

:no
ECHO Do all of the no things here!
abaqus cae noGUI=build_model.py

PAUSE
EXIT

:yes
ECHO Do all of the yes things here!
abaqus cae script=build_model.py

PAUSE
EXIT