from queue import Queue
import threading
import time
import sys

class process_thread(threading.Thread):
    global id_process, id_label
    def __init__(self, threadID, rootid, conn, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.children = []
        self.conn = conn
        self.rootid = rootid
        self.q = q
        self.parent=None
        if str(self.threadID) == str(self.rootid):
            print('marked')
            self.mark = True
            self.parent = 'Dummy'
        else:
            self.mark = False
            self.parent = None

    def run(self):
        '''
        if str(self.threadID) == str(self.rootid):
            print('marked')
            self.mark = True
            self.parent = 'Dummy'
        else:
            self.mark = False
            self.parent = None
        '''
        self.neighbors = []
        self.neighbor_ids = []
        for i in range(len(self.conn)):
            if (self.conn[i]==1 and id_label[i]!=self.threadID):
                self.neighbor_ids.append(id_label[i])
        '''
        for n in self.neighbor_ids: # might not need thread objects passed since sending msgs now
            if n!= self.threadID:
                self.neighbors.append(id_process[n])
        '''
        print(f'{self.threadID}: my neighbors are {self.neighbor_ids}, my mark {self.mark}')
        if self.mark:
            self.q.put(f'{self.threadID}|2|test')
            print(f'msg sent from {self.threadID}')
        while True:
            #self.q, msg = queue_peek(self.q)
            msg = self.q.get()
            sender = msg.split('|')[0]
            rec = msg.split('|')[1]
            mtype = msg.split('|')[2]
            print(f'{rec}:{self.threadID}')
            print(f'{self.q.empty()}')
            if str(rec)==str(self.threadID):
                print(f'{self.threadID}: msg {msg} intended for me')
                #incoming_msg = self.q.get()
                #print(f'{self.threadID}: msg {incoming_msg} taken out of q')
            if mtype=="_terminate":
                print(f'Exiting {self.threadID}; parent: {self.parent} children: {self.children}')
                break
            
            #print(f'- Process {self.threadID} | Round {incoming_msg}')
            # take care of recieved msgs
            '''
            # send msgs
            if self.mark: 
                print(f'---> {self.threadID} marked')
                msg = self.neighbor_ids
                broadcast(q_sub, msg) # N IS NOT KNOWN, MAKE INDIVIDUAL QUEUES FOR EACH COMM CHANNEL   
            
                    if not n.mark:
                        print('Round {incoming_msg}: {n.threadID} is not marked and found by {self.threadID}')
                        n.parent = self
                  n.mark = True
                  self.children.append(n)
                  print('-- {self.threadID} marked {n.threadID} as child')
            print(f'Exiting {self.threadID}; parent: {self.parent} children: {self.children}')
            '''

#message format: {sender}|{receipient}|{dir}
def broadcast(q,n, msg):
    print(f'broadcasting {msg}')
    for i in range(1,n+1):
        msg_complete = f'master|{i}|b'
        q.put(msg_complete)

#peek function in queue
def queue_peek(q):
    obj = q.get()
    tmp_q = Queue()
    tmp_q.put(obj)
    while not q.empty():
        tmp_obj = q.get()
        tmp_q.put(tmp_obj)
    return tmp_q, obj

def launch_master_thread(n, ids, root, conn_matrix):
    global id_process, id_label, _terminate
    print(f'In master thread. Launching {n} threads..')
    q = Queue() # master comm channel
    i=0
    for p_id, conn in zip(ids, conn_matrix):
        id_label[i] = p_id
        i += 1
        process = process_thread(p_id, root, conn, q)
        id_process[p_id] = process
    print(id_label)
    # start all processes
    for v in id_process.values():
            v.start()
    '''
    # for each round
    for i in range(3):
            print(f'***** Round {i} ********')
            broadcast(q,n,f'Round-{i}')
    broadcast(q,n,"_terminate")

    parents_found = False
    round=0
    while not parents_found:
        print(f'***** Round {round} ********')
        # start threads
        for v in id_process.values():
            v.start()
        for v in id_process.values():
            v.join()
        temp_parents = [v.parent for v in id_process.values()]
        if None not in temp_parents:
            parents_found = True
        round += 1
    '''
    for v in id_process.values():
        v.join()
    print('exiting master thread. bye!')

if __name__=="__main__":
    assert(len(sys.argv) == 3)
    n = int(sys.argv[1])
    root = sys.argv[2]
    with open("input.dat","r") as dat_file:
        data = dat_file.readlines()
    ids = data[0].strip().split(",")
    for i in range(len(ids)): ids[i] = int(ids[i])
    matrix_rows = data[1].strip().split(",")
    connectivity_matrix = []
    for row in matrix_rows:
        connectivity_matrix.append(row.split())
    for row in range(len(connectivity_matrix)):
        for j in range(len(connectivity_matrix)):
            connectivity_matrix[row][j] = int(connectivity_matrix[row][j])
    id_process = {}
    id_label = {} 
    master_thread = threading.Thread(name='master',target=launch_master_thread, args=(n, ids, root, connectivity_matrix))
    master_thread.start()    



