import ssl
from email.message import EmailMessage
#   import smtplib
import json
import random
import time
import psutil
from paho.mqtt import client as mqtt_client
from sendDataBase import sendDataFireBase


# Local
# BROKER = 'localhost'
# PORT = 1883
# 0TOPIC = "/test"
# generate client ID with pub prefix randomly
# CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
# USERNAME = 'admin'
# PASSWORD = 'public'
# FLAG_CONNECTED = 0

# Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "test_arquitectura2"
TOPIC_ALERT = "test_arquitectura2"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    #   client.on_message = on_message
    client.connect(BROKER, PORT)
    return client


client = connect_mqtt()


def publish(client, TOPIC, msg):
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)
    #   time.sleep(1)

#   All code above configures hivemq server
#   From here we configure auto-emails

#   set sender and receiver


email_sender = 'carlozedmusa@gmail.com'       # Ingresar mail desde donde se enviaran los mensajes
email_password = ''     # Ingresar contraseña del email
email_receiver = 'carlozedmusa@gmail.com'     # Ingresar email que recibira los mensajes


#   set message
subject = 'Uso de cpu alto'
body = """
El uso de su cpu es mayor al 40%
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()


#   if cpu > 40 send mail
TOPIC = "test_arquitectura2"
while True:
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()[2]
    usoDisco = round(psutil.disk_usage('/').percent)
    if cpu > 0:
        data = {
            'CPU': cpu,
            'Memoria': ram,
            'Disco': usoDisco
        }
        sendDataFireBase(cpu, ram, usoDisco)

        json_data = json.dumps(data)
        #publish(client, TOPIC, json_data)
        result= client.publish(TOPIC, json_data)


    time.sleep(2)