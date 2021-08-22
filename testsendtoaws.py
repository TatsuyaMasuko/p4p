# -*- coding: utf-8 -*-

# 共通
import json
import socket
import time
import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO
import click

# 輝度用
import ADC0832


# 温湿度用
import settings
from DHT11_Python import dht11


MQTTClient = None


class Sensor:
    """ 各種センサデータを包括的に扱うためのクラス """

    def __init__(self, pin_temp=7, demo=False):
        self.demo = demo
        if self.demo:
            return
        
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.cleanup()
        except NameError:
            raise Exception('Please add option "--demo".')

        ADC0832.setup()
        self.instance = dht11.DHT11(pin=pin_temp)

    def is_demo(self):
        return self.demo

    def update_sensordata(self):
        """ 各種センサの値を取得し、インスタンスがもつセンサデータを更新する """

        if self.is_demo():
            self.lux = 123.45
            self.temperature = 12.34
            self.humidity = 45.67
            return


        # 輝度の値取得
        res = ADC0832.getResult() - 80
        if res < 0:
            res = 0
        if res > 100:
            res = 100
        self.lux = res

        # 温湿度の値取得
        result = self.instance.read()
        while not result.is_valid():
            result = self.instance.read()
            time.sleep(1)

        self.temperature = result.temperature
        self.humidity = result.humidity

    def get_lux(self):
        return self.lux

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity


def init_awsiot_client():
    """ AWS IoT に接続するための各種初期化を行う """

    device_id = settings.MQTT_DEVICE_ID
    endpoint = settings.AWS_IOT_ENDPOINT

    my_mqtt_client = AWSIoTMQTTClient(device_id)
    my_mqtt_client.configureEndpoint(endpoint, 8883)
    my_mqtt_client.configureCredentials(
        settings.AWS_CERTS_PATH_ROOTCA,
        settings.AWS_CERTS_PATH_PRIVATEKEY,
        settings.AWS_CERTS_PATH_CERTIFICATE
    )
    my_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
    my_mqtt_client.configureOfflinePublishQueueing(-1)
    my_mqtt_client.configureDrainingFrequency(2)
    my_mqtt_client.configureConnectDisconnectTimeout(60*5)
    my_mqtt_client.configureMQTTOperationTimeout(60*5)
    return my_mqtt_client


def get_sensordata_and_send_to_aws(my_mqtt_client, sensor):
    """ センサ (DHT11, TSL2561) からデータを取得し、AWS に送信する """

    payload = {
        'device_id': settings.MQTT_DEVICE_ID,     
        'timestamp': None,
        'timesec': None,
        'temperature': None,
        'humidity': None,
        'lux': None,
    }

    payload['timestamp'] = str(datetime.datetime.now())
    
    payload['timesec'] = int(time.time())*1000

    # 温度・湿度・照度を取得
    sensor.update_sensordata()
    payload['lux'] = int(sensor.get_lux())
    payload['temperature'] = sensor.get_temperature()
    payload['humidity'] = sensor.get_humidity()

    payload_json = json.dumps(payload, indent=4)
    print(payload_json)

    # AWS IoT に Publish
    result = my_mqtt_client.publish(
        settings.MQTT_TOPIC,
        payload_json,
        settings.MQTT_QOS
    )
    if result:
        print('Publish result: OK')
    else:
        print('Publish result: NG')


@click.command()
@click.option('--demo', '-d', is_flag=True, help='Demo mode. (Send dummy data)')
def main(demo=False):
    my_mqtt_client = init_awsiot_client()
    my_mqtt_client.connect()
    print('MQTT connect.')
    
    # setting.py参照
    sensor = Sensor(pin_temp=settings.TEMP_SENSOR_PIN, demo=demo)

    while True:
        get_sensordata_and_send_to_aws(my_mqtt_client, sensor)
        time.sleep(settings.SEND_SENSORDATA_INTERVAL_SEC)


if __name__ == '__main__':
    main()
    
