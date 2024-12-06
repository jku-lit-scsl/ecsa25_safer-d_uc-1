# Created on 06.12.2024

from sec_levels.DefconHandler import DefconHandler
from util.utils import setup_logging

if __name__ == "__main__":
    setup_logging()
    defconHandler = DefconHandler()
    defconHandler.increase()
    defconHandler.increase()
    defconHandler.increase()
    defconHandler.decrease()
    defconHandler.decrease()
    defconHandler.decrease()
