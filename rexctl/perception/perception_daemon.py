from .fusion.bno_sensor import BNOSensor


class PerceptionDaemon:

    def __init__(self):
        self._bno_sensor = BNOSensor()

    def get_base_orientation(self):
        return self._bno_sensor.euler()

    def get_base_quaternion(self):
        return self._bno_sensor.quaternion()

    def get_linear_acceleration(self):
        return self._bno_sensor.linear_acceleration()

    def get_acceleration(self):
        return self._bno_sensor.acceleration()

    def get_temperature(self):
        return self._bno_sensor.temperature()
