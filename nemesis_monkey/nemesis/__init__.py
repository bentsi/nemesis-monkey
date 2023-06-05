from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Optional

from nemesis_monkey.targets import Target


class NemesisBase(metaclass=ABCMeta):
    def __init__(self, timeout: int = 60):
        self.timeout = timeout  # seconds
        self._target: Optional[Target] = None

    @property
    @abstractmethod
    def tags(self) -> list:
        ...

    @property
    @abstractmethod
    def run(self) -> Any:
        ...

    @property
    def target(self) -> Target:
        assert self._target, "Target not set"
        return self._target

    @target.setter
    def target(self, target: Target):
        self._target = target
