import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def readRFID():
    text = ''
    while text == '':
        id, text = reader.read()
        GPIO.cleanup()
    return text
