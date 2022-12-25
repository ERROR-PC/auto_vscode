"""Functions used by main"""

from subprocess import run as run_subprocess
from sys import stderr
from constants import WINGET_NO_INTERNET
from color_codes import ColorCode

def errprint(*args, **kwargs):
    """Prints to stderr (for errors)"""
    print(*args, file=stderr, **kwargs)

def install_app(app_id: str):
    """Installs the given application"""
    p = run_subprocess(
        [
            "winget",
            "install",
            "--id",
            f"{app_id}",
            "-e",
            "-s",
            "winget",
            "--accept-package-agreements",
            "--accept-source-agreements"
        ],
        shell=True,
        check=False,
    )

    if p.returncode == WINGET_NO_INTERNET:
        errprint(f"{ColorCode.RED}Your internet = 5ara{ColorCode.END}")
