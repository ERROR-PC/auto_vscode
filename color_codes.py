"""This file is for the ColorCode enum"""

from enum import StrEnum

class ColorCode(StrEnum):
    """All color escape characters"""
    END      = '\33[0m'
    BOLD     = '\33[1m'
    ITALIC   = '\33[3m'
    URL      = '\33[4m'
    BLINK   = '\33[6m'
    SELECTED = '\33[7m'

    GREY    = '\33[90m'
    RED    = '\33[91m'
    GREEN  = '\33[92m'
    YELLOW = '\33[93m'
    BLUE   = '\33[94m'
    VIOLET = '\33[95m'
    BEIGE  = '\33[96m'
    WHITE  = '\33[97m'

    BLACKBG  = '\33[40m'
    GREYBG    = '\33[100m'
    REDBG    = '\33[101m'
    GREENBG  = '\33[102m'
    YELLOWBG = '\33[103m'
    BLUEBG   = '\33[104m'
    VIOLETBG = '\33[105m'
    BEIGEBG  = '\33[106m'
    WHITEBG  = '\33[107m'
