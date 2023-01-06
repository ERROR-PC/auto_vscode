pyinstaller vscode_ext_install\main.py -y --onefile --name vscode_install --distpath assets\

pyinstaller -i .\assets\installer.ico --add-data=assets\installer.ico;assets main.py -y --name "auto vscode" --add-binary=assets\vscode_install.exe;assets --uac-admin --onefile
xcopy assets\ .\dist\assets\ /E /Y
