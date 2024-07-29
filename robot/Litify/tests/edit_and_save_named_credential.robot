*** Settings ***
Resource        cumulusci/robotframework/Salesforce.robot
Library         cumulusci.robotframework.PageObjects
Library         Process
Library  cumulusci.robotframework.CumulusCI  ${ORG}
Suite Setup     Run Keywords
...             Setup Test Data
...             Open Test Browser
Suite Teardown  Delete Records And Close Browser


*** Tasks ***
Edit And Save Named Credential
    [Documentation]             Edit and save Named Credential so that it can
    ...                         update to status "Authenticated".
    Navigate To Named Credentials
    Edit Named Credentials      ${credential}
    Click Save
    Login as User
    Verify Authentication Status Is Authenticated


*** Variables ***
${credential} =                 //setup_platform_namedcredential-credential-table//a[text()='LitifyMDAPI']//parent::*
${edit_button} =                //input[@value='Edit']
${save_button} =                //input[@value='Save']
${username_field} =             //input[@id='username']
${password_field} =             //input[@id='password']
${login_button} =               //input[@id='Login']
# Tokens
${orginfo} =                    Get Org Info
${ACCESS_TOKEN} =               will_be_replaced

*** Keywords ***
Setup Test Data
    [Documentation]             Sets up all data required for test.
    Get Salesforce Instance URL

Get Salesforce Instance URL
    [Documentation]
    ...                         Get Salesforce Org Instance URL.
    ...                         Sets as a Test Variable.
    ${org_info} =               Get Org Info
    Log                         ${org_info}
    ${instance_url} =           Get From Dictionary        ${org_info}
    ...                         instance_url
    ${instance_url} =           Set Suite Variable         ${instance_url}

Navigate To Named Credentials
    [Documentation]             Navigates to the Object Field History page.
    ${history_url} =            Set Variable
    ...                         ${instance_url}/lightning/setup/NamedCredential/home
    Go To                       ${history_url}

Edit Named Credentials
    [Documentation]             Click on edit button for provided Named Credential.
    [Arguments]                 ${named_credential}
    # iframe for Salesforce Classic setup pages
    Click Element               ${named_credential}
    Select Frame                //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe
    Click Element               ${edit_button}
    Unselect Frame
    Sleep                       15s

Click Save
    [Documentation]             Click Save Button on edit page.
    Wait Until Page Contains Element
    ...                         //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe
    Select Frame                //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe
    Wait Until Page Contains Element
    ...                         //*[@value="Save"]
    Click Element               //*[@value="Save"]
    Unselect Frame
    Sleep                       15s

Login as User
    [Documentation]             Enter User credentials and click Login Button on login page.
    Wait Until Page Contains Element
    ...                         ${username_field}
    ${access_token} =           Get From Dictionary        ${org_info}
    ...                         access_token
    ${access_token} =           Set Suite Variable         ${access_token}
    breakpoint                  # Pause for manual inspection
    Input Text                  ${username_field}            ${USERNAME}
    Input Text                  ${password_field}            ${PASSWORD}
    Click Element               ${login_button}
    Sleep                       15s

Verify Authentication Status Is Authenticated
    [Documentation]             Waits for Authenticaiton Status to load and then validates it's value
    ...                         is "Authenticated".
    Wait Until Page Contains Element
    ...                         //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe
    Select Frame                //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe
    Wait Until Page Contains Element
    ...                         //*[contains(@id,"authStatusSection")]
    SeleniumLibrary.Element Text Should Be
    ...                         //*[contains(@id,"authStatusSection")]
    ...                         Authenticated
    Unselect Frame