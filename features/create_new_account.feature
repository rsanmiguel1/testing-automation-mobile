@CreateTeam
Feature: Create New Accounts
  # We create new accounts for both Alice and Bob
     @Alice
    Scenario: Create New Account for Alice
      Given I am in the login screen
        Then I create a passcode number
        Then I click on the Sign Up button
        Then I am in the Team URL screen
         And I write the Team URL
         And I click the Continue button
        Then I see I am on the 'Save Your Recovery Phrase' screen
        Then I copy the recovery key
        Then I click Continue
        When I see the 'Are you sure you saved your Recovery Phrase' screen
         And I click on the 'No, go back' option
        Then I see I am on the 'Save Your Recovery Phrase' screen
        Then I copy the recovery key
        Then I click Continue
        When I see the 'Are you sure you saved your Recovery Phrase' screen
        Then I click on the 'Yes, I saved it' option
        Then I am on the Add/Create team start page
        Then I enter the License Key

    @Bob
    Scenario: Create New Account for Bob
       Given I am in the login screen
        Then I create a passcode number
        Then I click on the Sign Up button
        Then I am in the Team URL screen
         And I write the Team URL
         And I click the Continue button
        Then I see I am on the 'Save Your Recovery Phrase' screen
        Then I copy the recovery key
        Then I click Continue
        When I see the 'Are you sure you saved your Recovery Phrase' screen
        Then I click on the 'Yes, I saved it' option
        Then I am on the Add/Create team start page
