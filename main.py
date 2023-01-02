"""A program to install vscode for python and C/C++"""

from tkinter import messagebox, filedialog, Tk
from subprocess import CalledProcessError, run as subprocess_run
import sys
import os

from color_codes import ColorCode
from funcs import errprint, install_app, yes_no_input
from constants import WINGET_ID

# This line is to make tkinter functions work properly
_temp = Tk("Le epic installer")
_temp.iconbitmap(os.path.join("assets", "installer.ico"))
_temp.withdraw()
del _temp

# is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

# Make sure colors works by switching to unicode characters
subprocess_run(["chcp", "65001"], shell=True, check=True)

try:
    subprocess_run(["winget"], shell=True, check=True, capture_output=True)
except (CalledProcessError, FileNotFoundError):
    errprint(
        f"{ColorCode.RED}\aYou have an old version of 'app installer'{ColorCode.END}"
    )
    errprint("This program needs a newer version of 'app installer' in order to work")
    answer = messagebox.askyesno(
        title="Update 'windows app installer'",
        message="You need to update 'windows app installer' for this program to work",
    )

    if answer is True:
        # launch ms store to winget
        subprocess_run(
            ["start", f"ms-windows-store://pdp/?ProductId={WINGET_ID}"],
            check=True,
            shell=True,
        )
    sys.exit(0)

# check python installation
# first assume it is in PATH
try:
    p = subprocess_run(["pydf", "--list"], check=True, capture_output=True, text=True)
    for line in p.stdout.splitlines():
        # 5th char is the major version number
        if line[4] == "3":
            install_python = False
            break

except (CalledProcessError, FileNotFoundError):
    install_python = True

