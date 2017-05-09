import select, sys, os, tty, fcntl, time
from threading import Thread, Event
from driver.devices import StepMotor


class KeyboardEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.char = False
        self.control = False


class MaThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__isRun = True

    @property
    def isRun(self):
        return self.__isRun

    @isRun.setter
    def setIsRun(self):
        return None

    def stop(self):
        self.__isRun = False


class KeyboardThread(MaThread):
    KB_LEFT = '\x1b[D'
    KB_RIGHT = '\x1b[C'
    KB_UP = '\x1b[A'
    KB_DOWN = '\x1b[B'
    KB_ENTER = "\n"

    def __init__(self, core):
        MaThread.__init__(self)
        self.core = core
        self.name = 'Keebod'
        self.__commands = {}
        self.poller = select.poll()
        self.poller.register(sys.stdin, select.POLLIN)
        tty.setcbreak(sys.stdin)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    @property
    def commands(self):
        return self.__commands

    @commands.setter
    def commands(self, cmds):
        for key, cmd in cmds.items():
            self.__commands[key] = cmd

    def run(self):
        while self.isRun:
            events = self.poller.poll(500)
            if events:
                print('+')
                d = sys.stdin.read()
                if not self.core.kbEvent.is_set():
                    if d[0] == '\x1b':
                        self.core.kbEvent.char = False
                        self.core.kbEvent.control = d
                    else:
                        self.core.kbEvent.char = d
                        self.core.kbEvent.control = False
                    self.core.kbEvent.set()
                    if d in self.__commands:
                        self.__commands[d]()
            else:
                print('.')
                if self.core.kbEvent.is_set():
                    self.core.kbEvent.clear()
                    self.core.kbEvent.char = False
                    self.core.kbEvent.control = False
        print(self.name + 'thread terminating')


class MotoThread(MaThread):
    def __init__(self, kbEvent, motorH, motorV):
        MaThread.__init__(self)
        self.wait_event = kbEvent
        self.motorH = motorH
        self.motorV = motorV
        self.vertSteps = 0
        self.horSteps = 0
        self.stepsExteremum = 11.3 * 90  # 90 degrees max!
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
    def __init__(self, core):
        MaThread.__init__(self)
        self.core = core
        self.name = 'Cama'

    def run(self):
        while 1:
            self.core.camEvent.wait()
            self.core.camEvent.clear()
            self.core.cam.capture('picz/image.bmp')
            self.core.tftEvent.set()


class DisplayThread(MaThread):
    def __init__(self, core):
        MaThread.__init__(self)
        self.core = core
        self.name = 'Dizplay'

    def run(self):
        while 1:
            self.core.tftEvent.wait()
            self.core.tftEvent.clear()
            self.core.tft.draw_bmp("picz/image.bmp")
            self.core.camEvent.set()


class Core():
    def __init__(self):
        self.__kb = None
        self.__tft = None
        self.__cam = None
        self.__kbEvent = None
        self.menu = None
        self.receiver = self.menu

    @property
    def kb(self):
        return self.__kb

    @property
    def tft(self):
        return self.__tft

    @property
    def cam(self):
        return self.__cam

    @property
    def kbEvent(self):
        return self.__kbEvent

    @property
    def camEvent(self):
        return self.__camEvent

    @property
    def tftEvent(self):
        return self.__tftEvent

    @kb.setter
    def kb(self, val):
        self.__kb = val

    @tft.setter
    def tft(self, val):
        self.__tft = val
        self.menu = Menu(val)

    @cam.setter
    def cam(self, val):
        self.__cam = val

    @kbEvent.setter
    def kbEvent(self, val):
        self.__kbEvent = val

    @camEvent.setter
    def camEvent(self, val):
        self.__camEvent = val

    @tftEvent.setter
    def tftEvent(self, val):
        self.__tftEvent = val

    def bindKbToMenu(self):
        self.__kb.commands = {
            KeyboardThread.KB_DOWN: Command(self.menu, 'down'),
            KeyboardThread.KB_UP: Command(self.menu, 'up'),
            KeyboardThread.KB_ENTER: Command(self.menu, 'enter')
        }

    def bindMain(self):
        self.__kb.commands = {
            'q': Command(self, 'exit')
        }

    def exit(self):
        self.__kb.stop()
        print('Core exit')
        # exit(0)

    def run(self):
        self.bindKbToMenu()
        self.bindMain()

        # if self.wait_event.control == KeyboardThread.KB_LEFT:
        #     pass
        # elif self.wait_event.control == KeyboardThread.KB_RIGHT:
        #     pass
        # elif self.wait_event.control == KeyboardThread.KB_DOWN:
        #     self.
        # elif self.wait_event.control == KeyboardThread.KB_UP:


class Menu:
    menu = [
        {
            'idx': 0,
            'name': 'Camera settings',
            'menu': [
                {
                    'idx': 0,
                    'name': '..'
                },
                {
                    'idx': 1,
                    'name': '11111111'
                },
            ]
        },
        {
            'idx': 1,
            'name': 'Capture mode'
        },
        {
            'idx': 2,
            'name': 'Something else'
        }
    ]
    fontSize = 2

    def __init__(self, tft):
        self.tft = tft
        self.clearDisplay()
        self.currentMenu = self.menu
        self.idx = 0
        self.menuSteck = []
        self.printMenu()

    def clearDisplay(self):
        self.tft.clear_display(self.tft.BLACK)

    def printMenu(self):
        for item in self.currentMenu:
            print(item)
            if item['idx'] == self.idx:
                self.tft.put_string(item['name'],
                                    self.tft.textX(0, self.fontSize),
                                    self.tft.textY(item['idx'], self.fontSize),
                                    self.tft.BLACK,
                                    self.tft.WHITE,
                                    self.fontSize)
            else:
                self.tft.put_string(item['name'],
                                    self.tft.textX(0, self.fontSize),
                                    self.tft.textY(item['idx'], self.fontSize),
                                    self.tft.WHITE,
                                    self.tft.BLACK,
                                    self.fontSize)

    def enter(self):
        if 0 != len(self.menuSteck) and 0 == self.idx:
            # cursor will stay at current menu position
            self.idx = self.menuSteck.pop()
            # search for top level menu
            self.currentMenu = self.menu
            if 0 != len(self.menuSteck):
                for i in self.menuSteck:
                    self.currentMenu = self.currentMenu[i]
            self.clearDisplay()
            self.printMenu()

        elif self.currentMenu[self.idx].get('menu'):
            self.currentMenu = self.currentMenu[self.idx].get('menu')
            self.clearDisplay()
            self.menuSteck.append(self.idx)
            self.idx = 0
            self.printMenu()

    def up(self):
        print('Menu UP')
        if (0 < self.idx):
            self.idx -= 1
            self.printMenu()

    def down(self):
        print('Menu DOWN')
        if (len(self.currentMenu) > self.idx + 1):
            self.idx += 1
            self.printMenu()


class Command:
    def __init__(self, dest, action):
        self.destination = dest
        self.action = action

    def __call__(self):
        print('invoke' + ' ' + self.action)
        getattr(self.destination, self.action)()
