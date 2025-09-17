from machine import Pin
import neopixel
import time

# 1 vert -> force 0
# 2 vert -> force 1-2
# 1 orange -> force 3-4
# 2 orange -> force 5-6
# 1 rouge -> force 7-8
# 2 rouge -> force 9-10
# 2 rouge clignote -> force 11-12


PIN_DATA = 18   # change si tu as mis un autre GPIO
nb_leds = 2         # une LED au début
led = neopixel.NeoPixel(Pin(PIN_DATA, Pin.OUT), nb_leds)

wind_speed = 20

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
        
    
#remplacer i par la data envoyer par l'API et utiliser led_wind(wind_conversion(i)) pour utiliser les leds
#montage electrique => DIN sur pin 18 avec resistance 470 ohm, 5v sur 5v, GND sur GND 
    
print("Test Indicateur Force du Vent")
while True: 
    for i in range (31):
        led_wind(wind_conversion(i))
        print("Le vent est de force", wind_conversion(i))
        print("le vent va a ", i , "m/s")
        i += 1
        time.sleep(3)
        set_led(0,'')
    
