import devices as dev
import commands as cmd
import time
import random

button = dev.Button(17)
buzzer = dev.Buzzer(7)
led = dev.Led(18)
motor = dev.StepMotor([4,25,24,23])

# for _ in range(0, 10):
#     motor.go(dev.StepMotor.DIR_CCW_LOW, 100, 0.0009)
#     buzzer.beep(0.1)
#     motor.go(dev.StepMotor.DIR_CW_LOW, 100, 0.0009)
#     buzzer.beep(0.1)

motoCommand = cmd.StepMotorCommand(motor)
for _ in range(0,10):
  if random.randint(0, 1):
      print 'CW'
      motoCommand.setDirection(cmd.MotorCommandInterface.CLOCKWISE)
  else:
      print 'CCW'
      motoCommand.setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE)
  angle = random.randint(1, 60)
  motoCommand.setAngle(angle).do()
print('Zulu')
buzzer.beep(0.1)
motoCommand.returnToZulu()

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
