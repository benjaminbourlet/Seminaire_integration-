import network
import urequests
import time
from machine import Pin


def getweather():
    ville = "Bordeaux"
    res = {}
    data = urequests.get("https://api.openweathermap.org/data/2.5/weather?q=" + ville + "&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6&units=metric").json()

    if "message" in data and "cod" in data:
        print("Erreur de l'API : " + data["message"] + ", Code : " + data["cod"])
        return -1

    if "weather" not in data:
        print("Données météos manquantes" + data)
        return -1

    res["id_meteo"] = data["weather"][0]["id"]
    res["meteo"] = data["weather"][0]["main"]
    res["temperature"] = data["main"]["temp"]
    res["humidity"] = data["main"]["humidity"]
    res["wind"] = data["wind"]["speed"]
    res["wind_dir"] = data["wind"]["deg"]
    res["pcnuage"] = data["clouds"]["all"]
    res["pressure"] = data["main"]["pressure"]
    return res

def setupWifiCon():
    wifiCon = network.WLAN(network.STA_IF)
    wifiCon.active(True)
    wifiCon.scan()
    try:
        wifiCon.connect('POCO X7 Pro Benjamin', 'benjamin1234')
        return True
    except:
        print("Connexion Wifi NOK")
        while True: # Sinon on toggle
            connexionled.toggle()

# Création et reset des LEDS rouge/vert et connexion
greenled = Pin(0, Pin.OUT)
redled = Pin(4, Pin.OUT)
connexionled = Pin(27, Pin.OUT)

greenled.off()
redled.off()
connexionled.off()

if setupWifiCon():
    connexionled.on()
    print("Connexion Wifi OK")
    if getweather() == -1:
        while True:
            redled.on()
            time.sleep(1)
            redled.off()
    else: # Boucle principale autonome de l'appareil
        while True:
            redled.off()
            greenled.off()
            if (getweather()["id_meteo"]) >= 800:
                greenled.on()
                redled.off()
                time.sleep(15)
            else:
                greenled.off()
                redled.on()
                time.sleep(15)