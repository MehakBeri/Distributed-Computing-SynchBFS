from message import Message
from queue import Queue
import threading
import time

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, id, root_id, neighbor_ids, q):
        threading.Thread.__init__(self)
        self.processID = id
        self.neighbor_ids = neighbor_ids
        self.root_id = root_id
        self.q = q
        self.cnt = 2
        self.temp = None

        #print(f'{self.processID}, {self.root_id}')
        if self.processID == self.root_id:
            #print('Marked')
            self.marked = True
        else:
            self.marked = False


    def run(self):
        print(f"\n\nStarting Thread-{self.processID}")
        print(f'{self.processID}: my neighbors are {self.neighbor_ids}')

        # Get lock to synchronize threads
        threadLock.acquire()
        if self.marked and len(self.neighbor_ids) > 0:
            for i in range(len(self.neighbor_ids)):
                self.send_message(self.neighbor_ids[i])
        # Free lock to release next thread
        threadLock.release()


        while self.cnt > 0:
            self.cnt = self.cnt - 1
            #threadLock.acquire()
            #self.q, obj = self.queue_peek(self.q)
            obj = self.peek(self.q)
            #threadLock.release()
            print(f'Process-{self.processID} - Queue empty: {self.q.empty()}')
            print(f'\nProcess-{self.processID} : Receiver matched: {obj.receiverID == self.processID}')


    def queue_peek(self, q):
        obj = q.get()
        tmp_q = Queue()
        tmp_q.put(obj)
        while not q.empty():
            tmp_obj = q.get()
            tmp_q.put(tmp_obj)
        print(f'Process-{self.processID} ---- Inside peek: {tmp_q.empty()}')
        return tmp_q, obj


    def peek(self, q):
        if self.temp == None:
            self.temp = q.get()
        print(f'Process-{self.processID} ---- Inside peek: {tmp_q.empty()}')
        return self.temp


    def mark(self):
        self.marked = True


    def set_parent(self, parent):
        self.parent = parent


    def send_message(self, receiver):
        msg = Message(self.processID, receiver, False)
        print(msg)
        self.q.put(msg)


    def receive_message(self, sender):
        if self.marked != True:
            self.mark()
            self.set_parent(sender)
            print("{} -- Parent set to {}".format(self.processID, self.parent.processID))


def print_time(threadName, counter):
    while counter:
        time.sleep(2)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
