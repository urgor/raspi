import devices as dev
import commands as cmd
import time
import picamera


cam = picamera.PiCamera()
cam.vflip = True
cam.hflip = True
camCmd = cmd.CameraCommand(cam, 'picz/image{:0>6}.jpg')
camCmd.setResolution(cmd.CameraCommand.VIDEO_RESOLUTION_720)

mr = dev.CollectorMotor([20, 21])
ml = dev.CollectorMotor([26, 19])
chasis = cmd.CaterpilarChasisCommand(ml, mr)

for _ in range(1173,10000):
    camCmd.doSnapshot()
    chasis.forward()
    time.sleep(0.009)
    chasis.stop()
    time.sleep(0.1)