*** Settings ***

Documentation  Suppose we are implementing a tool like ping, who the main goal is to check the
...            connectivity between two hosts. This suite contains the implementation of the tests
...            related to this tool.

Library        ../lib/PingLib.py    ${cfg_file}

Suite Setup     Suite setup
Suite Teardown  Suite teardown
Test Setup      Test setup
Test Teardown   Test teardown

*** Variables ***

${pkt_count}    5

*** Test cases ***

Ping a reachable host
    [Documentation]   This test validates the scenario where the 'host1' run the ping tool against
    ...               a reachable host 'host2'.
    When I send ${pkt_count} packets to host2 from host1 using the ping tool
    Then The host host1 must receive ${pkt_count} reply packets from host2

*** Keywords ***

Suite setup
    Given I create a container named host1 with image "ubuntu-demo"
    And I create a container named host2 with image "ubuntu-demo"
    Then The container host1 is up
    And The container host2 is up

Suite teardown
    Given I destroy the container host1
    And I destroy the container host2
    Then The container host1 is down
    And The container host2 is down

Test setup
    I connect via ssh to host1
    I connect via ssh to host2

Test teardown
    I close the ssh connection with host1
    I close the ssh connection with host2
