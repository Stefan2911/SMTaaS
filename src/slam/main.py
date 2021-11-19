import logging
import os
import sys
import time

import src.slam.driver as sdriver
from src.slam.common.enums import RobotType
from src.slam.config import config

if __name__ == "__main__":
    logging_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logging_format, datefmt="%H:%M:%S")
    logger = logging.getLogger('main')
    logger.setLevel(level=logging.DEBUG)

    argv = sys.argv[1:]
    rtype = RobotType.SIMULATED

    for a in argv:
        if a.upper() in ("LEGO", "L"):
            rtype = RobotType.LEGO
            break
    config.setup(rtype)

    save = config.SAVE
    filename = None

    if save:
        save_folder = f"{config.SAVE_FOLDER}/" \
                      f"{time.strftime('%Y-%m-%d_%H-%M-%S')}"
        try:
            os.mkdir(save_folder)
            filename = f"{save_folder}/{config.SAVE_FILENAME_PREFIX}"
            logger.info(f"Images saved as {filename}*")
        except OSError:
            logger.error(f"Could not create a directory '{save_folder}'. "
                         "Images will not be saved.")
            save = False

    sdriver.run(rtype, save=save, filename=filename)
