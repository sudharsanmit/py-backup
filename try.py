import threading
import time
import logging
import queue
import importlib
#from multiprocessing import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-20s) %(message)s',
                    )
def worker(num=1):
    time.sleep(1)
    logging.info ('Worker %s' %num)

@worker
def daemon(num):
    logging.debug ('Starting Daemon %s' %num)
    logging.debug ('Ending Daemon %s' %num)

d = threading.Thread(name='daemon',target=daemon,args=(1,))
d.setDaemon(True)

d.start()

for t in threading.enumerate():
    logging.info('thread %s is active', t.getName())


def wait_for_event_timeout(*events):
    while not all([e.is_set() for e in events]):
#Check to see if the event is set. Timeout 1 sec.
        ev_wait_bool=[e.wait(1) for e in events]
# Process if all events are set. Change all to any to process if any event set
        if all(ev_wait_bool):
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


e1 = threading.Event()
e2 = threading.Event()

t3 = threading.Thread(name='non-block-multi',
                      target=wait_for_event_timeout,
                      args=(e1,e2))
t3.start()

logging.debug('Waiting before calling Event.set()')
time.sleep(1)
e1.set()
time.sleep(1)
e2.set()
logging.debug('Event is set')
t3.join()

q=queue.Queue()
for i in range(10):
    q.put(i) 

def getItem(q,timeout):
    while not q.empty():
        logging.debug(q.get())
        logging.debug('GetItem complete')


t1 = threading.Thread(name='Q1',target=getItem,args=(q,1))
t2 = threading.Thread(name='Q2',target=getItem,args=(q,1))
t1.start()
t2.start()
logging.debug('Process complete')


### importlib example

a=importlib.import_module('test')
obj=getattr(a,'A')(args=(1,2))
obj.b(1,2)

a=importlib.import_module('test')
obj=getattr(a,'A').b(4,5)