# if it isn't, try finding it
# NEEDS TESTING ----------------------------------------------------------------!!!
if install_python:
    try:
        p = subprocess_run(
            ["where", "pythonfgv"],
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        install_python = False

        # check if multiple versions exist
        py_dir = p.stdout
        if "\n" in py_dir:
            # multiple versions exist, exit program
            errprint(
                f"{ColorCode.RED}Ambiguous {ColorCode.BLUE}python {ColorCode.RED}installations found.{ColorCode.END}"
            )
            for directory in py_dir.splitlines():
                errprint(directory)

            errprint("\nProgram is unable to decide which one to use")
            errprint("Aborting")
            subprocess_run(["pause"], shell=True, check=True)
            sys.exit(0)

    except (CalledProcessError, FileNotFoundError):
        ...

# check vscode installation
try:
    install_vscode = False
    subprocess_run(["code", "-h"], shell=True, check=True, capture_output=True)
except (CalledProcessError, FileNotFoundError):  # vscode not installed
    install_vscode = True

# check gcc installation
try:
    install_gcc = False
    subprocess_run(["gcc", "--version"], check=True, capture_output=True)
except (CalledProcessError, FileNotFoundError):  # gcc not installed
    install_gcc = True


# Printing results
if install_python or install_vscode or install_gcc:
    print("The following program(s) will be installed:")
    if install_vscode is True:
        print(f"•{ColorCode.WHITE2} Visual Studio Code (VSCode){ColorCode.END}")
    if install_gcc is True:
        print(f"• {ColorCode.GREEN}gcc, g++ (C/C++ compilers){ColorCode.END}")
    if install_python is True:
        print(f"• {ColorCode.BLUE}Python 3 interpreter{ColorCode.END}")

if not install_python or not install_vscode or not install_gcc:
    print(
        "The following program(s) are already installed, no need to install them again:"
    )
    if install_vscode is False:
        print(f"•{ColorCode.WHITE2} Visual Studio Code (VSCode){ColorCode.END}")
    if install_gcc is False:
        print(f"• {ColorCode.GREEN}gcc, g++ (C/C++ compilers){ColorCode.END}")
    if install_python is False:
        print(f"• {ColorCode.BLUE}Python 3 interpreter{ColorCode.END}")
print("\n")

# LOCATIONS CONFIG --------------------------------------------------
# Configure location of VScode
if install_vscode is True:
    done = False
    while not done:
        answer = yes_no_input(
            "Do you want to specify VScode install location",
            "3ayez te7aded VScode hynzl fen?",
        )

        if answer is True:
            vscode_path = filedialog.askdirectory(
                title="VScode install location", mustexist=False
            ).replace("/", "\\")

            if vscode_path == "":
                print(
                    f"{ColorCode.RED}You have cancelled the operation, the question will be repeated{ColorCode.END}"
                )
                continue

            done = True

        else:
            done = True
            vscode_path = os.path.join(
                "%LocalAppData%", "Programs", "Microsoft VS Code"
            )

    print(f"VScode will be installed in: {vscode_path}\n")

# Configure location of gcc
if install_gcc is True:
    done = False
    while not done:
        answer = yes_no_input(
            "Do you want to specify gcc/g++ install location",
            "3ayez te7aded gcc/g++ hynzl fen?",
        )

        if answer is True:
            done = False
            # Validate no spaces
            while not done:
                gcc_path = filedialog.askdirectory(
                    title="gcc/g++ install location", mustexist=False
                ).replace("/", "\\")

                if " " in gcc_path:
                    errprint(
                        f"{ColorCode.RED}Error: spaces not allowed in gcc path{ColorCode.END}"
                    )
                
                else:
                    done = True

        else:
            gcc_path = os.path.join("c:", "msys64")
            done = True

    print(f"gcc/g++ will be installed in: {gcc_path}\n")

# Configure location of python interpreter
if install_python is True:
    done = False
    while not done:
        answer = yes_no_input(
            "Do you want to specify python install location",
            "3ayez te7aded python hynzl fen?",
        )

        if answer is True:
            python_path = filedialog.askdirectory(
                title="Python 3.11 install location", mustexist=False
            ).replace("/", "\\")

            if python_path == "":
                print(
                    f"{ColorCode.RED}You have cancelled the operation, the question will be repeated{ColorCode.END}"
                )
                continue

            done = True

        else:
            done = True
            python_path = os.path.join(
                "%LocalAppData%", "Programs", "Python", "Python311"
            )

    print(f"python will be installed in: {python_path}\n")

# INSTALL ---------------------------------------------------
if install_vscode is True:
    print(f"{ColorCode.WHITE2}VSCode installation begining...{ColorCode.END}")
    install_app("Microsoft.VisualStudioCode", "--location", f"'{vscode_path}'")
    print()

if install_gcc is True:
    print(f"{ColorCode.GREEN}gcc/g++ installation begining...{ColorCode.END}")
    install_app("MSYS2.MSYS2", "--location", gcc_path)
    
    # start ucrt64 cmds
    bash_path = os.path.join(gcc_path, "usr", "bin", "bash.exe")
    
    print("Updating pacman packages (required for gcc)...")
    for _ in range(2):
        # has to be ran twice
        subprocess_run([bash_path, "-lc", "\"pacman --noconfirm -Syuu\""], shell=True, check=True)

    print("Downloading C compilers...")
    # tell ucrt to install gcc/g++ and gdb
    subprocess_run([bash_path, "-lc", "\"pacman --noconfirm -S mingw-w64-ucrt-x86_64-gcc\""], shell=True, check=True)
    print("Downloading gdb (C debugger)...")
    subprocess_run([bash_path, "-lc", "\"pacman --noconfirm -S mingw-w64-ucrt-x86_64-gdb\""], shell=True, check=True)

    print()
    # add gcc to PATH
    subprocess_run(["SETX", "/M", f"\"%PATH%;{bash_path}\""], check=True, shell=True)

if install_python is True:
    print(f"{ColorCode.BLUE}Python installation begining...{ColorCode.END}")
    install_app(
        "Python.Python.3.11",
        "--override",
        "/passive",
        "InstallAllUsers=1",
        f"DefaultAllUsersTargetDir='{python_path}'",
        "PrependPath=1",
        "AppendPath=1",
        "Include_symbols=1"
    )
    print()

# END ----------------------------------------------------
print("Program finished.")
subprocess_run(["pause"], shell=True, check=True)
