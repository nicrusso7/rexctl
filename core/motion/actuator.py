import math
import logging
import time


class Actuator:
    def __init__(self, servos):
        # This really depends on how precisely
        # your servos are aligned.
        self.scale_factors = {
            0: 88, 1: 100, 2: 105,
            3: 96, 4: 95, 5: 70,
            6: 102, 7: 86, 8: 120,
            9: 94, 10: 88, 11: 56
        }
        self.default_scale_factor = 90
        ####################################
        self._servos = servos
        # @TODO we can find something smarter..
        self._legs = {
            0: 0, 1: 0, 2: 0,
            3: 1, 4: 1, 5: 1,
            6: 2, 7: 2, 8: 2,
            9: 3, 10: 3, 11: 3
        }

    def debug_pose(self):
        try:
            for i in range(12):
                if i in self.scale_factors:
                    value = self.scale_factors[i]
                else:
                    value = self.default_scale_factor
                logging.info(f"Set motor_id={i} to {value}")
                self._servos.servo[i].angle = value
                time.sleep(0.03)
        except Exception as ex:
            logging.exception(ex)

    def set(self, action, sleep=0.03):
        try:
            for i in range(12):
                direction = action[i] if self._legs[i] % 2 else -action[i]
                if i in self.scale_factors:
                    value = self.scale_factors[i] + math.degrees(direction)
                else:
                    value = self.default_scale_factor + math.degrees(direction)
                logging.info(f"Set motor_id={i} to {value}")
                self._servos.servo[i].angle = value
                time.sleep(sleep)
        except Exception as ex:
            logging.exception(ex)

    def set_gait_pose(self, action):
        try:
            for i in range(12):
                value = math.degrees(action[i])
                logging.info(f"Set motor_id={i} to {value}")
                self._servos.servo[i].angle = value
                time.sleep(0.03)
        except Exception as ex:
            logging.exception(ex)
