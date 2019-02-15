from queue import Queue
from message import Message
from process import Process
import threading
import time
import sys

#message format: {sender}|{receipient}|{dir}
def broadcast(q, r, id_process):
    for id in ids:
        msg= Message('Master',id,f'broadcast{r}')
        q.put(msg)

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
    global id_process, id_label
    print(f'In master thread. Launching {n} threads..')
    q = Queue() # master comm channel
    i=0
    for p_id in ids:
        id_label[i] = p_id
        i += 1
    for p_id, conn in zip(ids, conn_matrix):
        neighbor_ids = []
        for j in range(len(conn)):
            if (conn[j]==1 and id_label[j]!=int(p_id)):
                neighbor_ids.append(id_label[j])
        process = Process(int(p_id), root, neighbor_ids, q)
        id_process[p_id] = process  
    print(id_label)
    for v in id_process.values():
            v.start()
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



