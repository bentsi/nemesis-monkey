from io import StringIO
from typing import Optional

from fabric import Connection
from paramiko.rsakey import RSAKey

from nemesis_monkey.targets import Target


class RemoteSshServerTarget(Target):
    def __init__(
        self, host: str, user: str, password: Optional[str] = None, private_key: Optional[str] = None, port: int = 22,
        connect_timeout: int = 10,
    ):
        self.private_key = private_key
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connect_timeout = connect_timeout

    def connect(self):
        connect_kwargs = {"banner_timeout": 10}
        if self.private_key:
            connect_kwargs = {
                "pkey": RSAKey.from_private_key(
                    file_obj=StringIO(self.private_key),
                ),
            }
        elif self.user and self.password:
            connect_kwargs = {"password": self.password}
        connection = Connection(
            host=self.host, user=self.user, port=self.port, connect_timeout=self.connect_timeout,
            connect_kwargs=connect_kwargs,
        )
        return connection

    def run_cmd(self, cmd: str, sudo: bool = False, bash_wrap: bool = True):
        if bash_wrap:
            cmd = f'bash -cxe "{cmd}"'
        with self.connect() as ssh_connection:
            if sudo:
                result = ssh_connection.sudo(cmd)
            else:
                result = ssh_connection.run(cmd)
            return result
