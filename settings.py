# -*- coding: utf-8 -*-

# AWS 設定
AWS_IOT_ENDPOINT = 'a8xj2opu6rf39-ats.iot.ap-northeast-1.amazonaws.com'
AWS_IOT_THING_NAME = 'iot-device'

# Certificates 設定
HOME_DIR = '/home/pi/p4p/work'
AWS_CERTS_PATH_BASE = HOME_DIR
AWS_CERTS_PATH_ROOTCA = AWS_CERTS_PATH_BASE + '/' + AWS_IOT_THING_NAME + '.root-CA.pem'
AWS_CERTS_PATH_PRIVATEKEY = AWS_CERTS_PATH_BASE + '/' + AWS_IOT_THING_NAME + '.private.key'
AWS_CERTS_PATH_CERTIFICATE = AWS_CERTS_PATH_BASE + '/' + AWS_IOT_THING_NAME + '.cert.pem'

# MQTT 設定
MQTT_DEVICE_ID = 'device_001'
MQTT_TOPIC = 'iot/device/sensordata'
MQTT_QOS = 0

# Raspberry Pi 設定
I2C_BUS = 0x1

# DHT11 の DATA pin をつないだ GPIO pin 番号
# https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/
TEMP_SENSOR_PIN = 7  

# センサデータの送信間隔（秒）
SEND_SENSORDATA_INTERVAL_SEC = 60*15
