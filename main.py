import network
import urequests
import time
from machine import Pin

def getweather():
    ville = "Bordeaux"

    res = {}
    data = urequests.get("https://api.openweathermap.org/data/2.5/weather?q=" + ville + "&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6&units=metric").json()
    if len(data) == 0:
        return None

    res["id_meteo"] = data["weather"][0]["id"]
    res["meteo"] = data["weather"][0]["main"]
    res["temperature"] = data["main"]["temp"]
    res["humidity"] = data["main"]["humidity"]
    res["wind"] = data["wind"]["speed"]*3.6 #km/h
    res["wind_dir"] = data["wind"]["deg"]
    res["pcnuage"] = data["clouds"]["all"]
    res["pressure"] = data["main"]["pressure"]
    return res

led_green = Pin(0, Pin.OUT)
led_red = Pin(4, Pin.OUT)

wifiCon = network.WLAN(network.STA_IF)
wifiCon.active(True)
wifiCon.scan()
wifiCon.connect('POCO X7 Pro Benjamin', 'benjamin1234')

if wifiCon.isconnected():
  # allumer LED de connexion
  print("Connexion Wifi OK")
  currentweather = getweather()
  while True:
      print(currentweather)
      #if currentweather == None: signaler erreur
      led_red.off()
      led_green.off()
      if (currentweather["id_meteo"]) >= 800:
          print("meteo OK")
          led_green.on()
          led_red.off()
          time.sleep(15)
      else:
          print("meteo NOK")
          led_green.off()
          led_red.on()
          time.sleep(15)
else:
    print("Connexion Wifi NOK")
    wifiCon.disconnect()
    # + signaler erreur de connexion