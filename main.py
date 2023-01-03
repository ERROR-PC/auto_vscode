"""A program to install vscode for python and C/C++"""

from tkinter import messagebox, filedialog, Tk
from subprocess import CalledProcessError, run as subprocess_run
import sys
import os

# to check for admin perms
import ctypes

from color_codes import ColorCode
from funcs import *
from constants import WINGET_ID

# Make sure colors works by switching to unicode characters
subprocess_run(["chcp", "65001"], shell=True, check=False)

is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0


# This line is to make tkinter functions work properly
_temp = Tk("Le epic installer")
_temp.iconbitmap(os.path.join("assets", "installer.ico"))
_temp.withdraw()
del _temp

# * Check for winget
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

# * Check admin permissions (needed)
if is_admin is False:
    errprint("Run this program as Administrator")
    errprint(
        f"{ColorCode.RED}Error: permission to install apps denied, administrator permissions needed{ColorCode.END}\n"
    )
    subprocess_run(["pause"], check=False, shell=True)
    sys.exit(0)





# * Check for installed apps -------------------------------------------------------
# check python installation
try:
    p = subprocess_run(["py", "--list"], check=True, capture_output=True, text=True)
    for line in p.stdout.splitlines():
        # 5th char is the major version number
        if line[4] == "3":
            INSTALL_PYTHON = False
            break

except (CalledProcessError, FileNotFoundError):
    INSTALL_PYTHON = True

# check vscode installation
try:
    INSTALL_VSCODE = False
    subprocess_run(["code", "-h"], shell=True, check=True, capture_output=True)
except (CalledProcessError, FileNotFoundError):  # vscode not installed
    INSTALL_VSCODE = True

# check gcc installation
try:
    INSTALL_GCC = False
    subprocess_run(["gcc", "--version"], check=True, capture_output=True)
except (CalledProcessError, FileNotFoundError):  # gcc not installed
    INSTALL_GCC = True





# * Printing results --------------------------------------------------------
if INSTALL_PYTHON or INSTALL_VSCODE or INSTALL_GCC:
    print("The following program(s) will be installed:")
    if INSTALL_VSCODE is True:
        print(f"•{ColorCode.WHITE2} Visual Studio Code (VSCode){ColorCode.END}")
    if INSTALL_GCC is True:
        print(f"• {ColorCode.GREEN}gcc, g++ (C/C++ compilers){ColorCode.END}")
    if INSTALL_PYTHON is True:
        print(f"• {ColorCode.BLUE}Python 3 interpreter{ColorCode.END}")

print()

if not INSTALL_PYTHON or not INSTALL_VSCODE or not INSTALL_GCC:
    print(
        "The following program(s) are already installed, no need to install them again:"
    )
    if INSTALL_VSCODE is False:
        print(f"•{ColorCode.WHITE2} Visual Studio Code (VSCode){ColorCode.END}")
    if INSTALL_GCC is False:
        print(f"• {ColorCode.GREEN}gcc, g++ (C/C++ compilers){ColorCode.END}")
    if INSTALL_PYTHON is False:
        print(f"• {ColorCode.BLUE}Python 3 interpreter{ColorCode.END}")
print("\n")





# * Questions --------------------------------------------------
# Configure location of VScode
if INSTALL_VSCODE is True:
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

# Ask if user wants extensions for vscode
INSTALL_EXTS = yes_no_input(
    "Do you want to download vscode extension for C/C++ and python development - choose yes if you don't know",
    "If you don't know the answer, then choose yes",
)

# Configure location of gcc
if INSTALL_GCC is True:
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
if INSTALL_PYTHON is True:
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







# * Installations ---------------------------------------------------
# will be used whenever needed
PATH = subprocess_run(
    "PATH", check=False, shell=True, capture_output=True, text=True
).stdout

if INSTALL_VSCODE is True:
    print(f"{ColorCode.WHITE2}VSCode installation begining...{ColorCode.END}")
    if VSCODE_PATH is None:
        install_app("Microsoft.VisualStudioCode")
    else:
        install_app("Microsoft.VisualStudioCode", f'--location="{VSCODE_PATH}"')

    print()

if INSTALL_EXTS is True:
    install_vscode_extensions(
        # better comment highlighting
        "aaron-bond.better-comments",
        # C/C++ extension pack
        "ms-vscode.cpptools-extension-pack",
        # important C/C++ snippets
        "hars.CppSnippets",
        # Code runner
        "formulahendry.code-runner",
        # IntelliCode
        "VisualStudioExptTeam.vscodeintellicode",
        # IntelliCode for APIs
        "VisualStudioExptTeam.intellicode-api-usage-examples",
        # Python pack (pylance + Pyline + isort + jupiter + formatter + refactoring + ... a lot)
        "donjayamanne.python-extension-pack",
        # Python image preview (for PILLOW and such)
        "076923.python-image-preview",
        # todos and fixmes
        "Gruntfuggly.todo-tree",
        # Cool looking icons
        "vscode-icons-team.vscode-icons",
    )

    print()


if INSTALL_GCC is True:
    print(f"{ColorCode.GREEN}gcc/g++ installation begining...{ColorCode.END}")
    install_app("MSYS2.MSYS2", f"--location={GCC_PATH}")

    # start ucrt64 cmds
    bash_path = os.path.join(GCC_PATH, "usr", "bin", "bash.exe")

    print("\n\nUpdating pacman packages (required for gcc)...")
    for _ in range(2):
        # has to be ran twice
        subprocess_run(
            f'{bash_path} -lc "pacman -q  --color=always --needed --noconfirm -Syuu"',
            shell=True,
            check=False,
        )

    print("\n\nDownloading C compilers...")
    # tell ucrt to install gcc/g++ and gdb
    subprocess_run(
        f'{bash_path} -lc "pacman -S -q --disable-download-timeout --color=always --needed --noconfirm base-devel mingw-w64-x86_64-toolchain"',
        shell=True,
        check=False,
    )

    print()
    # add gcc to PATH
    usr_bin_path = GCC_PATH + os.path.sep + os.path.join("mingw64", "bin")
    if usr_bin_path not in PATH:
        subprocess_run(
            ["SETX", "/M", "PATH", f"%PATH%;{usr_bin_path}"], check=False, shell=True
        )

if INSTALL_PYTHON is True:
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

# * END ----------------------------------------------------
print("Program finished.")
subprocess_run(["pause"], shell=True, check=False)
