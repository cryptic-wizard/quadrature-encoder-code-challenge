# check_sensor_valid.py
## check_sensor_valid.py
### class Point()
`Holds raw data and intermediate calculations for a single sensor point` 

> **def print(self)** \
> `Print sensor point member variables to command line` 
>
> **@staticmethod \
def parse(line)** \
> `Converts a .txt line into a point` \
`` \
`Parameters:` \
`    line (string): A text file line` \
`Returns:` \
`    Point | null` 
>
> **@staticmethod \
def simple_moving_avg(points_ring_buffer)** \
> `Calculates the simple moving average for sensor points` \
`` \
`Parameters:` \
`    points_ring_buffer (RingBuffer[Point]): a collection of points to use for rolling averages` \
`Returns:` \
`    Point` 
>
> **@staticmethod \
def exponenial_moving_avg(points_ring_buffer)** \
> `Calculates the exponential moving average for sensor points` \
`` \
`Parameters:` \
`    points_ring_buffer (RingBuffer[Point]): a collection of points to use for rolling averages` \
`Returns:` \
`    Point` 
>
### class RingBuffer()
`A generic ring buffer` 

> **def \_\_init\_\_(self, size)** \
> `Constructs a new RingBuffer with the specified size` \
`` \
`Parameters:` \
`    size (int): size of the ring buffer` 
>
> **def append(self, to_append)** \
> `Appends an object to the RingBuffer` \
`` \
`Parameters:` \
`    to_append (object): Object to append` 
>
> **def \_\_iter\_\_(self)** \
> `None` 
>
**def is_sensor_data_valid(file_name)** \
`Determines if sensor data is valid by comparing the expected potentiometer output to the actual potentiometer output` \
`` \
`Parameters:` \
`    file_name (string): The .txt file of sensor data` \
`Returns:` \
`    True | False` 

**def get_file_from_args(args)** \
`Checks for a valid file as a command line argument` \
`` \
`Parameters:` \
`    args (sys.argv): Command line arguments` \
`Returns:` \
`    string | exits program` 


