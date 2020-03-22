import math

from ..perception.perception_daemon import PerceptionDaemon


class Observer:

    def __init__(self, servos):
        self._servos = servos
        self._perception = PerceptionDaemon()

    def get_observations(self):
        obs = []
        # rex.GetMotorAngles
        for servo in self._servos.servo:
            obs.append(servo.angle)
        # rex.GetBaseOrientation
        obs.extend(self._perception.get_base_quaternion())
        return obs

    def termination(self):
        roll, pitch, _ = self._perception.get_base_orientation()
        if math.fabs(roll) > 0.3 or math.fabs(pitch) > 0.5:
            # TODO implement logging
            # print("Falling down!")
            return True
        return False
