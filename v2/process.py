from message import Message
from queue import Queue
import threading
import time

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, id, root_id, neighbor_ids, q, head):
        threading.Thread.__init__(self)
        self.processID = id
        self.neighbor_ids = neighbor_ids
        self.root_id = root_id
        self.q = q
        self.cnt = 2
        self.head = head

        #print(f'{self.processID}, {self.root_id}')
        if self.processID == self.root_id:
            #print('Marked')
            self.marked = True
        else:
            self.marked = False


    def run(self):
        print(f"\n\nStarted Thread-{self.processID}")
        print(f'{self.processID}: my neighbors are {self.neighbor_ids}')

        #print(f'Marked: {self.marked}')
        while self.marked != True:

            self.cnt = self.cnt - 1
            #threadLock.acquire()
            #self.q, obj = self.queue_peek(self.q)
            #obj = self.peek(self.q)
            #threadLock.release()
            if self.head is None:
                if not self.q.empty():
                    self.head = self.q.get()
                    if self.processID == 6:
                        print(f'Head: {self.head}')

            #print(f'Process-{self.processID} - Queue empty: {self.q.empty()}')
            #if self.head is not None and self.processID == 6:
            #    print(f'\nProcess-{self.processID} : Receiver: {self.head.receiverID}')

            if self.head is not None and self.head.receiverID == self.processID:
                print(f'\nProcess-{self.processID} : Receiver matched')
                self.receive_message(self.head.senderID)


        # Get lock to synchronize threads
        threadLock.acquire()
        if self.marked and len(self.neighbor_ids) > 0:
            for i in range(len(self.neighbor_ids)):
                self.send_message(self.neighbor_ids[i])
        # Free lock to release next thread
        threadLock.release()


    def mark(self):
        self.marked = True


    def set_parent(self, parent):
        self.parent = parent


    def send_message(self, receiver):
        msg = Message(self.processID, int(receiver), False)
        print(msg)
        self.q.put(msg)
        #print(f'Message sent: {self.q.empty()}')


    def receive_message(self, sender):
        self.head = None
        # Mark the process
        self.mark()
        self.set_parent(sender)
        print("{} -- Parent set to {}".format(self.processID, self.parent.processID))


def print_time(threadName, counter):
    while counter:
        time.sleep(2)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
