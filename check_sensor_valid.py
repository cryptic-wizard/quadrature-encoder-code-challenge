'''
A command line tool to determine if quadrature encoder sensor data is valid
'''
from sys import argv
from os.path import exists

class Point:
    '''
    Holds raw data and intermediate calculations for a single sensor point
    '''
    def __init__(self, time, encoder, pot):
        self.time = time
        self.encoder = encoder
        self.encoder_roll_avg = -1
        self.pot = pot
        self.pot_roll_avg = -1
        self.pot_expected = -1
        self.error = -1
        self.error_detected = False

    def point_print(self):
        '''
        Print sensor point member variables to command line
        '''
        print("\ttime = " + str(self.time) + " s")
        print("\tencoder = " + str(self.encoder))
        print("\tencoder_roll_avg = " + str(self.encoder_roll_avg))
        print("\tpot = " + str(self.pot))
        print("\tpot_roll_avg = " + str(self.pot_roll_avg))
        print("\tpot_expected = " + str(self.pot_expected))
        print("\terror = " + str(self.error) + " %")
        print("\terror_detected = " + str(self.error_detected))

    @classmethod
    def parse(cls, line):
        '''
        Converts a .txt line into a point

        Parameters:
            line (string): A text file line
        Returns:
            Point | null
        '''
        values = line.split()
        if len(values) != 3:
            print("Error: expected columns is 3 but was " + str(len(values)))
            return
        try:
            time = float(values[0])
            encoder = int(values[1])
            pot = int(values[2])
            return cls(time, encoder, pot)
        except ValueError:
            return

class RingBuffer:
    '''
    A generic ring buffer
    '''
    def __init__(self, size):
        '''
        Constructs a new RingBuffer with the specified size

        Parameters:
            size (int): size of the ring buffer
        '''
        self.values = list()
        self.size = size
        self.full = False

    def append(self, to_append):
        '''
        Appends an object to the RingBuffer

        Parameters:
            to_append (object): Object to append
        '''
        self.values.append(to_append)
        if (len(self.values) > self.size):
            self.values.pop(0)
            self.full = True
        elif (len(self.values) == self.size):
            self.full = True

    def __iter__(self):
          for each in self.values:
              yield each

# Constants
DEGREES = 360
GEAR_RATIO = 30
ENCODER_RES = 2048
POT_RES = 256
ROLL_AVG_COUNT = 10     # size of rolling average window
POT_ALLOWED_ERROR = 5   # percentage of error allowed for a single point
ERROR_THRESHOLD = 0.1   # percentage of points allowed to error for a single file

@staticmethod
def simple_moving_avg(points_ring_buffer):
    '''
    Calculates the simple moving average for sensor points

    Parameters:
        points_ring_buffer (RingBuffer[Point]): a collection of points to use for rolling averages
    Returns:
        Point
    '''
    encoder_sum = 0
    pot_sum = 0
    for point in points_ring_buffer.values:
        encoder_sum += point.encoder
        pot_sum += point.pot
    point = points_ring_buffer.values[points_ring_buffer.size - 1]
    point.encoder_roll_avg = encoder_sum / points_ring_buffer.size
    point.pot_roll_avg = pot_sum / points_ring_buffer.size
    return point

@staticmethod
def exponenial_moving_avg(points_ring_buffer):
    '''
    Calculates the exponential moving average for sensor points
    
    Parameters:
        points_ring_buffer (RingBuffer[Point]): a collection of points to use for rolling averages
    Returns:
        Point
    '''
    k = 2/(points_ring_buffer.size + 1)
    current_point = points_ring_buffer.values[points_ring_buffer.size - 1]
    last_point = points_ring_buffer.values[points_ring_buffer.size - 2]
    current_point.encoder_roll_avg = k*current_point.encoder + ((1-k) * last_point.encoder_roll_avg)
    current_point.pot_roll_avg = k*current_point.pot + ((1-k) * last_point.pot_roll_avg)
    return current_point

def is_sensor_data_valid(file_name):
    '''
    Determines if sensor data is valid by comparing the expected potentiometer output to the actual potentiometer output
    
    Parameters:
        file_name (string): The .txt file of sensor data
    Returns:
        True | False
    '''

    # Variables
    pot_start = -1
    encoder_sum = -1
    pot_sum = -1
    total_points = 0
    error_count = 0

    # Main
    points_ring_buffer = RingBuffer(ROLL_AVG_COUNT)
    lower_error_limit = -1 * POT_ALLOWED_ERROR
    upper_error_limit = POT_ALLOWED_ERROR

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
            if (points_ring_buffer.full == True):
                # Initialize pot start location and simple moving average
                if (pot_start == -1):
                    point = simple_moving_avg(points_ring_buffer)
                    point.encoder_roll_avg = 0
                    points_ring_buffer.values[points_ring_buffer.size - 1] = point
                    pot_start = point.pot_roll_avg
                    #print("Potentiometer start set to " + str(pot_start))
                else:
                    point = exponenial_moving_avg(points_ring_buffer)
                    
                # Set expected pot value and check for error
                point.pot_expected = pot_start + (point.encoder_roll_avg*POT_RES/ENCODER_RES/GEAR_RATIO)
                point.error = float((point.pot_expected - point.pot_roll_avg)/POT_RES*100)
                if (point.error < lower_error_limit or point.error > upper_error_limit):
                    point.error_detected = True
                    error_count += 1
                    #point.point_print()
        
        # Report error percentage and pass/fail
        error_percent = float(error_count / total_points*100)
        print (file_name + " --> " + str(error_percent) + " % points were expected error")
        if (error_percent > ERROR_THRESHOLD):
            print (file_name + " --> Sensor error detected")
            return False
        else:
            print (file_name + " --> Sensor data is valid")
            return True

def get_file_from_args(args):
    '''
    Checks for a valid file as a command line argument

    Parameters:
        args (sys.argv): Command line arguments
    Returns:
        string | exits program
    '''
    # Quit program if wrong number of arguments
    if len(args) != 2:
        print("Error: expected arguments is 1 but was " + str(len(args)-1))
        print("Example: check_sensor_valid.py my_sensor_data.txt")
        quit()

    # Quit program if file does not exist
    file_name = args[1]
    if not exists(file_name):
        print("Error: " + file_name + " does not exist")
        print("Example: check_sensor_valid.py my_sensor_data.txt")
        quit()

    # Quit program if file is the wrong type
    if not file_name.__contains__(".txt"):
        print("Error: expected .txt file")
        print("Example: check_sensor_valid.py my_sensor_data.txt")
        quit()
    else:
        return file_name

if (len(argv) != 0 and argv[0] == "check_sensor_valid.py"):
    file_name = get_file_from_args(argv)
    is_sensor_data_valid(file_name)