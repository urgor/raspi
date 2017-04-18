
## https://habrahabr.ru/post/149420/
# https://www.ibm.com/developerworks/ru/library/l-python_part_9/

from threading import Thread
import time

class Writer(Thread):
    def __init__(self, x): #, event_for_wait, event_for_set
        Thread.__init__(self)
        self.x = x
        # self.event_for_wait = event_for_wait
        # self.event_for_set = event_for_set

    def run(self):
        for i in range(10):
            # event_for_wait.wait() # wait for event
            # event_for_wait.clear() # clean event for future
            print('tread' + str(self.x))
            # event_for_set.set() # set event for neighbor thread
            time.sleep(self.x * 0.2)

# init events
# e1 = Thread.Event()
# e2 = Thread.Event()
# e3 = Thread.Event()

o1 = Writer(1)
o1.setName('one')
o2 = Writer(2)
o2.setName('two')
o3 = Writer(4)
o3.setName('three')

# init threads
# print('init')
# t1 = threading.Thread(target=Writer, args=(1, e1, e2))
# t2 = threading.Thread(target=Writer, args=(2, e2, e3))
# t3 = threading.Thread(target=Writer, args=(4, e3, e1))

# start threads
print('starting threads')
o1.start()
o2.start()
o3.start()

# print('set')
# e2.set() # initiate the first event

try:
    # join threads to the main thread
    print('join1')
    o1.join()
    print('join2')
    o2.join()
    print('join3')
    o3.join()
except KeyboardInterrupt:
    print('stopped')

print('main done')