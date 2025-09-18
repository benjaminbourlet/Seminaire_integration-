import network
import urequests
import time
from machine import Pin, PWM 

# --- CONFIG Wi-Fi ---
SSID = 'Jean Galaxy S21 5G'
PASSWORD = '12345678'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)

while not sta_if.isconnected():
    print("Connexion au Wi-Fi en cours...")
    time.sleep(1)

print("Connecté au Wi-Fi:", sta_if.ifconfig())

# --- CONFIG Servo ---
servo_pin = Pin(26)  # GPIO 26
servo = PWM(servo_pin, freq=50)  # Servo à 50Hz

def set_servo_angle(angle):
    # Conversion angle 0-180° → duty cycle pour servo
    duty = int((angle / 180 * 102) + 26)
    servo.duty(duty)
    print("Servo angle réglé à:", angle)

# --- API OpenWeatherMap ---
API_KEY = "9f3a00dc848b4363baeee053ddfc8ff7"
VILLE = "Angers"  # Mets ici la ville de ton choix

def get_wind_direction():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={VILLE}&appid={API_KEY}"
    try:
        response = urequests.get(url)
        data = response.json()
        response.close()
        wind_deg = data['wind']['deg']  # 0-360°
        return wind_deg
    except:
        print("Erreur récupération météo")
        return None

# --- BOUCLE PRINCIPALE ---
while True:
    wind_deg = get_wind_direction()
    if wind_deg is not None:
        # Convertir 0-360° en 0-180° pour le servo
        servo_angle = max(0, min(180, int((wind_deg / 360) * 180)))
        print("Direction vent:", wind_deg, "→ angle servo:", servo_angle)
        set_servo_angle(servo_angle)
    time.sleep(60)  # mise à jour toutes les 60s
