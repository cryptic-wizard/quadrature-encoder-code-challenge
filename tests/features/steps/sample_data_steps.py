# test_sample_data.py

# behave is used to PASS/FAIL tests based on assertions
from behave import *
import sys

sys.path.append('../..')
from quadrature_encoder_code_challenge.check_sensor_valid import *

def before_scenario(context):
    print()

@when('I check if {file_name} is valid')
def when_i_check_if_x_is_valid(context, file_name):
    context.valid = is_sensor_data_valid(file_name)

@when('I calculate the SMA of {array}')
def when_i_calculate_the_SMA_of_x(context, array):
    context.ring_buffer = RingBuffer(len(array))
    for value in array:
        point = Point()
        point.encoder = value
        point.pot = value
        context.ring_buffer.append(Point())
    assert(len(context.ring_buffer.values) == len(array))
    context.point = simple_moving_avg(context.ring_buffer)

@then("the sample data {truthiness} valid")
def then_the_same_data_x_valid(context, truthiness):
    print("Truthiness = " + str(truthiness))
    print("Valid = " + str(context.valid))
    if (truthiness == "is"):
        assert(context.valid == True)
    elif (truthiness == "is not"):
        assert(context.valid == False)

@then('the SMA is {sma}')
def then_the_sma_is_x(context, sma):
    context.point.encoder_roll_avg = sma
    context.point.pot_roll_avg = sma