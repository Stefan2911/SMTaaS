import os
import random
import threading
import time

import yaml
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class Config:

    def __init__(self):
        self.file_path = "src/config/config.yaml"
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=self.watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def on_modified(self, event):
        if event.src_path.endswith(os.path.basename(self.file_path)):
            with open(self.file_path, "r") as changed_configfile:
                self.data = yaml.load(changed_configfile, Loader=yaml.FullLoader)

    def watch_config(self):
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = True
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_modified = self.on_modified
        my_observer = Observer()
        my_observer.schedule(my_event_handler, os.path.dirname(self.file_path) + os.sep, recursive=False)
        my_observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            my_observer.stop()
        my_observer.join()

    # general
    def get_logging_level(self):
        return self.data['logging-level']

    # decision reinforcement learning
    def get_training_problem_directory(self):
        if self.is_ev3():
            return self.data['decision']['reinforcement-learning']['training-smt-problem-directory-robot']
        return self.data['decision']['reinforcement-learning']['training-smt-problem-directory-edge']

    def is_mode_active(self, mode):
        return self.data['decision']['reinforcement-learning']['reward-modes'][mode.value]['active']

    def get_reward_ranges(self, mode):
        if 'ranges' in self.data['decision']['reinforcement-learning']['reward-modes'][mode.value]:
            return self.data['decision']['reinforcement-learning']['reward-modes'][mode.value]['ranges']
        return []

    def get_solver_instances(self):
        if self.is_ev3():
            return self.data['instances']['edge']
        return self.data['instances']['cloud']

    def get_solver_instance(self, index):
        return self.get_solver_instances()[index]

    def get_action_space(self):
        return len(self.get_solver_instances()) + 1  # number of instances to offload + solve locally

    def get_common_hyper_parameters(self):
        return self.data['decision']['reinforcement-learning']['common-hyper-parameters']

    # decision reinforcement learning q-learning
    def get_q_table_location(self):
        return self.data['decision']['reinforcement-learning']['q-learning']['q-table-location']

    # decision reinforcement learning dqn
    def get_dqn_hyper_parameters(self):
        return self.data['decision']['reinforcement-learning']['deep-q-network']['hyper-parameters']

    def get_neural_network_location(self):
        return self.data['decision']['reinforcement-learning']['deep-q-network']['neural-network-location']

    # ev3
    def is_ev3(self):
        return self.data['ev3']['in-use']

    def get_directory_to_observe(self):
        return self.data['ev3']['smt']['watch-directory']

    # monitoring
    def get_connectivity_checking_hosts(self):
        if self.is_ev3():
            return self.data['monitoring']['connectivity']['hosts']['edge']
        else:
            return self.data['monitoring']['connectivity']['hosts']['cloud']

    def get_connectivity_checking_host(self):
        hosts = self.get_connectivity_checking_hosts()
        random_index = random.randrange(len(hosts))
        return hosts[random_index]

    def get_indicator_ranges(self, indicator):
        return self.data['monitoring']['indicators'][indicator]

    def get_state_update_period(self):
        return self.data['monitoring']['update-period']

    def is_training_active(self):
        return self.data['monitoring']['is-training-active']

    def get_max_rtt(self):
        return self.data['monitoring']['connectivity']['max-rtt']

    def get_max_problem_complexity(self):
        return self.data['monitoring']['max-problem-complexity']

    # smt
    def get_solver_location(self):
        return self.data['smt']['solver-location']

    def get_decision_mode(self):
        return self.data['smt']['decision-mode']

    # instances
    def get_cloud_instances(self):
        return self.data['instances']['cloud']

    def get_edge_instances(self):
        return self.data['instances']['edge']

    def get_uplink_cost(self):
        return self.data['uplink-cost']

    def get_invocation_cost(self):
        return self.data['invocation-cost']

    # simulation
    def get_simulation_latencies(self):
        return self.data['simulation']['latencies']
