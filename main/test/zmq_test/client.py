import zmq

context = zmq.Context()

#  Socket to talk to server  
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response  
for request in range(1, 10):
    print("Sending request ", request, "...")

    socket.send("Hello".encode())

    #  Get the reply.  
    message = socket.recv().decode()
    print("Received reply ", request, "[", message, "]")
