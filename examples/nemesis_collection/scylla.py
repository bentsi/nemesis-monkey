from nemesis_monkey.nemesis.fill_disk import FillDisk
from nemesis_monkey.nemesis.reboot import RebootServer
from nemesis_monkey.nemesis.start_stop_service import StopStartService


class RebootScyllaNode(RebootServer):
    @property
    def tags(self) -> list:
        return ["basic-chaos"]


class RestartScyllaService(StopStartService):
    def __init__(self):
        super().__init__(name="scylla-server", delay=30)

    @property
    def tags(self) -> list:
        return ["basic-chaos"]


class FillScyllaDataPartition(FillDisk):
    def __init__(self):
        super().__init__(target_dir="/var/lib/scylla/data", percentage=100)

    @property
    def tags(self) -> list:
        return ["basic-chaos"]
