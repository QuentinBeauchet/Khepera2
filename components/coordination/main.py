import paho.mqtt.client as mqtt
import json
MAX_SPEED = 10

service_list = ["light","dist"]

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
        last_speed["res/"+i] = []
        client.subscribe("res/"+i, qos=0)

def is_someone_empty():
    for i in service_list:
        if(last_speed["res/"+i] == []):
            return True
    return False

def free_last_speed():
    for i in service_list:
        last_speed["res/"+i] = []

# Take the last value of each algorithm and process the coordination
def coordination_controller(client,topic, speed):
    last_speed[topic] = speed
    if(not is_someone_empty()):
        res = str(coordination( last_speed["res/dist"],last_speed["res/light"]))
        client.publish("move",res)
        free_last_speed()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Coordination : Connected with result code "+str(rc))
    init_last_speed(client)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors", qos=0)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if ( b"nan" in msg.payload ):
        return
    arr_msg = json.loads(msg.payload)
    if (msg.topic == "sensors"):
        client.publish("algo/light",str(arr_msg[0]))                   #publish
        client.publish("algo/dist",str(arr_msg[1]))                    #publish
    elif ("res/" in msg.topic ):
        speed_array = json.loads(msg.payload)
        coordination_controller(client, msg.topic, speed_array)
        #print(msg.topic + "  : -> " + str(msg.payload) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1880, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

