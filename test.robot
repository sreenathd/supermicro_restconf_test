*** Settings ***
Library       OperatingSystem
Library       RestConf
Library    Collections

*** Variables ***
${MESSAGE}    Hello, world!

*** Test Cases ***
Get Hostname
    ${result}=  get    system:system/config
    Should Be Equal  ${result.status_code}  ${200}
    ${json}=  Set Variable  ${result.json()}
    Log    ${json}
Put Hostname
    ${putresult}=  put    system:system/config    {"config":{"hostname":"Switch1"}}
    Should Be Equal  ${putresult.status_code}  ${200}
    ${result}=  get    system:system/config
    Should Be Equal  ${result.status_code}  ${200}
    ${json}=  Set Variable  ${result.json()}
    Log    ${json}
    json property should equal    ${json}    openconfig-system:system    {"config":{"hostname":"Switch1"}}  
Post Vlan
    ${postresult}=    post    vlan:vlans    {"vlan-id":33}
    Should Be Equal  ${postresult.status_code}  ${204}
    ${result}=  get    vlan:vlans/vlan=33/config/vlan-id
    Should Be Equal  ${result.status_code}  ${200}
    ${json}=  Set Variable  ${result.json()}
    Log    ${json}
    json property should equal    ${json}    openconfig-vlan:vlans    {"vlan":[{"config":{"vlan-id":33},"vlan-id":33}]}
Patch Vlan
    ${patchresult}=    patch    vlan:vlans/vlan=33/config/vlan-id    {"config":{"name":"lab-test-vlan"},"vlan-id":33}
    Should Be Equal  ${patchresult.status_code}  ${204}
    ${result}=  get    vlan:vlans/vlan=33/config/vlan-id
    Should Be Equal  ${result.status_code}  ${200}
    ${json}=  Set Variable  ${result.json()}
    Log    ${json}
    json property should equal    ${json}    openconfig-vlan:vlans    {"vlan":[{"config":{"name":"lab-test-vlan"},"vlan-id":33}]}   
Delete VLAN
    ${delresult}=    delete    vlan:vlans/vlan=33
    Log    ${delresult.status_code}
    Should Be Equal  ${delresult.status_code}  ${204}
    ${result}=  get    vlan:vlans/vlan=33/config/vlan-id
    Should Be Equal  ${result.status_code}  ${404}
    
    
*** Keywords ***
json_property_should_equal    
    [Arguments]  ${json}  ${property}  ${value_expected}
    ${value_found} =    Get From Dictionary  ${json}  ${property}
    ${error_message} =  Catenate  SEPARATOR=  Expected value for property "  ${property}  " was "  ${value_expected}  " but found "  ${value_found}  "
    Should Be Equal As Strings  ${value_found}  ${value_expected}  ${error_message}    values=false

