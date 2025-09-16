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
    #Hambourg
    latitude = "50"
    longitude = "6"
    
    #Bordeaux
    #latitude = "44.8650212"
    #longitude = "-0.5774944"

    host = "api.openweathermap.org"
    path = "/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6"
    raw = httpgetremaster(host, path).decode()
    data = json.loads(raw[raw.find("\r\n\r\n") + 4:])
    print(data['weather'][0]['main'])
    if data['weather'][0]['id'] < 800:
      return False
    return True

led_green = Pin(0, Pin.OUT)
led_red = Pin(4, Pin.OUT)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('POCO X7 Pro Benjamin', 'benjamin1234')

if sta_if.isconnected():
  print("Connexion WiFi OK")
  while True:
      led_red.off()
      led_green.off()
      if (getweather()):
          led_green.on()
          led_red.off()
          time.sleep(15)
      else:
          led_green.off()
          led_red.on()
          time.sleep(15)