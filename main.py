"""A program to install vscode for python and C/C++"""

from tkinter import messagebox, filedialog, Tk
from subprocess import CalledProcessError, run as subprocess_run
import sys
import os

# to check for admin perms
import ctypes

from color_codes import ColorCode
from funcs import errprint, install_app, yes_no_input
from constants import WINGET_ID

# Make sure colors works by switching to unicode characters
subprocess_run(["chcp", "65001"], shell=True, check=False)

is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0


# This line is to make tkinter functions work properly
_temp = Tk("Le epic installer")
_temp.iconbitmap(os.path.join("assets", "installer.ico"))
_temp.withdraw()
del _temp

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

# check admin permissions (needed)
if is_admin is False:
    errprint("Run this program as Administrator")
    errprint(
        f"{ColorCode.RED}Error: permission to install apps denied, administrator permissions needed{ColorCode.END}\n"
    )
    subprocess_run(["pause"], check=False, shell=True)
    sys.exit(0)

# check python installation
# first assume it is in PATH
try:
    p = subprocess_run(["py", "--list"], check=True, capture_output=True, text=True)
    for line in p.stdout.splitlines():
        # 5th char is the major version number
        if line[4] == "3":
            install_python = False
            break

except (CalledProcessError, FileNotFoundError):
    install_python = True

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

print()

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
            VSCODE_PATH = filedialog.askdirectory(
                title="VScode install location", mustexist=False
            ).replace("/", "\\")

            if VSCODE_PATH == "":
                print(
                    f"{ColorCode.RED}You have cancelled the operation, the question will be repeated{ColorCode.END}"
                )
                continue

            done = True

        else:
            done = True
            VSCODE_PATH = None

    print(f"VScode will be installed in: {VSCODE_PATH}\n")

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
                GCC_PATH = filedialog.askdirectory(
                    title="gcc/g++ install location", mustexist=False
                ).replace("/", "\\")

                if " " in GCC_PATH:
                    errprint(
                        f"{ColorCode.RED}Error: spaces not allowed in gcc path{ColorCode.END}"
                    )

                else:
                    done = True

        else:
            GCC_PATH = "c:\\msys64"
            done = True

    print(f"gcc/g++ will be installed in: {GCC_PATH}\n")

# Configure location of python interpreter
if install_python is True:
    done = False
    while not done:
        answer = yes_no_input(
            "Do you want to specify python install location",
            "3ayez te7aded python hynzl fen?",
        )

        if answer is True:
            PYTHON_PATH = filedialog.askdirectory(
                title="Python 3.11 install location", mustexist=False
            ).replace("/", "\\")

            if PYTHON_PATH == "":
                print(
                    f"{ColorCode.RED}You have cancelled the operation, the question will be repeated{ColorCode.END}"
                )
                continue

            done = True

        else:
            done = True
            PYTHON_PATH = None

    print(f"python will be installed in: {PYTHON_PATH}\n")

# INSTALL ---------------------------------------------------
# will be reused whenever needed
PATH = subprocess_run(
    "PATH", check=False, shell=True, capture_output=True, text=True
).stdout

if install_vscode is True:
    print(f"{ColorCode.WHITE2}VSCode installation begining...{ColorCode.END}")
    if VSCODE_PATH is None:
        install_app("Microsoft.VisualStudioCode")
    else:
        install_app("Microsoft.VisualStudioCode", f'--location="{VSCODE_PATH}"')

    print()

if install_gcc is True:
    print(f"{ColorCode.GREEN}gcc/g++ installation begining...{ColorCode.END}")
    install_app("MSYS2.MSYS2", f"--location={GCC_PATH}")

    # start ucrt64 cmds
    bash_path = os.path.join(GCC_PATH, "usr", "bin", "bash.exe")

    print("\n\nUpdating pacman packages (required for gcc)...")
    for _ in range(2):
        # has to be ran twice
        subprocess_run(
            f'{bash_path} -lc "pacman -q --color=always --needed --noconfirm -Syuu"',
            shell=True,
            check=False,
        )

    print("\n\nDownloading C compilers...")
    # tell ucrt to install gcc/g++ and gdb
    subprocess_run(
        f'{bash_path} -lc "pacman -q --color=always --needed --noconfirm -S mingw-w64-ucrt-x86_64-gcc"',
        shell=True,
        check=False,
    )

    print()
    # add gcc to PATH
    usr_bin_path = GCC_PATH + os.path.sep + os.path.join("ucrt64", "bin")
    if usr_bin_path not in PATH:
        subprocess_run(
            ["SETX", "/M", "PATH", f"%PATH%;{usr_bin_path}"], check=False, shell=True
        )

if install_python is True:
    print(f"{ColorCode.BLUE}Python installation begining...{ColorCode.END}")

    # " args..."
    override_cmd = [
        "/passive",
        "InstallAllUsers=1",
        "CompileAll=1",
        "PrependPath=1",
        "AppendPath=1",
        "Include_symbols=1",
    ]

    if PYTHON_PATH is not None:
        override_cmd.append(f"TargetDir='{PYTHON_PATH}'")

    override_cmd = '"' + " ".join(override_cmd) + '"'
    install_app("Python.Python.3.11", f"--override={override_cmd}")
    print()

# END ----------------------------------------------------
print("Program finished.")
subprocess_run(["pause"], shell=True, check=False)
