import sys
from os.path import exists

header = ['time','encoder','potentiometer']

class Point:
    time = 0
    encoder = 0
    potentiometer = 0

    def parse(line):
        values = line.split()
        if len(values) != 3:
            print("Error - expected columns is 3 but was " + str(len(values)))
        else:
            point = Point()
            point.time = values[0]
            point.encoder = values[1]
            point.potentiometer = values[2]
            print("\ttime = " + str(point.time))
            print("\tencoder = " + str(point.encoder))
            print("\tpotentiometer = " + str(point.potentiometer))
            return point

if len(sys.argv) != 2:
    print("Error: expected arguments is 1 but was " + str(len(sys.argv)-1))
    print("Example: main.py my-sensor-data.txt")
    quit()

file_name = sys.argv[1]
if not exists(file_name):
    print(file_name + " does not exist")
    quit()

if not file_name.__contains__(".txt"):
    print(file_name + " is not a .txt")
    quit()

points = list()
with open(file_name, "r") as sensor_data:
    for line in sensor_data:
        print(line, end='')
        points.append(Point.parse(line))
    