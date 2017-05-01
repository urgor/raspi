import select, sys, os, tty, fcntl

poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

tty.setcbreak(sys.stdin)

fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

while True:
    events = poller.poll(500)
    if events:
        # for char in sys.stdin.read():
        #     print(str(ord(char)))
        d = sys.stdin.read()
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
    else:
        print('.')


exit()

import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []

if __name__ == '__main__':
    atexit.register(set_normal_term)
    set_curses_term()

    while 1:
        if kbhit():
            ch = getch()
            break
        sys.stdout.write('.')

    print('done')