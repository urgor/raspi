import select, sys, os, tty, fcntl, time
from threading import Thread, Event
from driver.devices import StepMotor

class MaThread(Thread):
    def __init__(self):
        Thread.__init__(self)


class KeyboardThread(MaThread):
    KB_LEFT = '\x1b[D'
    KB_RIGHT = '\x1b[C'
    KB_UP = '\x1b[A'
    KB_DOWN = '\x1b[B'
    def __init__(self, event_to_rise):
        MaThread.__init__(self)
        self.event_to_rise = event_to_rise
        self.name = 'Keebod'
        self.poller = select.poll()
        self.poller.register(sys.stdin, select.POLLIN)
        tty.setcbreak(sys.stdin)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    def run(self):
        while True:
            events = self.poller.poll(500)
            if events:
                print('+')
                d = sys.stdin.read()
                if not self.event_to_rise.is_set():
                    if d[0] == '\x1b':
                        self.event_to_rise.char = False
                        self.event_to_rise.control = d
                    else:
                        self.event_to_rise.char = d
                        self.event_to_rise.control = False
                    self.event_to_rise.set()
                    if 'q' == d:
                        print(self.name + ' thread ending.')
                        time.sleep(.5)
                        return
            else:
                print('.')
                if self.event_to_rise.is_set():
                    self.event_to_rise.clear()
                    self.event_to_rise.char = False
                    self.event_to_rise.control = False

class KeyboardEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.char = False
        self.control = False

class MotoThread(MaThread):
    def __init__(self, kbEvent, motorH, motorV):
        MaThread.__init__(self)
        self.wait_event = kbEvent
        self.motorH = motorH
        self.motorV = motorV
        self.vertSteps = 0
        self.horSteps = 0
        self.stepsExteremum = 11.3 * 90 # 90 degrees max!
        self.name = 'Motoz'
        self.step = 10
        self.motoMinimumDelay = .01

    def run(self):
        while 1:
            self.wait_event.wait()
            print(self.wait_event.char)
            if 'q' == self.wait_event.char:
                print(self.name + ' thread ending.')
                return
            while 1:
                time.sleep(.01)
                if self.wait_event.is_set():
                    if self.wait_event.control == KeyboardThread.KB_LEFT:
                        if self.horSteps - self.step > -self.stepsExteremum:
                            self.horSteps -= self.step
                            self.motorH.go(StepMotor.DIR_CCW_LOW, self.step, self.motoMinimumDelay)
                    if self.wait_event.control == KeyboardThread.KB_RIGHT:
                        if self.horSteps + self.step < self.stepsExteremum:
                            self.horSteps += self.step
                            self.motorH.go(StepMotor.DIR_CW_LOW, self.step, self.motoMinimumDelay)
                    if self.wait_event.control == KeyboardThread.KB_DOWN:
                        if self.vertSteps - self.step > -self.stepsExteremum:
                            self.vertSteps -= self.step
                            self.motorV.go(StepMotor.DIR_CCW_LOW, self.step, self.motoMinimumDelay)
                    if self.wait_event.control == KeyboardThread.KB_UP:
                        if self.vertSteps + self.step < self.stepsExteremum:
                            self.vertSteps += self.step
                            self.motorV.go(StepMotor.DIR_CW_LOW, self.step, self.motoMinimumDelay)
                    if self.wait_event.control == KeyboardThread.KB_UP:
                        pass
                    if self.wait_event.control == KeyboardThread.KB_DOWN:
                        pass
                # else:
                #     print('motor stop')
                #     break


class CameraThread(MaThread):
    def __init__(self, camEvent, tftEvent, camera):
        MaThread.__init__(self)
        self.camEvent = camEvent
        self.tftEvent = tftEvent
        self.cam = camera
        self.name = 'Cama'
    def run(self):
        while 1:
            self.camEvent.wait()
            self.camEvent.clear()
            self.cam.capture('picz/image.bmp')
            self.tftEvent.set()

class DisplayThread(MaThread):
    def __init__(self, camEvent, tftEvent, display):
        MaThread.__init__(self)
        self.camEvent = camEvent
        self.tftEvent = tftEvent
        self.tft = display
        self.name = 'Dizplay'
    def run(self):
        while 1:
            self.tftEvent.wait()
            self.tftEvent.clear()
            self.tft.draw_bmp("picz/image.bmp")
            self.camEvent.set()

class Core(MaThread):
    def __init__(self, camEvent, tftEvent, tft):
        MaThread.__init__(self)
        self.name = 'Core'