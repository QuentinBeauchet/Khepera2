from controller import Robot
import paho.mqtt.client as paho
import json

# create the Robot instance.
robot = Robot()

TIME_STEP = int(robot.getBasicTimeStep())
NUM_SENSORS = 8


BROKER = "localhost"
PORT = 1880


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


def initMQTT():
    client = paho.Client()  # create client object
    client.connect(BROKER, PORT)  # establish connection
    client.subscribe("move", qos=0)
    client.on_message = on_message
    return client


def move():
    leftMotor.setVelocity(speed[0])
    rightMotor.setVelocity(speed[1])


def publish_sensors():
    dist = [x.getValue() for x in dist_sensors]
    light = [x.getValue() for x in light_sensors]
    client.publish("sensors", str([light, dist]))


def on_message(client, userdata, msg):
    global speed
    speed = json.loads(msg.payload)


if __name__ == "__main__":
    client = initMQTT()

    speed = [0.0, 0.0]
    leftMotor, rightMotor = initMotor()
    light_sensors = initLight()
    dist_sensors = initBraitengerg()

    while robot.step(TIME_STEP) != -1:
        publish_sensors()
        move()
        client.loop()
