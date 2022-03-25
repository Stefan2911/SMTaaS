import datetime
import random

from src.config.config import Config

config = Config()
connectivity_checking_hosts = config.get_connectivity_checking_hosts()
latencies = config.get_simulation_latencies()


class Simulation:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Simulation.__instance is None:
            Simulation()
        return Simulation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Simulation.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Simulation.__instance = self
        self.additional_latency = {}  # dictionary with host:additional_latency
        self.additional_waiting_time = {}
        self.additional_latency_general = 0
        self.additional_waiting_time_general = 0

    def get_additional_latency(self, host=None):
        if host is None:
            return self.additional_latency_general
        return self.additional_latency.get(host, self.additional_latency_general)

    def set_additional_latency(self, host, additional_latency):
        self.additional_latency[host] = additional_latency

    def get_additional_waiting_time(self, host=None):
        if host is None:
            return datetime.timedelta(seconds=self.additional_waiting_time_general)
        return datetime.timedelta(seconds=self.additional_waiting_time.get(host, self.additional_waiting_time_general))

    def set_additional_waiting_time(self, host, additional_waiting_time):
        self.additional_waiting_time[host] = additional_waiting_time

    def simulate_random_latency(self):
        random_latency = latencies[random.randrange(len(latencies))]
        self.simulate_latency(random_latency)

    def simulate_latency(self, latency):
        self.additional_latency_general = latency
        self.additional_waiting_time_general = latency * 0.005
        for host in connectivity_checking_hosts:
            self.set_additional_latency(host, latency)
            self.set_additional_waiting_time('http://' + host + ':5000/formulae', latency * 0.005)
