# coding = utf-8
# 中间代理
import zmq

front_port = 5559
back_port = 5560

# Prepare our context and sockets
context = zmq.Context()

frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:%d" % front_port)
backend.bind("tcp://*:%d" % back_port)

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    # frontend 收到了提问后，由backend发送给REP端
    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv_multipart()
        backend.send_multipart(message)

    # backend 收到了回答后，由frontend发送给REQ端
    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        frontend.send_multipart(message)
