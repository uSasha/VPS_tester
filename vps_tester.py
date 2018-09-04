import logging
import time

import paramiko
from hetznercloud import HetznerActionException
from hetznercloud import HetznerCloudClient
from hetznercloud import HetznerCloudClientConfiguration
from hetznercloud import constants

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger('vps_test')


class HetznerTester:
    def __init__(self, hetzner_api_key, ssh_key_file_name):
        configuration = HetznerCloudClientConfiguration().with_api_key(hetzner_api_key).with_api_version(1)
        self.client = HetznerCloudClient(configuration)
        self.key_pub = self.find_or_create_key(ssh_key_file_name=ssh_key_file_name)
        self.ssh_key_file_name = ssh_key_file_name
        self.server_counter = 0

    def find_or_create_key(self, ssh_key_file_name):
        for key in self.client.ssh_keys().get_all():
            if key.name == 'vps_test':
                return key
        # not found, create one
        with open(ssh_key_file_name, 'r') as f:
            key_pub = f.readlines()[0]
        key = self.client.ssh_keys().create(name='vps_test', public_key=key_pub)
        return key

    def create_server(self, vps_type, datacenter):
        self.server_counter += 1
        try:
            server, create_action = self.client.servers().create(name=f'cpu-test-server-{self.server_counter}',
                                                                 server_type=vps_type,
                                                                 image=constants.IMAGE_UBUNTU_1804,
                                                                 datacenter=datacenter,
                                                                 start_after_create=True,
                                                                 ssh_keys=[self.key_pub.name],
                                                                 )
            server.wait_until_status_is(constants.SERVER_STATUS_RUNNING)
        except Exception as e:
            logger.error(e)
            server = self.create_server(vps_type, datacenter)

        return server

    @staticmethod
    def delete_server(server):
        try:
            action = server.delete()
            action.wait_until_status_is(constants.ACTION_STATUS_SUCCESS)
        except HetznerActionException:
            logger.warning(f'no such server with name {server.name} and id {server.id}')

    def run_ssh_command(self, server, command, print_errors=False):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username='root', key_filename=self.ssh_key_file_name)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

        e = ssh_stderr.read()
        if print_errors and len(e):
            logger.warning(e)

        result = ssh_stdout.read()
        ssh.close()
        return result

    def test_vps(self, datacenter, vps_type, kill_instantly=True):
        server = self.create_server(vps_type, datacenter)
        ip = server.public_net_ipv4
        logger.debug('server created, going to sleep 30 seconds')
        time.sleep(30)
        logger.debug('woke up')
        self.run_ssh_command(ip,
                             '''
                             apt-get update \
                             && apt-get install docker.io -y \
                             ''',
                             print_errors=True,
                             )
        t = self.run_ssh_command(ip, 'docker run usasha/vps_test', print_errors=False)
        logger.debug('test complete')
        if kill_instantly:
            self.delete_server(server)
            server = None
            logger.debug('server deleted')

        try:
            t = int(t)
        except ValueError:
            pass

        return t, server
