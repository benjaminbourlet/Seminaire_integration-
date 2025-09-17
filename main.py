import network
import urequests
import time
from machine import Pin

def getweather():
    latitude = "50"
    longitude = "6"

    data = urequests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6&units=metric").json()
    print(data)
    return data['weather'][0]['id'] > 800

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
else:
    # activer LED connexion