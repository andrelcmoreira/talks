from robot.api.deco import keyword
from json import load
from os import system
from docker import from_env
from docker.errors import NotFound

class PingLib(object):

    """"""

    #def __init__(self, cfg_file_path):
    #    """"""
    #    self.__containers = {}

    #    try:
    #        with open(cfg_file_path, 'r') as cfg_file:
    #            self.__cfg_data = load(cfg_file)
    #    except Exception as e:
    #        raise e

    @keyword("I ${option} a host with address ${host_ip} on network")
    def check_host(self, option, host_ip):
        """
        Check if a given host is online or offline on network.

        Args:
            option (str): Must be 'have' (when we want to check if a host is available) or
            'do not have' (when we check if the host is not available).
            host_ip (str): Ip of host.
        Raises:
            AssertionError: When an assert error ocurrs.
        """
        cmd = 'ping -c 2 ' + host_ip
        ret = system(cmd)

        if option == "have" and ret == 256:
            raise AssertionError("The specified address is offline!")
        elif option == 'do not have' and ret == 0:
            raise AssertionError("The specified address is online!")

    @keyword("I send ${pkt_count} ${pkg_type} packets to ${hostname_2} from ${hostname_1} using the ping tool")
    def ping(self, pkt_count, pkt_type, hostname_2, hostname_1):
        """"""
        pass

    @keyword("The host ${hostname_1} must receive ${pkt_count} ${pkt_type} packets from ${hostname_2}")
    def must_receive(self, hostname_1, pkt_count, pkt_type, hostname_2):
        """"""
        pass

    @keyword('Create a container named ${host1} with image ${image}')
    def create_container(self, name, image):
        pass
        #try:
        #    client = from_env()
        #    client.inspect_image('ubuntu-demo') # check if the image exists.
        #    db_container = client.create_container('ubuntu-demo')

        #    client.start(container=db_container.get('Id')) # setup

        #except NotFound:
        #    raise RuntimeError("the container image wasn't found, aborting the execution!")

    @keyword('Destroy the container ${name}')
    def destroy_container(self, name):
        pass
