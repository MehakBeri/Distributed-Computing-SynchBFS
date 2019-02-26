from message import Message
import threading

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, pid, root_id, neighbor_ids,q, config):
        threading.Thread.__init__(self)
        self.pid = pid
        self.neighbor_ids = neighbor_ids
        self.root_id = root_id
        self.parent = config[pid]['parent']
        self.children = config[pid]['children']
        self.marked = config[pid]['marked']
        self.q = config[pid]['q']
        self.sent = config[pid]['sent']
        self.roundNumber = config[pid]['r']
        if int(self.pid) == int(self.root_id):
            self.marked=True
            self.parent = 0

    def run(self):
            self._run()
    
    def _run(self):
        if self.marked and len(self.neighbor_ids) > len(self.sent):
            #print(f'{self.pid} in sec1')
            for i in range(len(self.neighbor_ids)):
                if self.parent != self.neighbor_ids[i]:
                    self.sent.append(self.neighbor_ids[i])
                    self.send_message(self.neighbor_ids[i])
        pending_msgs = 0
        snapshot = list(self.q.queue)
        for msg in snapshot:
            if msg.receiverID==self.pid and (int(msg.msg_type.split(':')[1])<self.roundNumber):
                pending_msgs += 1
        #print(f'{self.pid} pending msgs: {pending_msgs}')
        while(pending_msgs!=0):
            threadLock.acquire()
            tmp = self.q.get()
            threadLock.release()
            if tmp.receiverID==self.pid and (int(tmp.msg_type.split(':')[1])<self.roundNumber):
                if ('inter-thread' in tmp.msg_type) :
                    #print(f'{self.pid}: Receiving msg {tmp}, {self.q.qsize()}')
                    self.receive_message(tmp.senderID)
                elif ('inform-parent' in tmp.msg_type) :
                    #print(f'{self.pid} -- Added {tmp.senderID} to my children')
                    if tmp.senderID not in self.children:
                        self.children.append(tmp.senderID)
                pending_msgs -= 1
            else:
                threadLock.acquire()
                self.q.put(tmp)
                threadLock.release()

        #print(f'{self.pid} in sec4. Pending msgs {pending_msgs}')
        done_msg = {'parent': self.parent,
                    'children':self.children,
                    'marked':self.marked,
                    'sent':self.sent,
                    'r':self.roundNumber+1,
                    'q':self.q
                    }
        threadLock.acquire()
        self.q.put(Message(self.pid, 'Master', done_msg))
        threadLock.release()
        #print(f'{self.pid} rel')

    def set_parent(self, parent):
        self.parent = parent

    def send_message(self, receiver):
        msg = Message(self.pid, int(receiver), 'inter-thread:' + str(self.roundNumber))
        threadLock.acquire()
        self.q.put(msg)
        threadLock.release()
        #print(f'{self.pid}: sent {msg} to queue, {self.q.qsize()}')
        
    def receive_message(self, sender):
        if not self.marked:
            self.mark_me()
            self.set_parent(sender)
            self.inform_parent(sender)

    def mark_me(self, r=None):
        #if r==None:
        #    r=self.roundNumber
        self.marked = True
        print '|| BFS LEVEL: {0}'.format(self.pid)

    def inform_parent(self, sender):
        threadLock.acquire()
        self.q.put(Message(self.pid, int(sender), 'inform-parent:' + str(self.roundNumber)))
        threadLock.release()
        #print(f'{self.pid} -- informing parent {sender}')

