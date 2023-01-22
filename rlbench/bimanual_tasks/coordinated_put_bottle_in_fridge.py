from typing import List, Tuple
import numpy as np
from pyrep.objects.object import Object
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.conditions import NothingGrasped
from rlbench.backend.task import BimanualTask
from collections import defaultdict


class CoordinatedPutBottleInFridge(BimanualTask):

    def init_task(self) -> None:
        bottle = Shape('bottle')
        self.register_graspable_objects([bottle])
        self.register_success_conditions(
            [DetectedCondition(bottle, ProximitySensor('success')),
             NothingGrasped(self.robot.right_gripper), NothingGrasped(self.robot.left_gripper)])
        
        self.waypoint_mapping = defaultdict(lambda: 'left')
        for i in range(4):
            self.waypoint_mapping[f'waypoint{i}'] = 'right'

    def init_episode(self, index: int) -> List[str]:
        return ['put bottle in fridge',
                'place the bottle inside the fridge',
                'open the fridge and put the bottle in there',
                'open the fridge door, pick up the bottle, and leave it in the '
                'fridge']

    def variation_count(self) -> int:
        return 1

    def boundary_root(self) -> Object:
        return Shape('fridge_root')

    def base_rotation_bounds(self) -> Tuple[Tuple[float, float, float],
                                            Tuple[float, float, float]]:
        return (0.0, 0.0, -np.pi / 4), (0.0, 0.0, np.pi / 4)