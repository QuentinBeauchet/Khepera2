'''MAX_SPEED = 10

# Determine the correct speed for each motor based on the results of the other algorithms
def coordination(dist, light):
    if dist == [MAX_SPEED, MAX_SPEED]:
        weights = [0.5, 0.5]
    else:
        weights = [1, 0]

    return [x * weights[0] + y * weights[1] for x, y in zip(dist, light)]


if __name__ == "__main__":
    print(coordination([100], [50]))
'''
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/light", qos=2)
    client.subscribe("sensors/dist", qos=2)
    client.subscribe("res/light", qos=2)
    client.subscribe("res/dist", qos=2)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == "sensors/light"):
        client1.publish("algo/light",msg.payload)                   #publish
    elif (msg.topic == "sensors/dist"):
        client1.publish("algo/dist",msg.payload)                    #publish
    elif (msg.topic == "res/light" or "res/dist" ):
        # à insérer le code ici 
        client1.publish("move",msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1880, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

