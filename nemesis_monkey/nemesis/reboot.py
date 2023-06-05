from nemesis_monkey.nemesis import NemesisBase


class RebootServer(NemesisBase):
    def run(self):
        self.target.run_cmd("reboot", sudo=True)


class RebootDockerContainer(NemesisBase):
    ...
