Feature: End-to-End Shopping Experience
  As a customer
  I want to complete a full shopping experience
  So that I can purchase products successfully

  @smoke @e2e
  Scenario: Complete shopping journey - Login, Search, Add to Cart
    Given I am on the demo webshop homepage
    When I click on the login link
    And I enter valid login credentials
    And I click the login button
    Then I should be logged in successfully
    When I search for "laptop"
    Then I should see search results
    When I click on the first product in the search results
    And I click add to cart
    Then I should see a success message
    When I navigate to the shopping cart
    Then I should see the products in my cart
    And I should see the total price

  @e2e
  Scenario: Guest user shopping experience
    Given I am on the demo webshop homepage
    When I search for "book"
    Then I should see search results
    When I click on the first product in the search results
    And I click add to cart
    Then I should see a success message
    When I navigate to the shopping cart
    Then I should see the products in my cart
    And I should be able to proceed as a guest