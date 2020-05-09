import os

from adafruit_servokit import ServoKit

from rex_gym.agents.ppo import simple_ppo_agent
from rex_gym.agents.scripts import utility
from rex_gym.model.rex import Rex
from rex_gym.util import action_mapper, bullet_client
import tensorflow as tf

from motion.actuator import Actuator
from motion.observer import Observer
from util.singleton import Singleton
import logging


class MotionDaemon(metaclass=Singleton):
    STATIC_AGENTS = set()

    POSES = Rex.INIT_POSES

    def __init__(self):
        self._servos = ServoKit(channels=16)
        self._pybullet_client = bullet_client.BulletClient()
        self._observer = Observer(self._pybullet_client)
        self._actuator = Actuator(self._servos)
        for action_key in action_mapper.STATIC_ACTIONS_MAP.keys():
            self.STATIC_AGENTS.add(action_key)

    def set_position(self, pose=None, pose_id=None):
        try:
            if pose_id is None:
                self._actuator.set(pose)
            else:
                value = self.POSES[pose_id]
                logging.info(f"{pose_id}: {value}")
                self._actuator.set(value)
                logging.info('position set.')
        except Exception as ex:
            logging.exception(ex)

    def debug_pose(self):
        self._actuator.debug_pose()

    def set_gait(self, action_id, args=None, simulation=False):
        # @TODO Handle parametric policies
        # policy_dir, policy_check = action_mapper.DYNAMIC_ACTIONS_MAP[action_id]
        # with tempfile.TemporaryDirectory() as workpath:
        #     j2_env = Environment(loader=FileSystemLoader(workpath),
        #                          trim_blocks=True)
        #     lib_dir_path = os.path.join(str(site.getsitepackages()[0]), 'core')
        #     args['env_name'] = action_mapper.ACTIONS_TO_ENV_NAMES[action_id]
        #     config = j2_env.get_template(lib_dir_path + '/util/templates/config.j2').render(args)
        #     agent = self._load_agents(config, policy_dir + "/" + policy_check, False)
        # ------------------------------------------------------------------
        if action_id in self.STATIC_AGENTS:
            # this is a very poor hardcoded path
            # @ TODO
            gym_dir_path = '/usr/local/lib/python3.6/dist-packages/'
            # --------------------------------------------------------------
            log_dir, checkpoint = action_mapper.STATIC_ACTIONS_MAP[action_id]
            log_dir = os.path.join(gym_dir_path, log_dir)
            config = utility.load_config(log_dir)
            policy_layers = config.policy_layers
            value_layers = config.value_layers
            env = config.env(render=False)
            network = config.network
            with tf.Session() as sess:
                agent = simple_ppo_agent.SimplePPOPolicy(sess,
                                                         env,
                                                         network,
                                                         policy_layers=policy_layers,
                                                         value_layers=value_layers,
                                                         checkpoint=os.path.join(log_dir, checkpoint))
                logging.info(f'start gait_id={action_id}.')
                env.reset()
                while True:
                    obs = self._observer.get_observations(simulation)
                    action = agent.get_action([obs])
                    _, _, done, info = env.step(action[0])
                    self._actuator.set(info['action'], 0.003)
                    # @ TODO handle termination
                    # if self._observer.termination(done):
                    #     logging.info(f'gait_id={action_id} terminated.')
                    #     from control_unit.rex_daemon import RexDaemon
                    #     RexDaemon().stop("motion")
                    #     break
                    # time.sleep(0.36)
