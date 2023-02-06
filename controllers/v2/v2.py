from controller import Robot, Motor
import paho.mqtt.client as paho
import json
# create the Robot instance.
robot = Robot()

TIME_STEP = int(robot.getBasicTimeStep())
MAX_SPEED = 10
SPEED_UNIT = 0.00053429
NUM_SENSORS = 8
DISTANCE_RANGE = 2000

MATRIX = [
    [-5000, -5000],
    [-20000, 40000],
    [-30000, 50000],
    [-70000, 70000],
    [70000, -60000],
    [50000, -40000],
    [40000, -20000],
    [-5000, -5000],
    [-10000, -10000],
]

broker="localhost"
port=1880

def on_publish(client,userdata,result):             #create function for callback
    #print("data published \n")
    pass

def on_message(client, userdata, msg):
    move(msg.payload)
    pass
client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                             #establish connection
client1.subscribe("move")
client1.on_message = on_message



def bound(
    x,
    a,
    b,
):
    return a if x < a else (b if x > b else x)


def initMotor():
    leftMotor = robot.getDevice("left wheel motor")
    rightMotor = robot.getDevice("right wheel motor")

    leftMotor.setPosition(float("inf"))
    rightMotor.setPosition(float("inf"))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    return leftMotor, rightMotor


def initBraitengerg():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ds{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)

    return sensors


def initLight():
    sensors = []
    for i in range(NUM_SENSORS):
        sensor = robot.getDevice(f"ls{i}")
        sensor.enable(TIME_STEP)
        sensors.append(sensor)
    return sensors


leftMotor, rightMotor = initMotor()
light_sensors = initLight()

def move(speed):
    speed = json.loads(speed)
    leftMotor.setVelocity(speed[0])
    rightMotor.setVelocity(speed[1])

def get_light_infos():
    max_light = 0
    max_index = 0
    s = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i].getValue()
        s += value
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index, s)


def get_light_infos():
    max_light = 0
    max_index = 0
    s = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i].getValue()
        s += value
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index, s)


def publish_sensors():
    sensors_dist = [x.getValue() for x in initBraitengerg()]
    max_light, max_index, s = get_light_infos()
    client1.publish("sensors/light",str([max_light,max_index,s]))                   #publish
    client1.publish("sensors/dist",str(sensors_dist))                                #publish



while robot.step(TIME_STEP) != -1:
    client1.loop()
    publish_sensors()
