from abc import ABCMeta
from pathlib import Path
from typing import Union

from nemesis_monkey.nemesis import NemesisBase


class FillDisk(NemesisBase, metaclass=ABCMeta):

    def __init__(self, target_dir: Union[str, Path], percentage: int):
        self.target_dir = target_dir
        self.percentage = percentage
        super().__init__()

    def run(self):
        # TODO: implement
        ...
