import sys
from os.path import exists

# Holds raw data and intermediate calculations for a single point
class Point:
    # Variables
    time = -1
    encoder = -1
    encoder_roll_avg = -1
    pot = -1
    pot_roll_avg = -1
    pot_expected = -1
    error = -1
    error_detected = 'False'

    # Print point member variables
    def print(self):
        print("\ttime = " + str(self.time) + " s")
        print("\tencoder = " + str(self.encoder))
        print("\tencoder_roll_avg = " + str(self.encoder_roll_avg))
        print("\tpot = " + str(self.pot))
        print("\tpot_roll_avg = " + str(self.pot_roll_avg))
        print("\tpot_expected = " + str(self.pot_expected))
        print("\terror = " + str(self.error) + " %")
        print("\terror_detected = " + str(self.error_detected))

    # Converts txt line into a point
    @staticmethod
    def parse(line):
        values = line.split()
        if len(values) != 3:
            print("Error: expected columns is 3 but was " + str(len(values)))
            return
        try:
            point = Point()
            point.time = float(values[0])
            point.encoder = int(values[1])
            point.pot = int(values[2])
            return point
        except ValueError:
            return

    # Calculates simple moving average for points in ring buffer
    @staticmethod
    def simple_moving_avg(points_ring_buffer):
        encoder_sum = 0
        pot_sum = 0
        for point in points_ring_buffer.values:
            encoder_sum += point.encoder
            pot_sum += point.pot
        point = points_ring_buffer.values[roll_avg_count - 1]
        point.encoder_roll_avg = encoder_sum / roll_avg_count
        point.pot_roll_avg = pot_sum / roll_avg_count
        return point

    # Calculates exponenial moving average for points in ring buffer
    @staticmethod
    def exponenial_moving_avg(points_ring_buffer):
        k = 2/(points_ring_buffer.size + 1)
        current_point = points_ring_buffer.values[points_ring_buffer.size - 1]
        last_point = points_ring_buffer.values[points_ring_buffer.size - 2]
        current_point.encoder_roll_avg = k*current_point.encoder + ((1-k) * last_point.encoder_roll_avg)
        current_point.pot_roll_avg = k*current_point.pot + ((1-k) * last_point.pot_roll_avg)
        return current_point

class RingBuffer:
    values = list()
    size = -1
    full = 'False'

    def __init__(self, size):
        self.size = size

    def append(self, to_append):
        self.values.append(to_append)
        if (len(self.values) > self.size):
            self.values.pop(0)
            self.full = 'True'
        elif (len(self.values) == self.size):
            self.full = 'True'
    
    # Allow ring buffer to be iterated like a list
    def __iter__(self):
          for each in self.values:
              yield each

# Constants
degrees = 360
gear_ratio = 30
encoder_res = 2048
pot_res = 256
roll_avg_count = 10     # size of rolling average window
pot_allowed_error = 5   # percentage of error allowed for a single point
error_threshold = 0.1   # percentage of points allowed to error for a single file

# Variables
pot_start = -1
encoder_sum = -1
pot_sum = -1
total_points = 0
error_count = 0

# Quit program if wrong number of arguments
if len(sys.argv) != 2:
    print("Error: expected arguments is 1 but was " + str(len(sys.argv)-1))
    print("Example: main.py my-sensor-data.txt")
    quit()

# Quit program if file does not exist
file_name = sys.argv[1]
if not exists(file_name):
    print("Error: " + file_name + " does not exist")
    print("Example: main.py my-sensor-data.txt")
    quit()

# Quit program if file is the wrong type
if not file_name.__contains__(".txt"):
    print("Error: expected .txt file")
    print("Example: main.py my-sensor-data.txt")
    quit()

# Main
points_ring_buffer = RingBuffer(roll_avg_count)
lower_error_limit = -1 * pot_allowed_error
upper_error_limit = pot_allowed_error

with open(file_name, "r") as sensor_data:
    # Parse each point and add to ring buffer
    for line in sensor_data:
        #print(line, end='')
        raw_point = Point.parse(line)
        if not raw_point:
            continue
        points_ring_buffer.append(raw_point)
        total_points += 1

        # Calculate rolling averages from ring buffer
        if (points_ring_buffer.full == 'True'):
            # Initialize pot start location and simple moving average
            if (pot_start == -1):
                point = Point.simple_moving_avg(points_ring_buffer)
                points_ring_buffer.values[points_ring_buffer.size - 1] = point
                pot_start = point.pot_roll_avg
                #print("Potentiometer start set to " + str(pot_start))
            else:
                point = Point.exponenial_moving_avg(points_ring_buffer)
                
            # Set expected pot value and check for error
            point.pot_expected = pot_start + (point.encoder_roll_avg*pot_res/encoder_res/gear_ratio)
            point.error = float((point.pot_expected - point.pot_roll_avg)/pot_res*100)
            if (point.error < lower_error_limit or point.error > upper_error_limit):
                point.error_detected = 'True'
                error_count += 1
                #point.print()
    
    # Report error percentage and pass/fail
    error_percent = float(error_count / total_points*100)
    print (file_name + " --> " + str(error_percent) + " % points were expected error")
    if (error_percent > error_threshold):
        print (file_name + " --> Sensor error detected")
    else:
        print (file_name + " --> Sensor is good")
    