class Actuator:
    def __init__(self, servos):
        self.scale_factor = 90
        self._servos = servos

    # TODO scale input
    def set(self, action):
        for i in range(len(action)):
            self._servos.servo[i].angle = action[i]
