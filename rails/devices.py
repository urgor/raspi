
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)

class Button():
    def __init__(self, pin):
        self.pin = pin
        self.previous = True

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( pin, GPIO.IN )

    def pressed(self):
        """ Allow multiple triggering """
        return not GPIO.input( self.pin )

    def single_pressed(self):
        """ Prevent mutiple triggering """
        state = GPIO.input( self.pin )
        if self.previous != state:
            self.previous = state
            return not state
        else:
            return False


class Buzzer():
    def __init__(self, pin):
        self.pin = pin
        self.delay = 0.001

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( pin, GPIO.OUT )

    def beep(self, duration):
        repeats = round(duration / self.delay)
        while repeats > 0:
            GPIO.output(self.pin, False)
            time.sleep(self.delay)
            GPIO.output(self.pin, True)
            time.sleep(self.delay)
            repeats -= 1
        return self

    def sleep(self, duration):
        time.sleep(duration)
        return self

class Led():
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( pin, GPIO.OUT )

    def on(self):
        GPIO.output(self.pin, False)
        return self

    def off(self):
        GPIO.output(self.pin, True)
        return self

class StepMotor():
    DIR_CW_LOW = 1
    DIR_CW_HI = 2
    DIR_CCW_LOW = -1
    DIR_CCW_HI = -2
    MINIMUM_DELAY = 0.0009

    def __init__(self, pins):
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        self.pins = pins
        self.stepCounter = 0

        # Set all pins as output
        for pin in self.pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        # Define advanced sequence
        # as shown in manufacturers datasheet
        self.seq = [
                [True,  False,  False,  True],
                [True,  False,  False,  False],
                [True,  True,   False,  False],
                [False, True,   False,  False],
                [False, True,   True,   False],
                [False, False,  True,   False],
                [False, False,  True,   True],
                [False, False,  False,  True]]

        self.stepCount = len(self.seq)

    def go(self, direction, steps, waitTime = 0):
        if 0 == waitTime: waitTime = self.MINIMUM_DELAY
        for _ in xrange(1, steps):

            for pin in range(0,4):
                GPIO.output(self.pins[pin], self.seq[self.stepCounter][pin])

            self.stepCounter += direction

            # If we reach the end of the sequence
            # start again
            if (self.stepCounter >= self.stepCount):
                self.stepCounter = 0
            if (self.stepCounter < 0):
                self.stepCounter += direction

            # Wait before moving on
            time.sleep(waitTime)
            for pin in range(0,4):
                GPIO.output(self.pins[pin], False)
