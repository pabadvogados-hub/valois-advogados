@echo off
REM Sincronizacao ZapSign -> Drive (Welington Valois Advogados Associados)
REM Agendar no Task Scheduler do Windows (3x ao dia).
REM Ajuste o caminho abaixo para a pasta onde o projeto foi instalado.
set "PROJETO=%~dp0.."
cd /d "%PROJETO%"
"%LOCALAPPDATA%\Microsoft\WindowsApps\py.exe" "%PROJETO%\SYNC\sync_assinados.py"
