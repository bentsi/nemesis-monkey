import time
from abc import ABCMeta

from nemesis_monkey.nemesis import NemesisBase


class StopStartService(NemesisBase, metaclass=ABCMeta):

    def __init__(self, name: str, delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.delay = delay

    def run(self):
        self.target.run_cmd(f"systemctl stop {self.name}")
        time.sleep(self.delay)
        self.target.run_cmd(f"systemctl start {self.name}")
