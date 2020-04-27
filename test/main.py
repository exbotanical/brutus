import sys
import os
import subprocess
from subprocess import PIPE, STDOUT
from subprocess import Popen

project_root = os.path.dirname(os.path.realpath(__file__))
print(project_root)
# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.system(f"""osascript -e 'tell app "Terminal"
#              do script "python3 {dir_path}/test.py"
#              end tell' """)
# subprocess.Popen(['python', 'test.py'], stdin=subprocess)
# proc = subprocess.Popen(['gnome-terminal','--', 'python test.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out, err = proc.communicate()
# subprocess.call(['open', '-a', 'Terminal.app', '/usr/bin/python3 ; test.py'])


# def subprocess_cmd(dr,cmd1,cmd2):
#     p1 = Popen(cmd1.split(),stdout=PIPE,cwd=dr)
#     p2 = Popen(cmd2.split(),stdin=p1.stdout,stdout=PIPE,cwd=dr)
#     p1.stdout.close()
#     return p2.communicate()[0]
# os.system(f"screen python3 -m test.test")



# os.system("open -a Terminal test.py")
# os.system("gnome-terminal -e 'bash -c \"python3 test.py; exec bash\"'")
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