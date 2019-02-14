from process import Process
from queue import Queue
import numpy as np
import threading

pcount = 6
conn_mat = None
root = None

filepath = 'input.dat'


def broadcast(q, msg):
    q.put(msg)


def launch_master_thread(n, ids, root, conn_matrix):
    global id_process, id_label, _terminate
    print(f'In master thread. Launching {n} threads..')
    q = Queue()  # master comm channel
    for p_id, conn in zip(ids, conn_matrix):
        neighbor_ids = []
        for i in range(len(conn)):
            if conn[i] == 1 and id_label[i] != int(p_id):
                neighbor_ids.append(id_label[i])
        process = Process(int(p_id), root, neighbor_ids, q, None)
        id_process[p_id] = process
    for v in id_process.values():
        v.start()
    # for each round
    # for k in range(3):
    #    print(f'***** Round {i} ********')
    # broadcast(q, _terminate)

    for v in id_process.values():
        v.join()
    print('exiting master thread. bye!')


if __name__ == "__main__":
    with open(filepath) as fp:
        pcount = int(fp.readline())
        p_ids = list(fp.readline().split(" "))
        root = int(fp.readline())
        line = fp.readline()
        conn_mat = np.zeros(shape=(pcount, pcount), dtype=int)
        for i in range(1, pcount + 1):
            newrow = line.split()
            conn_mat[i - 1] = newrow
            line = fp.readline()
    for row in range(len(conn_mat)):
        for col in range(len(conn_mat)):
            conn_mat[row][col] = int(conn_mat[row][col])
    id_process = {}
    id_label = {}
    cnt = 0
    for p_id in p_ids:
        id_label[cnt] = int(p_id)
        cnt += 1
    _terminate = object()
    master_thread = threading.Thread(name='master', target=launch_master_thread,
                                     args=(pcount, p_ids, root, conn_mat))
    master_thread.start()
