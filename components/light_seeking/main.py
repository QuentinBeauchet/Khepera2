import paho.mqtt.client as mqtt
import json 
LIGHT_DETECTION_THRESHOLD = 700
MAX_SPEED = 10

MATRIX = [
    [-MAX_SPEED, MAX_SPEED],
    [-MAX_SPEED / 2, MAX_SPEED / 2],
    [MAX_SPEED, MAX_SPEED],
    [MAX_SPEED, MAX_SPEED],
    [MAX_SPEED / 2, -MAX_SPEED / 2],
    [MAX_SPEED, -MAX_SPEED],
    [-MAX_SPEED, MAX_SPEED],
    [MAX_SPEED, -MAX_SPEED],
]
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("algo/light", qos=2)

def on_message(client, userdata, msg):
    #print(msg.payload)
    light_sensors = json.loads(msg.payload)
    client.publish("res/light",str(follow_light(light_sensors)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Returns the max light detected and the index of the corresponding sensor.
def get_light_infos(light_sensors):
    max_light = 0
    max_index = 0
    for i in range(len(light_sensors)):
        value = light_sensors[i]
        if value > max_light:
            max_light = value
            max_index = i
    return (max_light, max_index)


# Light following detection algorithm
def follow_light(light_sensors):
    max_light, max_index = get_light_infos(light_sensors)

    if max_light < LIGHT_DETECTION_THRESHOLD:
        return [0, 0]

    return MATRIX[max_index]

client.connect("localhost", 1880, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

'''
if __name__ == "__main__":
    print(follow_light([100]))
'''

