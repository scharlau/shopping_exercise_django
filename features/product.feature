Feature: checking products

    Scenario: add a product
        Given we want to add a product
        When we fill in the form
        Then it succeeds
    
    Scenario: adding products
        Given we have specific products to add
        | name          | price  |
        | this one      | 23.45  |
        | another thing | 34.56  |
        When we visit the listing page
        Then we will find 'another thing'