""" Initialise and handle hardware (daemons) and external comms """
import asyncio
import random
from datetime import datetime

from .comms.blue_portal import BluePortal
from ..motion.motion_daemon import MotionDaemon
from ..perception.perception_daemon import PerceptionDaemon
from ..util.singleton import Singleton


class RexDaemon(metaclass=Singleton):

    DAEMONS_MAP = {}
    TASKS_MAP = {}

    def __init__(self):
        self.portal_task = asyncio.create_task(BluePortal().start())
        self.DAEMONS_MAP['motion'] = MotionDaemon()
        self.DAEMONS_MAP['perception'] = PerceptionDaemon()

    """ command dictionary: daemon_id -> command_id, args -> args """
    def exec(self, command):
        task_id = datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + '_' + \
                  str(random.randint(10000, 99999))
        args = eval(command['args'])
        args['task_id'] = task_id
        task = asyncio.create_task(
            getattr(
                self.DAEMONS_MAP[command.keys()[0]], command.values()[0]
            )
            (args)
        )
        self.TASKS_MAP[task_id] = task

    def stop(self, task_id):
        self.TASKS_MAP[task_id].cancel()
        del self.TASKS_MAP[task_id]
