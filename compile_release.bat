ren main.py "auto vscode.py"
nuitka "auto vscode.py" --standalone --output-dir=build --windows-icon-from-ico=assets/installer.ico
ren "auto vscode.py" main.py
