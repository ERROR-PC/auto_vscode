"""A program to install vscode for python and C/C++"""

from tkinter import messagebox, filedialog, Tk
from subprocess import CalledProcessError, run as subprocess_run
import sys
import os

# to check for admin perms
import ctypes

from color_codes import ColorCode
from funcs import *
from constants import WINGET_ID, WINGET_ALREADY_INSTALLED

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
    else:
        INSTALL_PYTHON = True

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
        print(f"•{ColorCode.WHITE} Visual Studio Code (VSCode){ColorCode.END}")
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
        print(f"•{ColorCode.WHITE} Visual Studio Code (VSCode){ColorCode.END}")
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
    if VSCODE_PATH is not None:
        print(f"VScode will be installed in: {VSCODE_PATH}\n")
    else:
        print("VScode will be installed in the default location\n")


# Ask if user wants extensions for vscode
INSTALL_EXTS = yes_no_input(
    "Do you want to download vscode extension for C/C++ and python development - choose yes if you don't know",
    "If you don't know the answer, then choose yes",
)
print()

# Configure location of gcc
if INSTALL_GCC is True:
    done = False
    while not done:
        answer = yes_no_input(
            "Do you want to specify gcc/g++ install location",
            "3ayez te7aded gcc/g++ hynzl fen?",
        )

        if answer is True:
            GCC_PATH = filedialog.askdirectory(
                title="gcc/g++ install location", mustexist=False
            ).replace("/", "\\")

            if GCC_PATH == "":
                print(
                    f"{ColorCode.RED}You have cancelled the operation, the question will be repeated{ColorCode.END}"
                )
                continue

            elif " " in GCC_PATH:
                print(f"{ColorCode.RED}{GCC_PATH}{ColorCode.END}")
                print(
                    f"{ColorCode.RED}Error: spaces not allowed in gcc path{ColorCode.END}"
                )
                continue

            done = True

        else:
            done = True
            GCC_PATH = "c:\\msys64"

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

    if PYTHON_PATH is not None:
        print(f"python will be installed in: {PYTHON_PATH}\n")
    else:
        print("Python will be installed in the default location\n")


# * Installations ---------------------------------------------------
# Clear screen
print("Installation is going to begin, there won't be more questions or prompts")
subprocess_run(["pause"], shell=True, check=False)
subprocess_run(["cls"], shell=True, check=False)

# None means preinstalled
# If it is not preinstalled, the variables will change
vscode_returncode = None
vscode_exts_returncode = None
gcc_returncode = None
gcc_path_process = None
python_returncode = None

# will be used whenever needed
PATH = subprocess_run(
    "PATH", check=False, shell=True, capture_output=True, text=True
).stdout

if INSTALL_VSCODE is True:
    print(f"{ColorCode.WHITE}VSCode installation begining...{ColorCode.END}")
    if VSCODE_PATH is None:
        vscode_returncode = install_app("Microsoft.VisualStudioCode")
    else:
        vscode_returncode = install_app(
            "Microsoft.VisualStudioCode", f'--location="{VSCODE_PATH}"'
        )

    print()

if INSTALL_GCC is True:
    print(f"{ColorCode.GREEN}gcc/g++ installation begining...{ColorCode.END}")
    gcc_returncode = install_app("MSYS2.MSYS2", f"--location={GCC_PATH}")

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
        f'{bash_path} -lc "pacman -S -q --disable-download-timeout --color=always --needed --noconfirm mingw-w64-x86_64-gcc"',
        shell=True,
        check=False,
    )

    subprocess_run(
        f'{bash_path} -lc "pacman -S -q --disable-download-timeout --color=always --needed --noconfirm mingw-w64-x86_64-gdb"',
        shell=True,
        check=False,
    )

    print()
    # add gcc to PATH
    usr_bin_path = GCC_PATH + os.path.sep + os.path.join("mingw64", "bin")
    if usr_bin_path not in PATH:
        gcc_path_process = subprocess_run(
            ["SETX", "/M", "PATH", f"%PATH%;{usr_bin_path}"],
            check=False,
            shell=True,
            text=True,
        )

    print()

if INSTALL_EXTS is True:
    # has to be ran as a seperate process
    # because the PATH variable does not update
    # unless you restart
    vscode_exts_returncode = subprocess_run(
        os.path.join("assets", "vscode_install.exe"), check=False
    ).returncode

    print()

if INSTALL_PYTHON is True:
    print(f"{ColorCode.BLUE}Python installation begining...{ColorCode.END}")

    process = subprocess_run(
        ["winget", "show", "--id=Python.Python.3.11", "-e", "-s=winget"],
        check=False,
        shell=True,
        capture_output=True,
        text=True,
    )

    internet_check(process)

    # Get url of python
    url_start_index = process.stdout.find("Download Url: ") + 14
    url_end_index = process.stdout.find("\n", url_start_index)
    python_url = process.stdout[url_start_index:url_end_index]
    # Get installer name (last part of url)
    python_installer_name = python_url.split("/")[-1]

    # Download installer manually
    subprocess_run(
        [
            "powershell",
            "iwr",
            python_url,
            "-OutFile",
            '"' + os.path.join("%temp%", python_installer_name) + '"',
        ],
        check=False,
        shell=True,
    )

    # prepare args for python installer
    python_args = [
        os.path.join("%temp%", python_installer_name),
        "/passive",
        "InstallAllUsers=1",
        "CompileAll=1",
        "PrependPath=1",
        "AppendPath=1",
        "Include_symbols=1",
    ]

    if PYTHON_PATH is not None:
        python_args.append(f"TargetDir=\"{PYTHON_PATH}\"")

    print(f"Python args = {python_args}")
    python_returncode = subprocess_run(python_args, check=False, shell=True).returncode

    print()

# * END ----------------------------------------------------
print_success_or_fail("VScode", vscode_returncode)

print_success_or_fail("VScode extensions", vscode_exts_returncode)
if INSTALL_EXTS:
    print("Note: if VScode extensions failed to install, try restarting the program")

if gcc_returncode == WINGET_ALREADY_INSTALLED:
    print(f"{ColorCode.YELLOW}gcc/g++ was already installed.{ColorCode.END}")
else:
    print_success_or_fail("C compilers", gcc_returncode)

if gcc_path_process is not None:
    if gcc_path_process.returncode != 0:
        print(f"{ColorCode.RED}C was not added to PATH{ColorCode.END}")
        with open(os.path.join("assets", "errors.txt"), "w") as file:
            file.write(f"PATH output: {gcc_path_process.stdout}")
            file.write(f"PATH returncode: {gcc_path_process.returncode}")

print_success_or_fail("Python", python_returncode)

print("\nProgram finished.")
subprocess_run(["pause"], shell=True, check=False)
