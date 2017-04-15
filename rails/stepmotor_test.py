import devices as dev
import commands as cmd

motorH = dev.StepMotor([26,19,13,6])
motorV = dev.StepMotor([12,16,20,21])

horizontal = cmd.StepMotorCommand(motorH)
vertical = cmd.StepMotorCommand(motorV)

horizontal.setAngle(45)
vertical.setAngle(45)
for _ in range(0,2):
    horizontal.setDirection(cmd.MotorCommandInterface.CCW).do()
    vertical.setDirection(cmd.MotorCommandInterface.CCW).do()
    horizontal.setDirection(cmd.MotorCommandInterface.CW).do()
    vertical.setDirection(cmd.MotorCommandInterface.CW).do()
# vertical.setAngle(90).setDirection(cmd.MotorCommandInterface.CROSSCLOCKWISE).do()

exit()