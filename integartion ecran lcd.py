from machine import Pin, SoftI2C
from machine_i2c_lcd import I2cLcd
from time import sleep

# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#demo
meteo = "soleil"
temperature = 33
humidity = 10

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
    lcd.putstr("TEMPERATURE " + str(temperature) + chr(223) + "C")
    sleep(3)

    # Effacer juste la 2e ligne puis afficher humidité
    lcd.move_to(0, 1)
    lcd.putstr(" " * 16)
    lcd.move_to(0, 1)
    lcd.putstr("HUMIDITE " + str(humidity) + "%")
    sleep(3)
        
        
display_information(meteo, temperature, humidity)

    
    