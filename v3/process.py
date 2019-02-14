from message import Message
from queue import Queue
import threading
import time

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, pid, root_id, neighbor_ids, q, head=None):
        threading.Thread.__init__(self)
        self.pid = pid
        self.neighbor_ids = neighbor_ids
        self.root_id = root_id
        self.q = q
        self.head = head
        self.start_signal = False
        self.marked = False
        if int(self.pid) == int(self.root_id):
            self.marked = True
    
    def run(self):
        print(f'{self.pid}: my neighbors are {self.neighbor_ids}. {self.root_id} Marking: {self.marked}, {self.q.qsize()}')
        if not self.start_signal:
            brd = self.q.get()
            if brd.senderID == 'Master' and brd.receiverID == self.pid:
                print(f'{self.pid}: broadcast msg received {brd.msg_type}. Starting to run, {self.q.qsize()}')
                self.start_signal = True
                self._run()

    def _run(self):
        while self.marked != True and self.start_signal:
            if self.head is None:
                if not self.q.empty():
                    self.head = self.q.get()
            if self.head is not None and self.head.receiverID == self.pid and self.head.msg_type=='inter-thread':
                print(f'{self.pid} : Received msg {self.head.msg_type}')
                self.receive_message(self.head.senderID)
        # Get lock to synchronize threads
        threadLock.acquire()
        if self.marked and self.start_signal and len(self.neighbor_ids) > 0:
            for i in range(len(self.neighbor_ids)):
                self.send_message(self.neighbor_ids[i])
        self.start_signal = False
        if not self.start_signal :
            self.q.put(Message(self.pid, 'Master', int(self.pid))) #done msg
        # Free lock to release next thread
        threadLock.release()

    def set_parent(self, parent):
        self.parent = parent

    def send_message(self, receiver):
        msg = Message(self.pid, int(receiver), 'inter-thread')
        print(f'{self.pid}: sending {msg} to queue, {self.q.qsize()}')
        self.q.put(msg)
        print(f'{self.pid}: sent {msg} to queue, {self.q.qsize()}')
        
    def receive_message(self, sender):
        self.head = None
        # Mark the process
        self.mark()
        self.set_parent(sender)
        print("{} -- Parent set to {}".format(self.pid, self.parent))


def print_time(threadName, counter):
    while counter:
        time.sleep(2)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
