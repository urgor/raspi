import commands as cmd
import RPi.GPIO as GPIO
import picamera
from libtft144.lib_tft144 import TFT144

# python3-pigpio/stable 1.60-1 all
#   Python module which talks to the pigpio daemon (Python 3)
import spidev
cam = picamera.PiCamera()
# camCmd = cmd.CameraCommand(cam, 'picz/image.bmp')
# camCmd.setResolution(cmd.CameraCommand.PICTURE_RESOLUTION_TFT144)
# cam.vflip = True
# cam.hflip = True
# camCmd.doSnapshot()
cam.resolution = (128,128)
cam.iso = 800
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
RST = 25  # RST may use direct +3V strapping, and then be listed as 0 here. (Soft Reset used instead)
CE = 0  # RPI GPIO: 0 or 1 for CE0 / CE1 number (NOT the pin#)
DC = 24  # RS Labeled on board as "A0"   Command/Data select
LED = 5  # LED may also be strapped direct to +3V, (and then LED=0 here). LED sinks 10-14 mA @ 3V

spi = spidev.SpiDev()
TFT = TFT144(GPIO, spi, CE, DC, RST, LED, TFT144.ORIENTATION180, isRedBoard=False)

try :
    while 1:
        print('capture')
        cam.capture('picz/image.bmp')
        print('show')
        TFT.draw_bmp("picz/image.bmp")
except: # (KeyboardInterrupt, SystemExit):
    TFT.led_on(False)
    del TFT
    del cam
# TFT.draw_bmp("bl.bmp")
