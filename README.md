## Description
* A Python command line tool to determine if quadrature encoder sensor data is valid

## Tests
[![Python 3.10.5](https://github.com/cryptic-wizard/quadrature-encoder-code-challenge/actions/workflows/python.yml/badge.svg)](https://github.com/cryptic-wizard/quadrature-encoder-code-challenge/actions/workflows/python.yml)

## Usage
### Basic
```
py check_sensor_valid.py sensor_data.txt
```
### Generate Documentation
```
pip install -r requirements.txt
py -m inkpot check_sensor_valid.py
```
### Run Behave Tests
```
pip install -r requirements.txt
cd tests
behave
```

## Tools
* [Python 3.10.5](https://www.python.org/downloads/)
* [inkpot](https://pypi.org/project/inkpot/)
* [Behave](https://behave.readthedocs.io/en/stable/api.html)

## License
* [MIT License](https://github.com/cryptic-wizard/quadrature-encoder-code-challenge/blob/main/LICENSE.md)