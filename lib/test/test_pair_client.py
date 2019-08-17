# coding = utf-8
import zmq
import time

port = "5571"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

# while True:
# time.sleep(2)
socket.send_json({"token": "1234567890", "function": "station_total_generation", "args": [10, 10]})
socket.send_json({"token": "1234567890", "function": "station_total_generation", "args": [10, 10]})
# socket.send_json({"token": "1234567890", "function": "station_total_generation", "args": [10, 10]})
msg = socket.recv_json()
print(msg)
msg = socket.recv_json()
print(msg)
socket.send_json({"token": "1234567890", "function": "station_total_generation", "args": [10, 10]})
msg = socket.recv_json()
print(msg)
