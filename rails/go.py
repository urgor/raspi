import devices as dev
import commands as cmd
import time
import random
import sys
import RPi.GPIO as GPIO
import picamera

# python3-pigpio/stable 1.60-1 all
#   Python module which talks to the pigpio daemon (Python 3)

# cam = picamera.PiCamera()
# camCmd = cmd.CameraCommand(cam, 'image{:0>6}.jpg')
# camCmd.setResolution(cmd.CameraCommand.VIDEO_RESOLUTION_720)
#for _ in range(0,100):
#    print('.')
# cam.vflip = True
# cam.hflip = True
# camCmd.doSnapshot()


mr = dev.CollectorMotor([20, 21])
ml = dev.CollectorMotor([26, 19])
chasis = cmd.CaterpilarChasisCommand(ml, mr)
# chasis.initStep(.044, .03)
# chasis.initStep(.015, .01)

try:
    for i in range(0,400):
        print(i)
        chasis.doStep()
        time.sleep(.1)

except: # (KeyboardInterrupt, SystemExit):
    print()
    print('Stopping chasis normaly')
    chasis.stop()
    raise

#import curses
#stdscr = curses.initscr()
#curses.cbreak()
#print "press q to quit"
#quit=False
#while quit !=True:
#    c = stdscr.getch()
#    print curses.keyname(c),
#    ch = curses.keyname(c)
#    if ch == "q" :
#       quit=True
#    elif ch == 'd':
#        chasis.rotateRight()
#    elif ch == 'a':
#        chasis.rotateLeft()
#    elif ch == 'w':
#        chasis.forward()
#    elif ch == 's':
#        chasis.backward()
#    elif ch == ' ':
#        chasis.stop()
#curses.endwin()
#chasis.stop()
#exit()


#for _ in range(0,500):
#    chasis.forward()
#    time.sleep(0.009)
#    chasis.stop()
#    time.sleep(0.1)

# button = dev.Button(17)
# buzzer = dev.Buzzer(7)
# led = dev.Led(18)
# motor = dev.StepMotor([4,25,24,23])
# motor2 = dev.StepMotor([10,9,11,8])

# motoCommand = cmd.StepMotorCommand(motor)
# motoCommand2 = cmd.StepMotorCommand(motor2)

# motoCommand.setAngle(10)
# motoCommand2.setAngle(10)
# for _ in range(0, 10):
# 	motoCommand.setDirection(cmd.MotorCommandInterface.CLOCKWISE).do()
# 	motoCommand2.setDirection(cmd.MotorCommandInterface.CLOCKWISE).do()
# 	motoCommand.setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE).do()
# 	motoCommand2.setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE).do()

# for _ in range(0, 10):
#     motor.go(dev.StepMotor.DIR_CCW_LOW, 100, 0.0009)
#     buzzer.beep(0.1)
#     motor.go(dev.StepMotor.DIR_CW_LOW, 100, 0.0009)
#     buzzer.beep(0.1)

# motoCommand = cmd.StepMotorCommand(motor)
# for _ in range(0,10):
#   if random.randint(0, 1):
#       print 'CW'
#       motoCommand.setDirection(cmd.MotorCommandInterface.CLOCKWISE)
#   else:
#       print 'CCW'
#       motoCommand.setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE)
#   angle = random.randint(1, 60)
#   motoCommand.setAngle(angle).do()
# print('Zulu')
# buzzer.beep(0.1)
# motoCommand.returnToZulu()

# motoCommand = cmd.StepMotorCommand(motor)
# ledCommand = cmd.LedCommand(led)
# motoCommand.setAngle(1).setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE)
# while 1:
#     if not button.single_pressed():
#         continue
#     while 1:
#         motoCommand.do()
#         if button.single_pressed():
#             ledCommand.toggle()
#             buzzer.beep(0.1)
#             break


# while True:
#     if button.single_pressed():
#         print 'Push'
#         buzzer.beep(0.05).sleep(0.1).beep(0.05).sleep(0.1).beep(0.05).sleep(0.2)
#         buzzer.beep(0.1).sleep(0.1).beep(0.1).sleep(0.1).beep(0.1).sleep(0.2)
#         buzzer.beep(0.05).sleep(0.1).beep(0.05).sleep(0.1).beep(0.05)


# motoCommand = cmd.StepMotorCommand(motor)
# ledCommand = cmd.LedCommand(led)
# motoCommand.setAngle(45).setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE).setTime(10)
# while 1:
#     for _ in range(0, 10):
#         motoCommand.do()
#         ledCommand.toggle()
#         buzzer.beep(0.1)
