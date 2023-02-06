import paho.mqtt.client as mqtt
import json

MAX_SPEED = 10

service_list = ["light", "dist"]

last_speed = {}

# Determine the correct speed for each motor based on the results of the other algorithms
def coordination(dist, light):
    if dist == [MAX_SPEED, MAX_SPEED]:
        weights = [0.5, 0.5]
    else:
        weights = [1, 0]

    return [x * weights[0] + y * weights[1] for x, y in zip(dist, light)]


def init_last_speed(client):
    for i in service_list:
        last_speed["res/" + i] = [0, 0]
        client.subscribe("res/" + i, qos=0)


# Take the last value of each algorithm and process the coordination
def coordination_controller(client, topic, speed):
    last_speed[topic] = speed
    print("MOVE")
    client.publish("move", str(coordination(last_speed["res/dist"], last_speed["res/light"])))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Coordination : Connected with result code " + str(rc))
    init_last_speed(client)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors", qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if b"nan" in msg.payload:
        return
    arr_msg = json.loads(msg.payload)
    if msg.topic == "sensors":
        client.publish("algo/light", str(arr_msg[0]))  # publish
        client.publish("algo/dist", str(arr_msg[1]))  # publish
    elif "res/" in msg.topic:
        speed_array = json.loads(msg.payload)
        coordination_controller(client, msg.topic, speed_array)


def initMQTT():
    client = mqtt.Client("control1")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1880, 60)

    client.loop_forever()


if __name__ == "__main__":
    initMQTT()
