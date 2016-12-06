import sys
import time
import zmq

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    try:
        s = receiver.recv(flags=zmq.NOBLOCK)

        # Simple progress indicator for the viewer
        sys.stdout.write((s+b'\n').decode('utf-8'))
        sys.stdout.flush()
    except zmq.Again:
        sender.send(str.encode(input('\nEnter to flush stack and send message:: ')),flags=zmq.NOBLOCK)
