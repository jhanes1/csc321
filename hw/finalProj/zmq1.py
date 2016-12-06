import zmq
import random
import sys
import time

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

# Socket with direct access to the sink: used to syncronize start of batch
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Process tasks forever
while True:
    try:
        s = receiver.recv(flags=zmq.NOBLOCK)

        # Simple progress indicator for the viewer
        sys.stdout.write((s+b'\n').decode('utf-8'))
        sys.stdout.flush()
    except zmq.Again:
        sender.send(str.encode(input('\nEnter to flush stack and send message: ')),flags=zmq.NOBLOCK)
