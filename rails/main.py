from rail_lib import *
from driver.devices import StepMotor
from threading import Event
import picamera
from driver.libtft144.lib_tft144 import TFT144
import RPi.GPIO as GPIO
import spidev

motorH = StepMotor([26,19,13,6])
motorV = StepMotor([12,16,20,21])


kbEvent = KeyboardEvent()
camEvent = Event()
tftEvent = Event()

# camera config
piCam = picamera.PiCamera()
piCam.resolution = (128, 128)
piCam.iso = 800
# diaplay config
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
tft = TFT144(GPIO, spidev.SpiDev(), 0, 24, 25, 5, TFT144.ORIENTATION180, isRedBoard=False)

motoT = MotoThread(kbEvent, motorH, motorV)
kbT = KeyboardThread(kbEvent)
camT = CameraThread(camEvent, tftEvent, piCam)
tftT = DisplayThread(camEvent, tftEvent, tft)
core = Core(camEvent, tftEvent, tft)

motoT.start()
kbT.start()
camT.start()
tftT.start()
core.start()

camEvent.set()

motoT.join()
kbT.join()
core.join()

del motoT
del kbT

print('main done')