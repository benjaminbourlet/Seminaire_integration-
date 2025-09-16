import network
import usocket
import time
import json
from machine import Pin

def httpgetremaster(host, path):
    addr = usocket.getaddrinfo(host, 80)[0][-1]
    s = usocket.socket()
    s.connect(addr)
    s.send("GET {} HTTP/1.0\r\nHost: {}\r\n\r\n".format(path, host).encode())
    response = b""
    while True:
        data = s.recv(100)
        if not data:
            break
        response += data
    s.close()
    return response

def getweather():
    host = "api.openweathermap.org"
    path = "/data/2.5/weather?lat=53.5586627&lon=9.6070582&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6"
    raw = httpgetremaster(host, path).decode()
    data = json.loads(raw[raw.find("\r\n\r\n") + 4:])
    print(data['weather'][0]['main'])
    if data['weather'][0]['id'] < 800:
      return False
    return True

p2 = Pin(2, Pin.OUT)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('POCO X7 Pro Benjamin', 'benjamin1234')
if sta_if.isconnected():
  print("Connexion WiFi OK")
  while True:
      if (getweather()):
          p2.on()
          time.sleep(15)
      else:
          for i in range(15):
              p2.on()
              time.sleep_ms(500)
              p2.off()
              time.sleep_ms(500)