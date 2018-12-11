# coding=utf-8
# 主函数
from main.src.communication.client import *


def main():
    """main function"""
    client = Client('tcp://localhost:3000')
    client.start()
    client.join()


if __name__ == "__main__":
    main()
