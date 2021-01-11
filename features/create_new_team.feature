@CreateTeam @Alice
#Manual Test Case Link:https://treehouse.spideroak.com/jira/secure/Tests.jspa#/testCase/SHARE-T9
Feature: Create Team (Happy Path)
         Create a new team via happy path.

#Background: User has a CCLAVE account
# Given A new account will automatically open the Add Team/Create Team screen
# And for an existing account, the tester will have to navigate to the Welcome Screen

  Scenario: Create Team in CrossClave
    Given  I am on the Add/Create team start page
      And  I enter the License Key
      When I click the Create Team button
      Then I enter the valid team name and check the continue button becomes active
      When I click the Continue button
      Then I enter the name for the user and check the Continue button becomes active
      When I click the Continue button
      Then I am on the Welcome Screen
      And  I see the team name in the Team Selector

