from ast import Try
from time import sleep
from client import BitforexRestApi
from logbook import Logger, RotatingFileHandler
import logbook
import os


path = "~/export/logs/bfapitest/"

class BitforexRestTestApi(BitforexRestApi):
  def __init__(self):
    super().__init__()
    self.logger = self.getLogger('bitforexapitest')



  def write_log(self, logmsg):
        self.logger.info(logmsg) 
  
  def getLogger(self, name):
    file = '/'.join([path, name+'.txt'])

    dir = os.path.dirname(file)
    if not os.path.exists(dir):
        os.makedirs(dir)

    logger = Logger(name)
    logbook.set_datetime_format('local')
    file_handler = RotatingFileHandler(file, max_size=33554432, backup_count=5, level = "DEBUG")
    logger.handlers.append(file_handler)
    return logger


bitforexapi = BitforexRestTestApi()
bitforexapi.connect("8dfb85d300a8c339208aca71a616d3ed", "ea31d40f04a149862394d295acb210d6", 3,"", "")

while(True): 
  try:
    bitforexapi.write_log(bitforexapi.query_all_open_orders_sync("coin-usdt-eth"))
    sleep(6)
  except BaseException as err:
    bitforexapi.write_log(f"Unexpected {err}")