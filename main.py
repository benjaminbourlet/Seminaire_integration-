import network
import urequests
import time
import neopixel
from machine import Pin

PIN_DATA = 18 
nb_leds = 2         
led = neopixel.NeoPixel(Pin(PIN_DATA, Pin.OUT), nb_leds)


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
        wifiCon.connect('Iphone de benji', 'a1z2e3r4t5')
        return True
    except:
        print("Connexion Wifi NOK")
        while True: # Sinon on toggle
            connexionled.toggle()

#////////////////////////////////////////////////////////////////////////#
            #//indicateur leds force du vent//#
            
#allumage des leds 
def set_led(status,color):
    
    if status == 0:
        led[0] = (0,0,0); led.write()
        led[1] = (0,0,0); led.write()
    elif status == 1:
        if color == 'green':
            led[0] = (0, 255, 0); led.write();
        elif color == 'red':
            led[0] = (255, 0, 0); led.write();
        elif color == 'orange':
            led[0] = (255, 150, 0); led.write();
        else:
            status = 0
    elif status == 3:
        if color == 'green':
            led[0] = (0, 255, 0); led.write();
            led[1] = (0, 255, 0); led.write();
        elif color == 'red':
            led[0] = (255, 0, 0); led.write();
            led[1] = (255, 0, 0); led.write();
        elif color == 'orange':
            led[0] = (255, 150, 0); led.write();
            led[1] = (255, 150, 0); led.write();
        else:
            status = 0
            
#logique d'allumage des leds 
def led_wind(strength_wind):
    
    if strength_wind == 0:
        # 1 vert
        set_led(1,'green')
    elif 1 <= strength_wind <= 2:
        # 2 verts
        set_led(3,'green')
    elif 3 <= strength_wind <= 4:
        # 1 orange
        set_led(1,'orange')
    elif 5 <= strength_wind <= 6:
        # 2 orange
        set_led(3,'orange')
    elif 7 <= strength_wind <= 8:
        # 1 rouge
        set_led(1,'red')
    elif 9 <= strength_wind <= 10:
        # 2 rouge
        set_led(3,'red')
    elif 11 <= strength_wind <= 12:
        for i in range (3):
            set_led(3,'red')
            time.sleep(1)
            set_led(0,'')
            time.sleep(1)
            set_led(3,'red')
            time.sleep(1)
            set_led(0,'')
            i += 1
        #2 rouge clignotent 
    else:
        set_led(0,'')
        
#conversion m/s en force que l'echelle de beaufort 
def wind_conversion(wind_speed):
    strength_wind = None
    
    if wind_speed <= 0.2:
        strength_wind = 0
    elif 0.2 < wind_speed <= 1.5:
        strength_wind = 1
    elif 1.5 < wind_speed <= 3.3:
        strength_wind = 2
    elif 3.3 < wind_speed <= 5.4:
        strength_wind = 3
    elif 5.4 < wind_speed <= 7.9:
        strength_wind = 4
    elif 7.9 < wind_speed <= 10.7:
        strength_wind = 5
    elif 10.7 < wind_speed <= 13.8:
        strength_wind = 6
    elif 13.8 < wind_speed <= 17.1:
        strength_wind = 7
    elif 17.1 < wind_speed <= 20.7:
        strength_wind = 8
    elif 20.7 < wind_speed <= 24.4:
        strength_wind = 9
    elif 24.4 < wind_speed <= 28.4:
        strength_wind = 10
    elif 28.4 < wind_speed <= 32.6:
        strength_wind = 11
    else:  # >= 32.7
        strength_wind = 12

    return strength_wind


            #//fin indicateur leds force du vent//#
#////////////////////////////////////////////////////////////////////////#





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
            
            #bloc indicateur force du vent
            led_wind(wind_conversion(getweather()["wind"]))
            print(wind_conversion(getweather()["wind"]))
            
            
            if (getweather()["id_meteo"]) >= 800:
                greenled.on()
                redled.off()
            else:
                greenled.off()
                redled.on()
            time.sleep(15)
            set_led(0,'')