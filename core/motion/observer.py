import ast
import math
import os

from perception.perception_daemon import PerceptionDaemon
import logging


class Observer:

    def __init__(self, bullet_client):
        self._perception = PerceptionDaemon()
        self._pybullet_client = bullet_client

        # this is a very poor hardcoded path
        # @ TODO
        lib_dir_path = '/usr/local/lib/python3.6/dist-packages/'
        # --------------------------------------------------------------
        try:
            self._sim = []
            self._line_counter = 0
            with open(os.path.join(lib_dir_path, 'util/sim/gyro_data')) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    # @TODO vulnerability!
                    self._sim.append(ast.literal_eval(line))
                    # --------------------------------------
        except FileNotFoundError:
            logging.info('simulation data not found.')

    def get_observations(self, simulation):
        obs = []
        if simulation:
            # the simulation has 620 steps.
            if self._line_counter > 619:
                self._line_counter = 0
            obs = self._sim[self._line_counter]
            self._line_counter += 1
        else:
            # rex.GetBaseOrientation
            obs.extend(list(self._pybullet_client.getQuaternionFromEuler(self._perception.get_base_orientation())))
        logging.info(f"observation={obs}")
        return obs

    def termination(self):
        roll, pitch, _ = self._perception.get_base_orientation()
        if math.fabs(roll) > 0.3 or math.fabs(pitch) > 0.5:
            logging.info("Falling down!")
            return True
        return False
