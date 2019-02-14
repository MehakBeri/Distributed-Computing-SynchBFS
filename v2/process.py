import threading
import time

threadLock = threading.Lock()


class Process(threading.Thread):
    def __init__(self, id, name, root_id, conn):
        threading.Thread.__init__(self)
        self.processID = id
        self.name = name
        self.conn = conn
        self.root_id = root_id
        if self.processID == root_id:
            self.marked = True
        else:
            self.marked = False

    def add_neighbor(self, neighbor):
        self.conn.append(neighbor)
        print("{} -- Neighbor: {}".format(self.name, neighbor.name))

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        print_time(self.name, 1)
        if len(self.conn) > 0:
            for i in range(1, len(self.conn) + 1):
                print("{} -- Message sent to {}".format(self.name, self.conn[i-1].name))
                self.send_message(self.conn[i-1])
            # Free lock to release next thread
        threadLock.release()


    def mark(self):
        self.marked = True


    def set_parent(self, parent):
        self.parent = parent


    def send_message(self, receiver):
        receiver.receive_message(self)


    def receive_message(self, sender):
        if self.marked != True:
            self.mark()
            self.set_parent(sender)
            print("{} -- Parent set to {}".format(self.name, self.parent.name))


def print_time(threadName, counter):
    while counter:
        time.sleep(2)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
