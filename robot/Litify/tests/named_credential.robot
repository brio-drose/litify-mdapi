*** Settings ***
Resource        cumulusci/robotframework/Salesforce.robot
Library         cumulusci.robotframework.PageObjects

Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Variables ***
${credentialName}     LitifyMDAPI

*** Test Cases ***
Edit Named Credential And Save
    Go To Setup Home
    Click Link    Named Credentials
    Open named credential edit modal    ${credentialName}
    Click Save in named credential


*** Keywords ***
Open named credential edit modal
    [Arguments]    ${credentialName}
    Wait Until Element Is Visible    xpath=//a[contains(text(),'${credentialName}')]
    Click Link    ${credentialName}
    Wait Until Modal Is Open
    Click Element    button[title='Edit']

Click Save in named credential
    Wait Until Modal Is Open
    Click Element    button[title='Save']
    Wait Until Modal Is Closed
