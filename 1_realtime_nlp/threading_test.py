import threading
from parser_function import parser
from queue import Queue


output_q = Queue()
parser_thread = threading.Thread(
	target=parser,
	args=[output_q],
	name='parser'
)
parser_thread.start()

while True:
	new_id = input()
	output_q.put(new_id)
