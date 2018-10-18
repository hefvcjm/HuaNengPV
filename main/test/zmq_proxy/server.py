import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
# REP连接的是DEALER
socket.connect("tcp://localhost:5560")

while True:
    message = socket.recv()
    print("Received request: %s" % message.decode())
    socket.send(b"World")
