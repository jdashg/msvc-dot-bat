@echo off
echo %INCLUDE% > .msvc-path.txt
echo %LIB% >> .msvc-path.txt
where cl.exe >> .msvc-path.txt
