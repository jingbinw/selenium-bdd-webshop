Feature: User Login
  As a user of the demo web shop
  I want to be able to log in to my account
  So that I can access my personal information and make purchases

  Background:
    Given I am on the demo webshop homepage
    When I click on the login link
    Then I should be on the login page

  @smoke @login
  Scenario: Successful login with valid credentials
    When I enter valid login credentials
    And I click the login button
    Then I should be logged in successfully
    And I should see the logout link

  @login @regression
  Scenario: Login with invalid email
    When I enter an invalid email "invalid-email"
    And I enter a valid password
    And I click the login button
    Then I should see an error message
    And I should remain on the login page

  @login @regression
  Scenario: Login with empty credentials
    When I leave the email field empty
    And I leave the password field empty
    And I click the login button
    Then I should see validation error messages
    And I should remain on the login page

  @login @regression
  Scenario: Login with valid email but wrong password
    When I enter a valid email
    And I enter an invalid password "wrongpassword"
    And I click the login button
    Then I should see an authentication error message
    And I should remain on the login page

  @login
  Scenario: Navigate to registration from login page
    When I click on the register link
    Then I should be redirected to the registration page