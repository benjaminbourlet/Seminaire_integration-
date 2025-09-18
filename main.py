import network
import urequests
from time import sleep
import time
import neopixel
from machine import Pin, PWM, SoftI2C
from machine_i2c_lcd import I2cLcd

#spécification du bandeau led
PIN_DATA = 18
nb_leds = 2
led = neopixel.NeoPixel(Pin(PIN_DATA, Pin.OUT), nb_leds)

#spécification ecran lcd
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

#initialisation de l'ecran sur Pin 21(SDA) et 22(SCL)
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#/////////////////////////////////////// BLOC connexion ////////////////////////////////////////#
def connexion():
    if setupWifiCon():
        connexionled.on()
        # playsoundonconnection(speakerPWM, 5000, 0.25)
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Connexion ok")
        print("connexion ok")
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Connexion perdu")
        print("connexion perdu")
        while setupWifiCon() == False:
            connexionled.on()
            sleep(1)
            connexionled.off()
            sleep(1)
        
            
            
        
        
        


def getweather():
    ville = "hambourg"
    res = {}
    rawdataget = urequests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + ville + "&appid=c1c60bb1bc8fbdcb97ee83119e4cc2c6&units=metric",
        timeout=5)
    data = rawdataget.json()

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
    try:
        wifiCon = network.WLAN(network.STA_IF)
        wifiCon.active(True)
        wifiCon.scan()
        #tel de benjamin
        #wifiCon.connect('POCO X7 Pro Benjamin', 'benjamin1234')
        #tel de benji
        wifiCon.connect('Iphone de benji', 'a1z2e3r4t5')
        return True
    except OSError as e:
        print("Erreur de connexion wifi : " + str(e))
        return False
    
#////////////////////////////////////BLOC indicateur led/////////////////////////////////////#    

def indicator_led(id_weather):
    redled.off()
    greenled.off()
    if (id_weather) >= 800:
        greenled.on()
        redled.off()
    else:
        greenled.off()
        redled.on()
    

#///////////////////////////////////////BLOC ECRAN LCD///////////////////////////////////////#

def display_information(meteo, temperature, humidity):
    # Ligne d'en-tête
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("EN CE MOMENT :")

    # Afficher météo → attendre
    lcd.move_to(0, 1)
    lcd.putstr("il fait " + str(meteo))
    sleep(3)

    # Effacer juste la 2e ligne puis afficher température
    lcd.move_to(0, 1)
    lcd.putstr(" " * 16)  # efface la ligne
    lcd.move_to(0, 1)
    lcd.putstr("TEMP : " + str(temperature) + chr(223) + "C")
    sleep(3)

    # Effacer juste la 2e ligne puis afficher humidité
    lcd.move_to(0, 1)
    lcd.putstr(" " * 16)
    lcd.move_to(0, 1)
    lcd.putstr("HUMIDITE " + str(humidity) + "%")
    sleep(3)

#//////////////////////////////////////BLOC BANDEAU LED//////////////////////////////////////#

# 1 vert -> force 0
# 2 vert -> force 1-2
# 1 orange -> force 3-4
# 2 orange -> force 5-6
# 1 rouge -> force 7-8
# 2 rouge -> force 9-10
# 2 rouge clignote -> force 11-12

# allumage des leds
def set_led(status, color):
    if status == 0:
        led[0] = (0, 0, 0);
        led.write()
        led[1] = (0, 0, 0);
        led.write()
    elif status == 1:
        if color == 'green':
            led[0] = (0, 255, 0);
            led.write()
        elif color == 'red':
            led[0] = (255, 0, 0);
            led.write()
        elif color == 'orange':
            led[0] = (255, 150, 0);
            led.write()
    elif status == 3:
        if color == 'green':
            led[0] = (0, 255, 0);
            led.write()
            led[1] = (0, 255, 0);
            led.write()
        elif color == 'red':
            led[0] = (255, 0, 0);
            led.write()
            led[1] = (255, 0, 0);
            led.write()
        elif color == 'orange':
            led[0] = (255, 150, 0);
            led.write()
            led[1] = (255, 150, 0);
            led.write()
        else:
            status = 0


# logique d'allumage des leds
def setledwind(strength_wind):
    if strength_wind == 0:
        # 1 vert
        set_led(0, '')
    elif 1 <= strength_wind <= 2:
        # 2 verts
        set_led(3, 'green')
    elif 3 <= strength_wind <= 4:
        # 1 orange
        set_led(1, 'orange')
    elif 5 <= strength_wind <= 6:
        # 2 orange
        set_led(3, 'orange')
    elif 7 <= strength_wind <= 8:
        # 1 rouge
        set_led(1, 'red')
    elif 9 <= strength_wind <= 10:
        # 2 rouge
        set_led(3, 'red')
    elif 11 <= strength_wind <= 12:
        for i in range(3):
            set_led(3, 'red')
            time.sleep(1)
            set_led(0, '')
            time.sleep(1)
            set_led(3, 'red')
            time.sleep(1)
            set_led(0, '')
            i += 1
        # 2 rouge clignotant
    else:
        set_led(0, '')


# Fonction de conversion de la vitesse du vent en coefficient de beaufort
def windconversion(windspeed):
    if windspeed == 0:
        return 0
    elif windspeed >= 32.7:
        return 12
    else:
        return int(0.836 * (windspeed ** (2 / 3)) + 0.5)


def playsoundonconnection(speaker, freq, dur):
    if freq > 0:
        speaker.freq(freq)
        speaker.duty(256)
        time.sleep(dur)
        speaker.duty(0)
        speaker.deinit()


# PROGRAMME PRINCIPAL

# Création et reset des LEDS rouge/vert et connexion
greenled = Pin(0, Pin.OUT)
redled = Pin(4, Pin.OUT)
connexionled = Pin(27, Pin.OUT)
speakerPin = Pin(25, Pin.OUT)
speakerPWM = PWM(speakerPin)

greenled.off()
redled.off()
connexionled.off()
speakerPWM.duty(0)

while setupWifiCon():
    connexion()
    currentweather = getweather()
    print(currentweather)
    setledwind(windconversion(currentweather["wind"]))
    indicator_led(currentweather["id_meteo"])
    display_information(currentweather["meteo"], currentweather["temperature"], currentweather["humidity"])
    print(windconversion(currentweather["wind"]))
    connexion()
    
            #time.sleep(15)
