from queue import Queue
from message import Message
from process import Process
import threading
import time
import sys
import json

def launch_master_thread(n, ids, root, conn_matrix):
    global id_process, id_label
    print(f'In master thread. Launching {n} threads..')
    initial_config = {}
    q = Queue() # initially empty queue
    for pid in ids:
        initial_config[int(pid)] = {'parent': None,
                                    'children':[],
                                    'marked':False,
                                    'sent':[],
                                    'r':0,
                                    'q':q
                                    }
    threadLock = threading.Lock()
    r=1
    while True:
        print(f'********** master broadcast {r} ***********')
        if r==1:
            config = initial_config
            latest_q = q
            print(f'|| BFS LEVEL: {root}')
        r = r+1
        print(list(latest_q.queue))
        id_process = launch_threads(ids, conn_matrix, root, latest_q, config)
        done_threads = []
        config={}
        while True: #wait for all threads to complete one round after the first broadcast
            #time.sleep(2)
            if len(done_threads) == len(id_process):
                #print(f'done status: {done_threads}')
                break
            tmp=None
            #print(f'master acq {list(q.queue)}')
            threadLock.acquire()
            if q.qsize()!=0:
                tmp = q.get()
            threadLock.release()
            #print(f'master rel')
            if tmp==None:
                continue
            if tmp.receiverID == 'Master':
                config[tmp.senderID] = tmp.msg_type 
                latest_q = tmp.msg_type['q']
                done_threads.append(tmp.senderID)
                #print(f'-----------------> Master recieved done from {tmp.senderID}')
            else:
                threadLock.acquire()
                q.put(tmp)
                threadLock.release()
        for v in id_process.values():
            v.join()
        # check termination
        visited = []
        for key in config.keys():
            if config[key]['marked']==True:
                visited.append(key)
        if len(visited)==n and latest_q.qsize()==0:
            break
    print('**********************************************')
    for c in config:
        print(f'{c} : Parent: {config[c]["parent"]} Children: {config[c]["children"]} Marked: {config[c]["marked"]}')
    print('exiting master thread. bye!')

def launch_threads(ids, conn_matrix, root, q, config):
    i=0
    for p_id in ids:
        id_label[i] = p_id
        i += 1
    for p_id, conn in zip(ids, conn_matrix):
        neighbor_ids = []
        for j in range(len(conn)):
            if (conn[j]==1 and id_label[j]!=int(p_id)):
                neighbor_ids.append(id_label[j])
        process = Process(int(p_id), root, neighbor_ids, q, config)
        id_process[p_id] = process  
    #print(id_label)
    for v in id_process.values():
            v.start()
    return id_process

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



