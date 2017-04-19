from threading import Event, Thread
from my_input import KeyboardT

class KeyboardEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.char = False
        self.control = False

# class StepMotorEvent(Event):
#     def __init__(self):
#         Event.__init__(self)
#         self.direction = False


class MotoT(Thread):
    def __init__(self, wait_event):  # , event_for_wait, event_for_set
        Thread.__init__(self)
        self.wait_event = wait_event
        self.name = 'Moto thread'

    def run(self):
        while 1:
            self.wait_event.wait()
            self.wait_event.clear()
            if self.wait_event.control:
                print('Motor begin move ' + self.wait_event.control)
            else:
                print('Motor stop')
            # event_for_set.set() # set event for neighbor thread

kb_Event = KeyboardEvent()

moto = MotoT(kb_Event)
ma_input = KeyboardT(kb_Event)

moto.start()
ma_input.start()

try:
    moto.join()
    ma_input.join()
except KeyboardInterrupt:
    del moto
    del ma_input
    print('stopped')

print('main done')