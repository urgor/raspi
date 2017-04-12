import time

from devices import CollectorMotor


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

class CaterpilarChasisCommand():
    def __init__(self, motor_left, motor_right):

        assert isinstance(motor_left, CollectorMotor)
        assert isinstance(motor_right, CollectorMotor)
        self.left = motor_left
        self.right = motor_right
        self.delayLeft = None
        self.delayRight = None
        self.strategyStop = CaterpilarStrategyStop(motor_left, motor_right)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def forward(self):
        self.left.forward()
        self.right.forward()

    def backward(self):
        self.left.backward()
        self.right.backward()

    def rotateRight(self):
        self.left.forward()
        self.right.backward()

    def rotateLeft(self):
        self.left.backward()
        self.right.forward()

    def initStep(self, delay_left, delay_right):
        """
        Define pulse length (work time of each caterpilar)
        Then you may invoke doStep()
        """
        if delay_left > delay_right:
            self.strategyStop = CaterpilarStrategyStopRight(self.left, self.right)
        elif delay_left < delay_right:
            self.strategyStop = CaterpilarStrategyStopLeft(self.left, self.right)
        else:
            self.strategyStop = CaterpilarStrategyStopTogether(self.left, self.right)
        self.delayLeft = delay_left
        self.delayRight = delay_right

    def doStep(self):
        """
        Make step using previously initialized data by initStep()
        """
        self.left.forward()
        self.right.forward()
        self.strategyStop.stop(self.delayLeft, self.delayRight)

class CaterpilarStrategyStop:
    def __init__(self, motor_left, motor_right):
        assert isinstance(motor_left, CollectorMotor)
        assert isinstance(motor_right, CollectorMotor)
        self.left = motor_left
        self.right = motor_right

    def stop(self, delay_left, delay_right):
        raise Exception('This class should be not instanced or use Caterpilar.initStep() first')

class CaterpilarStrategyStopLeft(CaterpilarStrategyStop):
    def stop(self, delay_left, delay_right):
        time.sleep(delay_left)
        self.left.stop()
        time.sleep(delay_right - delay_left)
        self.right.stop()

class CaterpilarStrategyStopRight(CaterpilarStrategyStop):
    def stop(self, delay_left, delay_right):
        time.sleep(delay_right)
        self.right.stop()
        time.sleep(delay_left - delay_right)
        self.left.stop()

class CaterpilarStrategyStopTogether(CaterpilarStrategyStop):
    def stop(self, delay_left, delay_right):
        time.sleep(delay_right)
        self.right.stop()
        self.left.stop()


class ServoCommand:
    def __init__(self, motor):
        self.motor = motor
    
    def goMin(self):
        self.motor.go(self.motor.extremum[0])
        
    def goMax(self):
        self.motor.go(self.motor.extremum[1])
        
    def goMiddle(self):
        self.motor.go(int(round((self.motor.getMin() + self.motor.getMax()) / 2)))
        
    def increment(self, value = 1):
        self.motor.go(self.motor.getCurrent() + value)
        
    def decrement(self, value = 1):
        self.motor.go(self.motor.getCurrent() - value)
        
class CameraCommand:
    PICTURE_RESOLUTION_MAX = (3280, 2464)
    VIDEO_RESOLUTION_720 = (1280, 720)
    
    def __init__(self, camera, filename):
        self.camera = camera
        self.i = 0
        self.filename = filename
        
    def setResolution(self, resolution):
        self.camera.resolution = resolution
        
    def doSnapshot(self):
        self.camera.capture(self.filename.format(self.i))
        self.i += 1
        
#camera.start_recording('video', 'mjpeg')
#time.sleep(10)
#camera.stop_recording()