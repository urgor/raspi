
# import driver.devices as dev
import driver.commands as cmd
import time
import picamera

import RPi.GPIO as GPIO
from driver.libtft144.lib_tft144 import TFT144
import spidev

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
tft = TFT144(GPIO, spidev.SpiDev(), 0, 24, 25, 5, TFT144.ORIENTATION180, isRedBoard=False)
tft.led_on(False)
del tft


cam = picamera.PiCamera()
# cam.vflip = True
# cam.hflip = True
camCmd = cmd.CameraCommand(cam, 'picz/image{:0>6}.jpg')
camCmd.setResolution(cmd.CameraCommand.VIDEO_RESOLUTION_1080)

while 1:
    camCmd.doSnapshot()
    time.sleep(3)



