
import sys
import select
import tty
import termios

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


if __name__ == '__main__':
    # Use like this
    with NonBlockingConsole() as nbc:
        i = 0
        while 1:
            d = nbc.get_data()
            if not d:
                continue

            if d == '\x1b[A':
                print("up")
            elif d == '\x1b[B':
                print("down")
            elif d == '\x1b[C':
                print("right")
            elif d == '\x1b[D':
                print("left")
            else:
                print(d)

            if d == 'q':
                break
