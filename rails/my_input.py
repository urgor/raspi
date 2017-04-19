import sys
import select
import tty
import termios
from threading import Thread

class NonBlockingConsole(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)
            if c == '\x1b':
                c += sys.stdin.read(2)
            return c
        return False

class KeyboardT(Thread):
    def __init__(self, event_to_rise):
        Thread.__init__(self)
        self.event_to_rise = event_to_rise
        self.name = 'KEyboard thread'

    def run(self):
        with NonBlockingConsole() as nbc:
            while 1:
                d = nbc.get_data()
                if not d:
                    if self.event_to_rise.is_set():
                        self.event_to_rise.char = False
                        self.event_to_rise.control = False
                    continue

                if d == '\x1b[A':
                    # print("up")
                    self.event_to_rise.char = False
                    self.event_to_rise.control = 'up'
                    self.event_to_rise.set()
                elif d == '\x1b[B':
                    # print("down")
                    self.event_to_rise.char = False
                    self.event_to_rise.control = 'down'
                    self.event_to_rise.set()
                elif d == '\x1b[C':
                    # print("right")
                    self.event_to_rise.char = False
                    self.event_to_rise.control = 'right'
                    self.event_to_rise.set()
                elif d == '\x1b[D':
                    # print("left")
                    self.event_to_rise.char = False
                    self.event_to_rise.control = 'left'
                    self.event_to_rise.set()
                # else:
                #     print(d)

                if d == 'q':
                    break

# if __name__ == '__main__':
