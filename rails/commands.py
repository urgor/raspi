import time

class MotorCommandInterface():
    CLOCKWISE = 1
    CROSSCLOCKWISE = -1

    def setDirection(self):
        raise Exception
    def setAngle(self):
        raise Exception
    def setTime(self):
        raise Exception
    def do(self):
        raise Exception

class StepMotorCommand(MotorCommandInterface):
    def __init__(self, motor):
        if 'StepMotor' !=  motor.__class__.__name__:
            raise Exception
        self.motor = motor
        self.directrion = MotorCommandInterface.CLOCKWISE
        self.angle = 0
        self.time = 0
        self.rememberedSteps = 0

    def setDirection(self, direction):
        """ Direction to rotate """
        # time.sleep(self.motor.MINIMUM_DELAY)
        self.direction = direction
        return self

    def setAngle(self, angle):
        """ ANgle to rotate the axis """
        self.angle = angle
        return self

    def setTime(self, time):
        """ Time (s) to do the rotate """
        self.time = time
        return self

    def do(self):
        steps = self.angle * 11.3
        if 0 == self.time:
            pause = self.motor.MINIMUM_DELAY
        else:
            pause = self.time / steps

        if self.motor.MINIMUM_DELAY > pause:
            raise Exception('Too fast')

        steps = int(round(steps))
        self.rememberedSteps += self.direction * steps
        self.motor.go(self.direction, steps, pause)

        return self

    def rememberZulu(self):
        """ Remember current position """
        self.rememberedSteps = 0
        return self

    def returnToZulu(self):
        """ Return axis to remembered position """
        # time.sleep(self.motor.MINIMUM_DELAY)

        self.motor.go(
            self.CLOCKWISE if self.rememberedSteps < 0 else self.CROSSCLOCKWISE,
            abs(self.rememberedSteps))

        self.rememberedSteps = 0;
        return self

class LedCommand():
    def __init__(self, led):
        if 'Led' !=  led.__class__.__name__:
            raise Exception
        self.led = led
        self.state = False

    def on(self):
        self.led.on()
        return self

    def off(self):
        self.led.off()
        return self

    def toggle(self):
        if self.state:
            self.led.off()
        else:
            self.led.on()
        self.state = not self.state
        return self