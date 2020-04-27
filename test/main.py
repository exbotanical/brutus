import sys
import os
import subprocess
from subprocess import PIPE, STDOUT
from subprocess import Popen

# subprocess.Popen(['python', 'test.py'], stdin=subprocess)
# proc = subprocess.Popen(['gnome-terminal','--', 'python test.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out, err = proc.communicate()


os.system("gnome-terminal -e 'bash -c \"python3 test.py; exec bash\"'")
# os.system("gnome-terminal -e 'bash -c \"python test.py; exec bash\"'")
# import threading
# from queue import Queue
# import time

# def worker(q):
#     """thread worker function"""
#     running = True
#     while running:
#         message = q.get()
#         print('Worker received message: {}'.format(message))
#         if message == 'KILL':
#             running = False
#     print('Worker completed')

# if __name__ == '__main__':
#     q = Queue()
#     worker = threading.Thread(target=worker, args=(q,))
#     worker.start()
#     running = True
#     while running:
#         user_input = input('Input some data: ')
#         q.put(user_input)
#         if user_input == 'KILL':
#             running = False
#         time.sleep(0.5)
#     print('Program terminated')