Feature: Product Search and Shopping Cart
  As a customer of the demo web shop
  I want to search for products and add them to my cart
  So that I can purchase items I need

  Background:
    Given I am on the demo webshop homepage

  @smoke @shopping
  Scenario: Search for a product and view results
    When I search for "computer"
    Then I should see search results
    And the search results should contain products related to "computer"

  @shopping @regression
  Scenario: Add a product to cart from search results
    When I search for "book"
    Then I should see search results
    When I click on the first product in the search results
    Then I should be on the product details page
    When I click add to cart
    Then I should see a success message
    And the product should be added to my cart

  @shopping @regression
  Scenario: Add multiple quantities of a product to cart
    When I search for "computer"
    Then I should see search results
    When I click on the first product in the search results
    And I change the quantity to "3"
    And I click add to cart
    Then I should see a success message
    And the cart should show "3" items

  @shopping
  Scenario: View shopping cart contents
    Given I have added products to my cart
    When I navigate to the shopping cart
    Then I should see the products in my cart
    And I should see the total price

  @shopping
  Scenario: Update product quantity in cart
    Given I have added products to my cart
    When I navigate to the shopping cart
    And I update the quantity of the first item to "2"
    And I click update cart
    Then the cart should reflect the updated quantity
    And the total price should be updated

  @shopping
  Scenario: Remove product from cart
    Given I have added products to my cart
    When I navigate to the shopping cart
    And I select the first item for removal
    And I click update cart
    Then the item should be removed from my cart

  @shopping
  Scenario: Empty cart message
    Given I have an empty cart
    When I navigate to the shopping cart
    Then I should see an empty cart message

  @shopping @regression
  Scenario: Continue shopping from cart
    Given I have added products to my cart
    When I navigate to the shopping cart
    And I click continue shopping
    Then I should be redirected to the homepage

  @shopping
  Scenario Outline: Search for different product categories
    When I search for "<product_category>"
    Then I should see search results
    And the search results should contain products related to "<product_category>"

    Examples:
      | product_category |
      | book            |
      | computer        |
      | camcorder       |
      | jewelry         |