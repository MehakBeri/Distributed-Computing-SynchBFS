from message import Message
from queue import Queue
import threading
import time

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, pid, root_id, neighbor_ids, q):
        threading.Thread.__init__(self)
        self.pid = pid
        self.neighbor_ids = neighbor_ids
        self.root_id = root_id
        self.q = q
        self.marked = False
        self.parent=None
        self.children=[]
        if int(self.pid) == int(self.root_id):
            self.marked = True
            self.parent = 'Root'

    def run(self):
        print(f'{self.pid}: my neighbors are {self.neighbor_ids}. {self.root_id} Marking: {self.marked}, {self.q.qsize()}')
        while True: 
            threadLock.acquire()
            tmp = self.q.get()
            threadLock.release()
            if tmp.receiverID == self.pid and tmp.senderID=='Master' and tmp.msg_type.split('-')[0]=='broadcast':
                print(f'{self.pid}: BROADCAST {tmp.msg_type}, {self.q.qsize()}') 
                self._run()
                print(f'{self.pid}: returned after {tmp.msg_type}')
            elif tmp.receiverID == self.pid and tmp.senderID=='Master' and tmp.msg_type=='terminate':
                print(f'{self.pid}: TERMINATE {tmp.msg_type}, {self.q.qsize()}') 
                break
            else:
                threadLock.acquire()
                self.q.put(tmp)
                threadLock.release()
            
    
    def _run(self):
        if self.marked and len(self.neighbor_ids) > 0 and len(self.children)==0:
            for i in range(len(self.neighbor_ids)):
                if self.parent != self.neighbor_ids[i]:
                    self.send_message(self.neighbor_ids[i])
        
        if not self.q.empty() and self.parent==None:
            curr_size = self.q.qsize()
            print(f'{self.pid}: curr q size: {curr_size}')
            for i in range(curr_size):
                threadLock.acquire()
                tmp = self.q.get()
                threadLock.release()
                if tmp.receiverID == self.pid and tmp.msg_type=='inter-thread':
                    print(f'{self.pid}: Receiving msg {tmp}, {self.q.qsize()}')
                    self.receive_message(tmp.senderID)
                    break
                else:
                    threadLock.acquire()
                    self.q.put(tmp)
                    threadLock.release()

        if not self.q.empty():
            curr_size = self.q.qsize()
            for i in range(curr_size):
                threadLock.acquire()
                tmp = self.q.get()
                threadLock.release()
                if tmp.receiverID == self.pid and tmp.msg_type== 'inform-parent':
                    print(f'{self.pid}: Added {tmp.senderID} to my children')
                    self.children.append(tmp.senderID)
                    break
                else:
                    threadLock.acquire()
                    self.q.put(tmp)
                    threadLock.release()

        print(f'{self.pid}: I am done')
        threadLock.acquire()
        self.q.put(Message(self.pid, 'Master', 'complete'))
        threadLock.release()

    def set_parent(self, parent):
        self.parent = parent

    def send_message(self, receiver):
        msg = Message(self.pid, int(receiver), 'inter-thread')
        print(f'{self.pid}: sending {msg} to queue, {self.q.qsize()}')
        threadLock.acquire()
        self.q.put(msg)
        threadLock.release()
        print(f'{self.pid}: sent {msg} to queue, {self.q.qsize()}')
        
    def receive_message(self, sender):
        self.head = None
        self.marked = True
        self.set_parent(sender)
        print("{} -- Parent set to {}".format(self.pid, self.parent))
        self.inform_parent(sender)

    def inform_parent(self, sender):
        threadLock.acquire()
        self.q.put(Message(self.pid, int(sender), 'inform-parent'))
        threadLock.release()
        print(f'{self.pid} -- informing parent {sender}')


def print_time(threadName, counter):
    while counter:
        time.sleep(2)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
