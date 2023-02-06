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

speed = [0.0, 0.0]

def on_publish(client,userdata,result):             #create function for callback
    #print("data published \n")
    pass

def on_message(client, userdata, msg):
    global speed
    speed = json.loads(msg.payload)
    pass

client= paho.Client("control1")                           #create client object
client.on_publish = on_publish                          #assign function to callback
client.connect(broker,port)                             #establish connection
client.subscribe("move", qos=0)
client.on_message = on_message



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

def move():
    leftMotor.setVelocity(speed[0])
    rightMotor.setVelocity(speed[1])

def publish_sensors():
    sensors_dist = [x.getValue() for x in initBraitengerg()]
    sensors_light = [x.getValue() for x in light_sensors]
    client.publish("sensors",str([sensors_light, sensors_dist]))                          #publish



while robot.step(TIME_STEP) != -1:
    publish_sensors()
    client.loop()
    move()

