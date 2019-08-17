# coding = utf-8
import logging

__format = '%(asctime)s - %(levelname)s - %(filename)s[%(funcName)s:%(lineno)d] - %(message)s'
logging.basicConfig(level=logging.INFO, format=__format)

log = logging.getLogger(__name__)
