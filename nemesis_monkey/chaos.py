import random
from functools import partial
from typing import Callable
from typing import List
from typing import Optional

from nemesis_monkey.nemesis import NemesisBase
from nemesis_monkey.nemesis import Target


class ChoiceStrategy:
    @staticmethod
    def random() -> Callable:
        return random.choice

    @staticmethod
    def by_tag(tag: str) -> Callable:
        return partial(filter, lambda n: tag in n.tags)

    @staticmethod
    def sequential():
        """Just pick the Nemesis in the same order"""
        return lambda x: x


class Chaos:
    def __init__(
        self,
        repeat_cycles: int = 1,
        nemesis_choice_strategy: Callable = ChoiceStrategy.random(),
        targets_choice_strategy: Callable = ChoiceStrategy.random(),
    ):
        """
        :param repeat_cycles: Number of times to repeat the Nemesis list
        :param nemesis_choice_strategy: Strategy to choose Nemesis
        :param targets_choice_strategy: Strategy to choose targets
        """
        self._targets: Optional[List[Target]] = None
        self.repeat_cycles = repeat_cycles
        self.targets_choice_strategy = targets_choice_strategy
        self.nemesis_choice_strategy = nemesis_choice_strategy
        self.nemesis_list: List[NemesisBase] = []

    @property
    def targets(self) -> Optional[List[Target]]:
        if self._targets is None:
            # get from JSON
            # for RemoteServer get connection from airflow.hooks.base.BaseHook.get_connection(conn_id='')
            #     store SSH private key in extra
            ...
        return self._targets

    @targets.setter
    def targets(self, targets_list: List[Target]):
        self._targets = targets_list

    def _create_list_of_targets(self, num_nemesis):
        num_targets = len(self.targets)
        if num_nemesis == num_targets:
            return self.targets
        elif num_nemesis < num_targets:
            return self.targets[:num_nemesis]
        else:
            quotient, remainder = divmod(num_nemesis, num_targets)
            return self.targets * quotient + self.targets[:remainder]

    def apply(self, list_of_nemesis: list[NemesisBase]):
        self.nemesis_list = self.nemesis_choice_strategy(
            list_of_nemesis,
        ) * self.repeat_cycles
        targets = self.targets_choice_strategy(self.targets)
        for nemesis, target in zip(self.nemesis_list, targets):
            nemesis.target = target

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
