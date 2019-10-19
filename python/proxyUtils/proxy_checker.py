from sqlite.sqlite import db_connector
from urllib.request import urlopen
from urllib import request
import requests

path = b'instagram.db'


class proxy_checker:
  def __init__(self, db_path):
    self.db = db_connector(db_path)
    self.alive = 0

  def is_alive(self, host, port):
    try:
      proxies = { host: port}
      response = requests.get("http://example.org", proxies=proxies)

      if response.status_code != 200:
        self.update_status(host, "failed")
        return False

      self.update_status(host, "success")
    except:
      self.update_status(host, "failed")
      return False
    return True

  def update_status(self, host, status):
    self.db.update("proxy_list", "status", "host", host, status)


  def check_unknown(self):
    proxies = self.db.select("host,port", "proxy_list", "status", "unknown")
    self.__check(proxies)

  def check_all(self):
    proxies = self.db.execute("SELECT host,port FROM proxy_list")
    self.__check(proxies)

  def __check(self, proxies):
    for proxy in proxies:
      res = self.is_alive(proxy[0], int(proxy[1]))
      if res == True:
          self.alive = self.alive +1
          print("Alive proxy {} from {}".format(self.alive, len(proxies)))


checker = proxy_checker(path)
checker.check_unknown()