#-*- coding: utf-8 -*-
import select
import time
import paramiko

from utils import get_logger
#from exceptions import SSHSessionInactiveError

class SSHHandler(object):
    def __init__(self, host, port, user, password, save_path):
        # SSH Info
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.save_path = save_path

        self.logger = get_logger("SSHHandler")

        # Create SSH Session
        self.ssh_handler = paramiko.SSHClient()
        self.ssh_handler.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_handler.connect(
            hostname=host,
            port=port,
            username=user,
            password=password
        )
        self.logger.info("[+] Connect Success")

    def execute(self, command):
        session = self.ssh_handler.get_transport().open_session()
        if session.active:
            self.logger.info("[*] Executing command...")
            session.exec_command(command)
            self.logger.info("[*] Execute result below")
            return session
        else:
            raise ValueError("SSH Session Error")

    def start_capture(self, iface, pktcount, bpf_filter=None, bufsize=1024):
        self.logger.info("[+] Start Capture!")
        command = [
            "tcpdump",
            "-c {}".format(pktcount),
            "-i {}".format(iface),
            "-w {}".format(self.save_path),
        ]
        if bpf_filter is not None:
            command.append("-f \"{}\"".format(bpf_filter))

        command = ' '.join(command)
        self.logger.info("[*] Let's Execute \"{}\"".format(command))

        session = self.execute(command)

        while True:
            if session.exit_status_ready():
                self.logger.info("[+] session exit")
                break
            read_list, write_list, exceptional_list = select.select([session],[],[],0.0)
            if len(read_list) > 0:
                self.logger.info(session.recv(bufsize))
        self.logger.info("[+] Executed.")

    def remove_remote_file(self):
        self.logger.info("[*] Removing remote file {}".format(self.save_path))
        self.execute("rm -f {}".format(self.save_path))
        self.logger.info("[+] Remove complete.")

    def download_pcap(self, local_path, cleanup=True):
        self.logger.info("[*] Download Pcap file to {}".format(local_path))
        self.logger.info("[*] Opening sftp session...")
        sftp = self.ssh_handler.open_sftp()

        self.logger.info("[*] Downloading")
        sftp.get(self.save_path, local_path)

        self.logger.info("[*] Closing sftp session...")
        sftp.close()

        self.logger.info("[+] Download complete.")
        self.remove_remote_file()

    def close(self):
        self.ssh_handler.close()




