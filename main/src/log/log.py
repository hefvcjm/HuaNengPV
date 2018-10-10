# coding=utf-8
# init and integrate logging
import logging


class Log:
    __log__ = None

    def __init__(self):
        if self.__log__ is None:
            LOG_FORMAT = "%(asctime)s-%(levelname)s-%(pathname)s-%(funcName)s:%(message)s"
            DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
            logging.basicConfig(level=logging.DEBUG, datefmt=DATE_FORMAT, format=LOG_FORMAT)
            self.__log__ = self

    def __getLog__(self):
        return self.__log__

    @staticmethod
    def debug(msg):
        Log()
        logging.debug(msg)

    @staticmethod
    def info(msg):
        Log()
        logging.info(msg)
