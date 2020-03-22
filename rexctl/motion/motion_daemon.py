import os
import site
import tempfile

from adafruit_servokit import ServoKit

from rex_gym.agents.ppo import simple_ppo_agent
from rex_gym.agents.scripts import utility
from rex_gym.model.rex import Rex
from rex_gym.util import action_mapper
import tensorflow as tf

from .actuator import Actuator
from .observer import Observer
from ..util.singleton import Singleton
from jinja2 import Environment, FileSystemLoader


class MotionDaemon(metaclass=Singleton):
    STATIC_AGENTS = {}

    POSES = Rex.INIT_POSES

    def __init__(self):
        self._servos = ServoKit(channels=16)
        self._observer = Observer(self._servos)
        self._actuator = Actuator(self._servos)
        for action_key in action_mapper.STATIC_ACTION_MAP.keys():
            log_dir, checkpoint = action_mapper.STATIC_ACTION_MAP[action_key]
            self.STATIC_AGENTS[action_key] = self._load_agents(log_dir, log_dir + "/" + checkpoint, False)

    async def set_position(self, pose, task_id, pose_id=None):
        if pose_id is None:
            self._actuator.set(pose)
        else:
            self._actuator.set(self.POSES[pose_id])
        from control_unit.rex_daemon import RexDaemon
        RexDaemon().stop(task_id)

    async def set_gait(self, action_id, args, task_id):
        if action_id in self.STATIC_AGENTS.keys():
            agent = self.STATIC_AGENTS[action_id]
        else:
            policy_dir, policy_check = action_mapper.INTERACTIVE_ACTION_MAP[action_id]
            with tempfile.TemporaryDirectory() as workpath:
                j2_env = Environment(loader=FileSystemLoader(workpath),
                                     trim_blocks=True)
                lib_dir_path = os.path.join(str(site.getsitepackages()[0]), 'rexctl')
                config = j2_env.get_template(lib_dir_path + '/util/templates/config.j2').render(
                    args=args,
                    env_name=action_mapper.ENV_NAMES[action_id])
                agent = self._load_agents(config, policy_dir + "/" + policy_check, True)
        while True:
            obs = self._observer.get_observations()
            action = agent.get_action([obs])
            self._actuator.set(action[0])
            if self._observer.termination():
                from control_unit.rex_daemon import RexDaemon
                RexDaemon().stop(task_id)
                break

    @staticmethod
    def _load_agents(config_path, checkpoint_path, is_stream):
        config = utility.load_config(config_path, is_stream)
        policy_layers = config.policy_layers
        value_layers = config.value_layers
        env = config.env()
        network = config.network
        with tf.Session() as sess:
            agent = simple_ppo_agent.SimplePPOPolicy(sess,
                                                     env,
                                                     network,
                                                     policy_layers=policy_layers,
                                                     value_layers=value_layers,
                                                     checkpoint=checkpoint_path)
            return agent
