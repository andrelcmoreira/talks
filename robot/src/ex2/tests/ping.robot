*** Settings ***

Documentation  Suppose we are implementing a tool like ping, who the main goal is to check the
...            connectivity between two hosts. This suite contains the implementation of the tests
...            related to this tool.

Library        SSHLibrary
Library        ../lib/PingLib.py

Suite Setup     Suite setup
Suite Teardown  Suite teardown
#Test Setup      Test setup
#Test Teardown   Test teardown

*** Variables ***

${user}      host
${pass}      1234

${host1_ip}  172.17.0.4
${host2_ip}  172.17.0.5
${host3_ip}  172.17.0.7
${host5_ip}  172.17.0.8

#${cfg_file}     topology.json
${pkt_count}    10
#${host1}        host1
#${host2}        host2

*** Test cases ***

Ping a reachable host
    [Documentation]   This test validates the scenario where the 'host1' run the ping tool against
    ...               a reachable host 'host2'.
    Given I have a host with address "${host1_ip}" on network
    Given I have a host with address "${host2_ip}" on network

    #When I send "${pkt_count}" "echo request" packets to "${host2}" from "${host1}" using the ping tool
    #Then The host "${host2}" must receive "${pkt_count}" "echo request" packets from "${host1}"
    #And The host "${host1}" must receive "${pkt_count}" "echo reply" packets from "${host2}"

#Ping an unreachable host
#    [Documentation]   This test validates the scenario where the 'host1' run the ping tool against
#    ...               an unreachable host 'host2'.
#    Given I "have" a host with address "${host1_ip}" on network
#    Given I "do not have" a host with address "${host2_ip}" on network

    #When I send "${pkt_count}" "echo request" packets to "${host2}" from "${host1}" using the ping tool
    #Then The host "${host1}" must receive "0" "echo reply" packets from "${host2}"

*** Keywords ***

Suite setup
    Create a container named "host1" with image "ubuntu-demo"
    Create a container named "host2" with image "ubuntu-demo"
    Open Connection     ${host1_ip}
    Login               ${user}     ${pass}
    Open Connection     ${host2_ip}
    Login               ${user}     ${pass}

Suite teardown
    Destroy the container "host-1"
    Destroy the container "host-2"
    Close All Connections

#Test setup
#    # Start tcpdump on both machines
#    # Remove generated pcap files
#
#Test teardown
#    # Stop tcpdump on both machines
#    # Remove generated pcap files
