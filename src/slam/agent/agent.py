import logging
import queue
import random
import threading
import time

import src.slam.common.datapoint as datapoint

logging.basicConfig()
logger = logging.getLogger('agent')
logger.setLevel(level=logging.DEBUG)


class Agent(threading.Thread):
    def __init__(self, data_queue: queue.Queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.shutdown_flag = threading.Event()
        logger.info(f"Using agent: {type(self).__name__}")

    def run(self):
        success = True
        while not self.shutdown_flag.is_set() and success:
            success = self.perform_action()
        self.die()

    def perform_action(self):
        """
        Dummy action
        """
        logger.info("Alive")
        time.sleep(1)
        if random.random() < 0.9:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            if random.random() < 0.5:
                data = datapoint.Observation(x, y)
            else:
                data = datapoint.Pose(x, y, 0)
            self.data_queue.put(data)
        return True

    def die(self):
        logger.info("Dead")
