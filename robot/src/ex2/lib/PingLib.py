from robot.api.deco import keyword
from json import load
from paramiko import SSHClient, AutoAddPolicy
from docker import from_env
from docker.errors import NotFound
from re import search

class PingLib(object):

    """Implementation of PingLib used on ping tool tests."""

    def __init__(self, cfg_file):
        """
        Initialize object attributes.

        Args:
            cfg_file (str): Name of config file.

        Raises:
            FileNotFoundError: When the specified doesn't exist.
        """
        try:
            self.__ping_output = ''
            self.__containers = {}
            self.__ssh_clients = {}

            with open(cfg_file) as file:
                self.__topology = load(file)
        except FileNotFoundError as e:
            raise e

    @keyword("The container ${name} is ${state}")
    def check_container_state(self, name, state):
        """
        Check the operational state of a given container.

        Args:
            name (str): Name of container.
            state (str): The operational state of container (up or down).

        Raises:
            AssertionError: When an assert error ocurrs.
        """
        client = self.__containers[name]['client']

        for container in client.containers():
            if container['Names'][0] == ('/' + name):
                if state == 'down' and container['State'] == 'running':
                    raise AssertionError('The container {} is up!'.format(name))
                if state == 'up' and container['State'] != 'running':
                    raise AssertionError('The container {} is down!'.format(name))

    @keyword("I send ${pkt_count} packets to ${hostname_2} from ${hostname_1} using the ping tool")
    def ping(self, pkt_count, hostname_2, hostname_1):
        """
        Send a given number of packets from the host 'hostname_1' to host 'hostname_2' using ping.

        Args:
            pkt_count (str): Number of packets to be send.
            hostname_2 (str): Name of target host.
            hostname_1 (str): Name of source host.
        """
        ip = self.__topology[hostname_2]['ip']

        client = self.__ssh_clients[hostname_1]
        _,stdout,_ = client.exec_command('ping -c ' + pkt_count + ' ' + ip)
        self.__ping_output = stdout.read().decode('ascii')

    @keyword("The host ${hostname_1} must receive ${pkt_count} reply packets from ${hostname_2}")
    def must_receive(self, hostname_1, pkt_count, hostname_2):
        """
        Check if a given number of packets was received from 'hostname_2' to 'hostname_1'.

        Args:
            hostname_1 (str): Name of source host.
            pkt_count (str): Number of packets to be send.
            hostname_2 (str): Name of target host.

        Raises:
            AssertionError:
        """
        ip = self.__topology[hostname_2]['ip']

        for i in range(1, int(pkt_count) + 1):
            pattern = '64 bytes from %s: icmp_seq=%d ttl=\d\d time=\d.\d\d\d ms\n' % (ip, i)

            if search(pattern, self.__ping_output) is None:
                raise AssertionError('pattern not found!')

    @keyword('I create a container named ${container_name} with image ${image}')
    def create_container(self, container_name, image):
        """
        Create a new container using the specified image.

        Args:
            container_name (str): The container name.
            image (str): The image name used to build the container.

        Raises:
            RunTimeError: When the specified image doesn't exist.
        """
        try:
            client = from_env()
            client.inspect_image('ubuntu-demo') # check if the image exists.
            demo_container = client.create_container('ubuntu-demo', name=container_name)

            client.start(container=demo_container.get('Id'))

            self.__containers[container_name] = { 'client': client, 'container': demo_container }
        except NotFound:
            raise RuntimeError("the container image wasn't found, aborting the execution!")

    @keyword('I destroy the container ${name}')
    def destroy_container(self, name):
        """
        Destroy an existing container.

        Args:
            name (str): Name of container to be destroyed.
        """
        client = self.__containers[name]['client']
        demo_container = self.__containers[name]['container']

        client.stop(container=demo_container.get('Id'))
        client.remove_container(container=demo_container.get('Id'))

    @keyword('I connect via ssh to ${hostname}')
    def connect_ssh(self, hostname):
        """
        Open a ssh connection to a given host.

        Args:
            hostname (str): Name of host.
        """
        ip = self.__topology[hostname]['ip']
        user = self.__topology[hostname]['user']
        pswd = self.__topology[hostname]['pass']

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=user, password=pswd)

        self.__ssh_clients[hostname] = client

    @keyword('I close the ssh connection with ${hostname}')
    def disconnect_ssh(self, hostname):
        """
        Close the ssh connection to a given host.

        Args:
            hostname (str): Name of host.
        """
        client = self.__ssh_clients[hostname]
        client.close()
