# coding = utf-8
import zmq
import json
import uuid


class CLITester:

    def __init__(self, port, role="server"):
        context = zmq.Context()
        self.__socket = context.socket(zmq.PAIR)
        if role.lower() == "server":
            self.__socket.bind("tcp://*:%s" % port)
        elif role.lower() == "client":
            self.__socket.connect("tcp://localhost:%s" % port)
        else:
            print(f"no such role: {role}")

    def send(self, data):
        self.__socket.send_json(data)
        print(json.dumps(self.__socket.recv_json(), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    tester = CLITester(5571, "client")
    # main_transformer_generation_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "main_transformer_generation_in_period",
            "args": [
                ["2017-10-11 11:50:00", "2017-10-11 11:55:00", "2017-10-11 12:00:00", "2017-10-11 12:05:00"],
                [1, 2, 3, 4],
                [1, 2, 3, 4]
            ]}
    tester.send(data)
    # gather_power_wire_generation_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "gather_power_wire_generation_in_period",
            "args": [
                ["2017-10-11 11:50:00", "2017-10-11 11:55:00", "2017-10-11 12:00:00", "2017-10-11 12:05:00"],
                [1, 2, 3, 4]
            ]}
    tester.send(data)
    # inverter_generation_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "inverter_generation_in_period",
            "args": [
                ["2019-08-26 12:47:30", "2019-08-26 12:48:30", "2019-08-26 12:49:30", "2019-08-26 12:50:30"],
                [59.3, 58.8, 58.0, 58.0]
            ]}
    tester.send(data)
    # box_generation_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "box_generation_in_period",
            "args": [
                ["2019-08-26 12:47:30", "2019-08-26 12:48:30", "2019-08-26 12:49:30", "2019-08-26 12:50:30"],
                [59.3, 58.8, 58.0, 58.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
                [5.3, 2.3, 8.0, 5.0],
            ]}
    tester.send(data)
    # series_generation_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "series_generation_in_period",
            "args": [
                ["2019-08-26 12:47:30", "2019-08-26 12:48:30", "2019-08-26 12:49:30", "2019-08-26 12:50:30"],
                [59.3, 58.8, 58.0, 58.0],
                [5.3, 2.3, 8.0, 5.0],
            ]}
    tester.send(data)
    # year_plan_completion_rate
    data = {"token": str(uuid.uuid4()),
            "function": "year_plan_completion_rate",
            "args": [
                90, 100
            ]}
    tester.send(data)
    # device_theoretical_generation
    data = {"token": str(uuid.uuid4()),
            "function": "device_theoretical_generation",
            "args": [
                ["2019-08-26 12:47:30", "2019-08-26 12:48:30", "2019-08-26 12:49:30", "2019-08-26 12:50:30"],
                [59.3, 58.8, 58.0, 58.0],
                1000000
            ]}
    tester.send(data)
    # device_pr_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "device_pr_in_period",
            "args": [
                2000,
                2924
            ]}
    tester.send(data)
    # square_loss_in_period
    data = {"token": str(uuid.uuid4()),
            "function": "square_loss_in_period",
            "args": [
                6000,
                [2924, 2509]
            ]}
    tester.send(data)
    # aging_rate
    data = {"token": str(uuid.uuid4()),
            "function": "aging_rate",
            "args": [
                6000,
                [2924, 2509]
            ]}
    tester.send(data)
