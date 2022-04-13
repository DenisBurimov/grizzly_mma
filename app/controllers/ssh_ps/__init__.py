# cSpell:ignore paramiko
import time
from paramiko import SSHClient, AutoAddPolicy
from config import BaseConfig as conf

from app.logger import log


class SshShell(object):
    class Error(Exception):
        def __init__(self, message: str):
            self.message = message

    def __init__(self, host, user, passwd=None, port=22):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            host,
            port=port,
            username=user,
            password=passwd,
        )

    def exec_command(self, cmd: str):
        log(log.DEBUG, "RemoteShell: command [%s]", cmd)
        if not self.client:
            return None
        stdin, stdout, stderr = self.client.exec_command(cmd)
        error_lines = stderr.readlines()
        if error_lines:
            log(log.ERROR, "RemoteShell: error exec command [%s]", cmd)
            error_message = "\n".join([line.strip("\n\r") for line in error_lines])
            raise RemoteShell.Error(error_message)
        result = "\n".join([line.strip("\n\r") for line in stdout.readlines()])
        log(log.DEBUG, "RemoteShell: result [%s]", result)
        return result

    def send_command(self, cmd):
        log(log.DEBUG, "RemoteShell: command [%s]", cmd)
        BUFFER_SIZE = 1024
        with self.client.get_transport().open_session() as channel:
            channel.get_pty(width=1024)
            channel.settimeout(5)
            channel.exec_command(cmd + "\n")
            if channel.recv_stderr_ready():
                log(log.ERROR, "RemoteShell: Error")
                data = channel.recv_stderr(BUFFER_SIZE)
                error_message = data.decode()
                raise RemoteShell.Error(error_message)
            out_message = ""
            while True:
                data = channel.recv(BUFFER_SIZE)
                if not data:
                    break
                out_message += data.decode()
            return out_message

    def run_shell_command(self, cmd):
        with self.client.invoke_shell() as chan:
            while chan.recv_ready():
                time.sleep(1)
                chan.recv(1024)
            time.sleep(1)
            chan.send(f"{cmd}\n")
            return chan.recv(1024).decode()


class RemoteShell(SshShell):
    def __init__(self):
        if conf.REMOTE_SHELL_SERVER:
            super().__init__(
                conf.REMOTE_SHELL_SERVER,
                port=conf.REMOTE_SHELL_PORT,
                user=conf.REMOTE_SHELL_USER,
                passwd=conf.REMOTE_SHELL_PASS,
            )
        else:
            log(log.WARNING, "RemoteShell: please define REMOTE_SHELL_SERVER")
            self.client = None
