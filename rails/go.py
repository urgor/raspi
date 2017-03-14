import devices as dev
import commands as cmd
import time
import random

import RPi.GPIO as GPIO

# python3-pigpio/stable 1.60-1 all
#   Python module which talks to the pigpio daemon (Python 3)



mr = dev.DcL9110([22,27])
ml = dev.DcL9110([24,23])
chasis = cmd.CaterpilarChasisCommand(ml, mr)
chasis.forward()
time.sleep(3)
chasis.rotateRight()
time.sleep(3)
chasis.backward()
time.sleep(3)
chasis.rotateLeft()
time.sleep(3)
chasis.stop()

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
