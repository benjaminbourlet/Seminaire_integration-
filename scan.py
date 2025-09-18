import machine

sdaPIN=machine.Pin(21)  
sclPIN=machine.Pin(22)

i2c=machine.I2C(sda=sdaPIN, scl=sclPIN, freq=10000)   

devices = i2c.scan()
print
if len(devices) == 0:
 print("Pas d'écran !")
else:
 print('i2c manquant :',len(devices))
for device in devices:
 print("L'adressage est : ",hex(device))
