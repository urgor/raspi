

# читает по символьно, но можно раздуплить нажатия на курсок
# import sys, tty, termios
#
# while 1:
#     print(1)
#     fd = sys.stdin.fileno()
#     print(2)
#     old_settings = termios.tcgetattr(fd)
#     try:
#         print(3)
#         tty.setraw(fd)
#         print(4)
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     print(ch)
#     if 'q' == ch:
#         exit()