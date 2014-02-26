import logging
logging.basicConfig(filename='thread_demo.log',
                    level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d  %(threadName)-16s %(levelname)-6s %(message)s', 
                    datefmt='%H:%M:%S')

import threading
import Queue
import numpy as np

procstack = 10

def fill(outq):
    logging.debug("Starting Fill thread")
    for i in range(procstack):
        logging.debug("fill %4i started" % (i))
        outq.put(np.random.rand(1000,10000))
        logging.debug("fill %4i complete" % (i))
    logging.debug("sending kill to que")
    outq.put("END")

def proc(inq, outq):
    logging.debug("Starting Processing Thread")
    i = 0
    while True:
        data = inq.get()
        if data == "END" :
            inq.put("END")
            logging.debug("proc found end statement, finishing")
            return
        logging.debug("proc %4i started" % (i))
        outq.put(np.sin(np.log(data)))
        logging.debug("proc %4i complete" % (i))
        i+=1
    logging.debug("Finished Processing Thread")

def plot(inq):
    logging.debug("Starting Plotting Thread")
    for i in range(procstack):
        data = inq.get()
        logging.debug("plot %4i started" % (i))
        m = np.mean(data)
        logging.debug("plot %4i complete" % (i))
    logging.debug("Finished Processing Thread")

q1 = Queue.Queue()
q2 = Queue.Queue()

f = threading.Thread(name='FillingThread', target=fill, args = (q1,))
f.daemon = True

p = threading.Thread(name='PlottingThread', target=plot, args = (q2,))
p.daemon = True

ps = []
for i in range(4):
    pp = threading.Thread(name='ProcessingThread-%02i' % (i), target=proc, args = (q1,q2))
    pp.daemon = True
    pp.start()
    ps.append(pp)


p.start()
f.start()

p.join()

logging.debug("All Done")
