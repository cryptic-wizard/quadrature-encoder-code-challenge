Feature: Sample Data

Scenario Outline: Sample data is evaluated correctly
    When I check if <file_name> is valid
    Then the sample data <truthiness> valid

    Examples:
    | file_name                 | truthiness |
    | sample_data/normal.txt    | is         |
    | sample_data/error.txt     | is not     |

Scenario Outline: Point SMA is calculated correctly
    When I calculate the SMA of <array>
    Then the SMA is <sma>

    Examples:
    | array               | sma  |
    | {7,8,9,10}          | 8.5  |
    | {42,43,44,45,46,47} | 44.5 |