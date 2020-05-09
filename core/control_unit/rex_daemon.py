""" Initialise and handle hardware (daemons) and external comms """
import multiprocessing

from motion.motion_daemon import MotionDaemon
from perception.perception_daemon import PerceptionDaemon
from util.singleton import Singleton
import logging


class RexDaemon(metaclass=Singleton):

    DAEMONS_MAP = {}
    TASKS_MAP = {}

    def __init__(self):
        self.DAEMONS_MAP['motion'] = MotionDaemon()
        self.DAEMONS_MAP['perception'] = PerceptionDaemon()

    def exec(self, command):
        try:
            logging.info('Start execution.')
            args = dict(command['command_args'])
            task = multiprocessing.Process(target=self._run, args=(command, args))
            task.daemon = True
            task.start()
            self.TASKS_MAP[command['daemon_id']] = task
        except Exception as ex:
            logging.exception(ex)

    def stop(self, task_id):
        t = self.TASKS_MAP[task_id]
        t.terminate()
        logging.info(f"task_id={t} terminated")
        del self.TASKS_MAP[task_id]

    def stop_all(self):
        for t in self.TASKS_MAP:
            self.TASKS_MAP[t].terminate()
            logging.info(f"task_id={t} terminated")
        self.TASKS_MAP = {}
        logging.info("task_map is now empty")

    def debug_pose(self):
        self.DAEMONS_MAP['motion'].debug_pose()

    def get_calibration(self):
        return [self.DAEMONS_MAP['perception'].get_calibration_status(),
                self.DAEMONS_MAP['perception'].get_mode()]

    def store_calibration(self):
        self.DAEMONS_MAP['perception'].store_calibration()

    def _run(self, command, args):
        getattr(
            self.DAEMONS_MAP[command['daemon_id']], command['command_id']
        )(**args)
