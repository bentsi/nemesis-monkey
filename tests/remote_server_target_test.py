from dataclasses import dataclass
from io import StringIO
from time import sleep
from typing import Optional

import pytest
from docker.models.containers import Container
from paramiko.rsakey import RSAKey

from nemesis_monkey.targets.remote_server import RemoteSshServerTarget


@dataclass
class SshServerTestConnection:
    user: str = "root"
    password: Optional[str] = None
    port: int = 8022
    host: str = "localhost"
    private_key = RSAKey.generate(bits=1024)


@pytest.fixture(scope="function")
def ssh_server_with_password_auth():
    import docker
    client = docker.from_env()
    test_conn = SshServerTestConnection(password="Root!pass)")
    sshd_container: Container = client.containers.run(
        image="takeyamajp/ubuntu-sshd",
        name="nemesis-monkey-test-ssh-server",
        ports={'22/tcp': test_conn.port},
        environment={"ROOT_PASSWORD": test_conn.password},
        remove=True, detach=True,
    )
    sleep(2)  # wait until sshd starts running TODO: improve
    yield test_conn
    sshd_container.stop()


@pytest.fixture(scope="function")
def ssh_server_with_private_key_auth():
    import docker
    client = docker.from_env()
    test_conn = SshServerTestConnection(user="root")
    public_key = test_conn.private_key.get_base64()
    key_name = test_conn.private_key.get_name()
    sshd_container: Container = client.containers.run(
        image="takeyamajp/ubuntu-sshd",
        name="nemesis-monkey-test-ssh-server",
        ports={'22/tcp': test_conn.port},
        remove=True, detach=True,
    )
    sshd_container.exec_run(cmd="mkdir -m 700 -p /root/.ssh")
    sshd_container.exec_run(
        cmd=f"bash -c 'echo {key_name} {public_key} > /root/.ssh/authorized_keys'",
    )
    sshd_container.exec_run(cmd="chmod 600 /root/.ssh/authorized_keys")
    sleep(2)  # wait until sshd starts running TODO: improve
    yield test_conn
    sshd_container.stop()


@pytest.mark.targets
def test_remote_server_target_password_auth(ssh_server_with_password_auth):
    remote_ssh_server = RemoteSshServerTarget(
        host=ssh_server_with_password_auth.host,
        user=ssh_server_with_password_auth.user,
        password=ssh_server_with_password_auth.password,
        port=ssh_server_with_password_auth.port,
    )
    test_file_path = "/tmp/test_file"
    remote_ssh_server.run_cmd(cmd=f"touch {test_file_path}")
    remote_ssh_server.run_cmd(cmd=f"test -e {test_file_path}")


@pytest.mark.targets
def test_remote_server_target_private_key_auth(ssh_server_with_private_key_auth):
    private_key_str_io = StringIO()
    ssh_server_with_private_key_auth.private_key.write_private_key(
        file_obj=private_key_str_io,
    )
    private_key_str_io.seek(0)
    private_key_str = private_key_str_io.read()
    ssh_server_with_private_key_auth.private_key.write_private_key_file(
        "/tmp/pkey_test",
    )
    remote_ssh_server = RemoteSshServerTarget(
        host=ssh_server_with_private_key_auth.host,
        user=ssh_server_with_private_key_auth.user,
        private_key=private_key_str,
        port=ssh_server_with_private_key_auth.port,
    )
    test_file_path = "/tmp/test_file"
    remote_ssh_server.run_cmd(cmd=f"touch {test_file_path}")
    remote_ssh_server.run_cmd(cmd=f"test -e {test_file_path}")
