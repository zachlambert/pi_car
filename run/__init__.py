
from multiprocessing import Queue

control_queue = Queue()
message_queue = Queue()
display_queue = Queue(maxsize=2)