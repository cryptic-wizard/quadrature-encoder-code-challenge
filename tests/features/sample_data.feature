Feature: Sample Data

Scenario: Perfect sample data is valid
    Given I check if sample_data/perfect.txt is valid
    Then the sample data is valid

Scenario: Normal sample data is valid
    Given I check if sample_data/normal.txt is valid
    Then the sample data is valid

Scenario: Error sample data is not valid
    Given I check if sample_data/error.txt is valid
    Then the sample data is not valid