from collections import defaultdict
from typing import List, Tuple

import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.conditions import NothingGrasped
from rlbench.backend.task import BimanualTask
from rlbench.backend.spawn_boundary import SpawnBoundary
from pyrep.objects.dummy import Dummy


class HandoverItemEasy(BimanualTask):

    def init_task(self) -> None:

        self.item = Shape('item')

        self.register_graspable_objects([self.item])

        self.waypoint_mapping = defaultdict(lambda: 'left')
        self.waypoint_mapping.update({'waypoint0': 'right', 'waypoint5': 'right'})

        self.boundaries = Shape('handover_item_boundary')


    def init_episode(self, index: int) -> List[str]:

        self._variation_index = index

        right_success_sensor = ProximitySensor('Panda_rightArm_gripper_attachProxSensor')
        left_success_sensor = ProximitySensor('Panda_leftArm_gripper_attachProxSensor')

        #b = SpawnBoundary([self.boundaries])
        #b.clear()
        #    b.sample(item, min_distance=0.1)

        self.register_success_conditions(
            [DetectedCondition(self.item, right_success_sensor),  
             DetectedCondition(self.item, left_success_sensor, negated=True)])

        return [f'bring me the item',
                f'hand over the object']

    def variation_count(self) -> int:
        return 1

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, - np.pi / 8], [0, 0, np.pi / 8]
