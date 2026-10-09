"""HIMLoco velocity task for the Unitree Go1 asset bundled with this project."""

from isaaclab.assets import ArticulationCfg
from isaaclab.utils import configclass

from himloco_lab.assets.unitree import UNITREE_GO1_CFG
from himloco_lab.tasks.locomotion import mdp
from himloco_lab.tasks.locomotion.robots.go2.velocity_env_cfg import (
    RobotEnvCfg as Go2RobotEnvCfg,
    RobotSceneCfg as Go2RobotSceneCfg,
)


@configclass
class RobotSceneCfg(Go2RobotSceneCfg):
    """The common HIMLoco scene with a Go1 articulation."""

    robot: ArticulationCfg = UNITREE_GO1_CFG.replace(
        prim_path="{ENV_REGEX_NS}/Robot"
    )


@configclass
class RobotEnvCfg(Go2RobotEnvCfg):
    """Go1 training configuration at the upstream 50 Hz policy rate."""

    scene: RobotSceneCfg = RobotSceneCfg(num_envs=4096, env_spacing=2.5)

    def __post_init__(self):
        super().__post_init__()
        # Go1 and the original HIMLoco Go1 policy use 200 Hz physics and
        # 50 Hz policy actions.  Keep all common terrain, observation, reward,
        # curriculum and randomization terms identical to the Go2 task.
        self.sim.dt = 0.005
        self.decimation = 4
        self.sim.render_interval = self.decimation
        self.scene.contact_forces.update_period = self.sim.dt * self.decimation
        self.scene.height_scanner.update_period = self.sim.dt * self.decimation
        self.scene.base_height_scanner.update_period = self.sim.dt * self.decimation
        self.rewards.base_height_l2.params["target_height"] = 0.30
        self.rewards.feet_height_body.params["target_height"] = -0.20


@configclass
class RobotPlayEnvCfg(RobotEnvCfg):
    """Small deterministic Go1 scene for playback and export."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 64
        self.scene.terrain.terrain_generator.num_cols = 10
        self.scene.terrain.max_init_terrain_level = 10
        self.scene.terrain.terrain_generator.curriculum = True
        self.commands.base_velocity.heading_command = False
        self.commands.base_velocity.ranges = (
            mdp.UniformLevelVelocityCommandCfg.Ranges(
                lin_vel_x=(1.0, 1.0),
                lin_vel_y=(0.0, 0.0),
                ang_vel_z=(0.0, 0.0),
            )
        )
        self.commands.base_velocity.low_vel_env_lin_x_ranges = (1.0, 1.0)
        self.events.add_base_mass = None
        self.events.randomize_rigid_body_com = None
        self.events.push_robot = None
