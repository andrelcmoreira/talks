*** Settings ***

Documentation  IT'S NOT MANDATORY, BUT YOU CAN PUT THE DOCUMENTATION OF TEST SUITE HERE!
Library        ../lib/DemoLib.py

Suite Setup     My suite setup
Suite Teardown  My suite teardown
Test Setup      My test setup
Test Teardown   My test teardown

*** Variables ***

${variable}  Robot is cool!

*** Test cases ***

Test case
    [Documentation]   This is a sample test case. In 'documentation' section, we can provide some
    ...               information about the test like, what is being tested and the expected results.
    [Tags]            TagSuccess
    Hello, I'm a custom keyword

Another test case
    [Documentation]   This is another test.
    [Tags]            TagSuccess
    Hello, I'm a custom keyword with parameter "${variable}"

Another test case with failure
    [Documentation]   This is a test case with failure.
    [Tags]            TagFailure
    Hello, I'm a costuom keyword who will fail

*** Keywords ***

My suite setup
    Log To Console  "Hi, I'm the suite setup"

My suite teardown
    Log To Console  "Hi, I'm the suite teardown"

My test setup
    Log To Console  "Hi, I'm the test setup"

My test teardown
    Log To Console  "Hi, I'm the test teardown"
