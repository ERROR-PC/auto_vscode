"""Helper program for extensions"""

from subprocess import CalledProcessError, run as subprocess_run

YELLOW = '\33[33m'
END_COLOR = '\33[0m'

def install_vscode_extensions(*args):
    """Takes vscode extension IDs, installs them"""
    vscode_args = [
        "code"
    ]
    for extension_id in args:
        vscode_args.append("--install-extension")
        vscode_args.append(extension_id)
        vscode_args.append("--pre-release")
        vscode_args.append("--force")

    try:
        subprocess_run(vscode_args, check=False, shell=True)
    except (CalledProcessError, FileNotFoundError):
        print(f"{YELLOW}To install vscode extensions, {END_COLOR}")

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
