from process import Process
import numpy as np

threads = []

pcount = 6
conn_mat = None
root = None

filepath = 'input.dat'
with open(filepath) as fp:
   pcount = int(fp.readline())
   p_ids = list(fp.readline().split(" "))
   root = fp.readline()
   line = fp.readline()
   conn_mat = np.zeros(shape=(pcount, pcount), dtype=int)
   for i in range(1, pcount + 1):
       newrow = line.split()
       conn_mat[i-1] = newrow
       line = fp.readline()

print(conn_mat)

for c in range(1, pcount + 1):
    # Create new threads
    thread = Process(c, "Thread-" + str(c), root, [])

    # Add threads to thread list
    threads.append(thread)


# add neighbors
for i in range(1, pcount + 1):
    for j in range(1, pcount + 1):
        if conn_mat[i-1][j-1] == 1:
            threads[i-1].add_neighbor(threads[j-1])


for thread in threads:
    # Start new Threads
    thread.start()

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")