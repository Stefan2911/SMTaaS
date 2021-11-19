"""
When a configuration differs for simulated and LEGO robot, the configuration
values are given in the form [VALUE_FOR_SIMULATED_ROBOT, VALUE_FOR_LEGO_ROBOT].
If only one value is given, it is either the same for both robots or it is only
required by one robot.
"""

import logging

from src.slam.common.enums import RobotType

logging.basicConfig()
logger = logging.getLogger('config')
logger.setLevel(level=logging.DEBUG)


class Config(object):
    # Both robots
    ROBOT_SIZE = [10.0, 25.0]
    SCANNING_PRECISION = 20
    VIEW_ANGLE = 330

    # Simulated robot
    WORLD_NUMBER = 3
    LIMITED_VIEW = 30.0  # Set to None to allow measurements up to infinity

    # LEGO Mindstorms robot (Socket)
    HOST = "10.0.0.18"
    PORT = 50000

    # Save
    SAVE = False
    SAVE_FOLDER = "out"
    SAVE_FILENAME_PREFIX = "img_"
    SAVE_PARAMS = {
        "format": "png",
    }

    # END OF CONFIGURATION. The rest are just some utility methods.

    def __init__(self):
        self.rtype = None

    def setup(self, rtype: RobotType):
        if self.rtype is not None:
            logger.warning("Setup already completed. Nothing changed.")
            return
        self.rtype = rtype

    def __getattr__(self, name: str):
        """
        Fallback if __getattribute__ raises exception.
        """
        object.__getattr__(self, name)

    def __getattribute__(self, name: str):
        value = object.__getattribute__(self, name)
        if isinstance(value, list):
            if len(value) >= 2:
                if self.rtype == RobotType.SIMULATED:
                    return value[0]
                elif self.rtype == RobotType.LEGO:
                    return value[1]
                else:
                    raise RuntimeError("Config.rtype is unset or has a " +
                                       "wrong value")
            if len(value) == 1:
                return value[0]
            raise ValueError(f"Missing configuration value for {name}")
        return value


config = Config()
