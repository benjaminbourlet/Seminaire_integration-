import time
from machine import Pin;


print("Mec bien");

led1 = Pin(4, Pin.OUT);
led2 = Pin(0, Pin.OUT)


while True :
    led1.on()
    time.sleep_ms(2000)
    led2.on()
    led1.off()
    time.sleep_ms(5000)
    led1.on()
    led2.off()
    time.sleep_ms(5000)
    led1.off()
    time.sleep_ms(5000)
    


