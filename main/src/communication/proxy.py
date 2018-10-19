# coding = utf-8
# 中间代理
import zmq

front_port = 5559
back_port = 5560


def main():
    context = zmq.Context(1)
    # Socket facing clients
    frontend = context.socket(zmq.XREP)
    frontend.bind("tcp://*:%d" % front_port)
    # Socket facing services
    backend = context.socket(zmq.XREQ)
    backend.bind("tcp://*:%d" % back_port)
    try:
        zmq.device(zmq.QUEUE, frontend, backend)
    except Exception:
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()
