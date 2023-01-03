"""Functions used by main"""

from subprocess import run as subprocess_run, CompletedProcess
from sys import stderr, exit as sys_exit
from typing import List

from constants import WINGET_NO_INTERNET
from color_codes import ColorCode


def errprint(*args, **kwargs):
    """Prints to stderr (for errors)"""
    print(*args, file=stderr, **kwargs)


def internet_check(process: CompletedProcess):
    """If the process failed because of an internet connection, it will tell the user"""
    if process.returncode == WINGET_NO_INTERNET:
        errprint(f"{ColorCode.RED}Error: bad internet connection{ColorCode.END}")
        errprint("Program is aborting")
        subprocess_run(["pause"], shell=True, check=True)
        sys_exit(0)


def install_app(app_id: str, *installer_args):
    """Installs the given application"""

    winget_command = [
        "winget",
        "install",
        f"--id={app_id}",
        "-e",
        "-s=winget",
        "--accept-package-agreements",
        "--accept-source-agreements",
    ]

    # if it is not empty
    if installer_args:
        winget_command.extend(installer_args)

    process = subprocess_run(winget_command, shell=True, check=False)

    internet_check(process)


def yes_no_input(question: str, arabic_hint: str) -> bool:
    """Asks a yes or no question with validation"""
    while True:
        answer = input(question + " (y/n)? ")
        if (
            answer == "yes"
            or answer == "y"
            or answer == "yea"
            or answer == "yep"
            or answer == "ah"
            or answer == "aywa"
            or answer == "اه"
            or answer == "نعم"
            or answer == "ايوة"
        ):
            return True
        elif (
            answer == "no"
            or answer == "n"
            or answer == "nope"
            or answer == "la"
            or answer == "la2"
            or answer == "la2a"
            or answer == "لا"
            or answer == "لأ"
        ):
            return False
        else:
            print(arabic_hint)
            print("Enter y for 'yes', enter n for 'n'")
