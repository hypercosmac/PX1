import firebase_admin
from firebase_admin import credentials, messaging
import RPi.GPIO as GPIO
import time
import requests

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
SENSOR_PIN = 17  # Change this to the GPIO pin you're using
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Firebase Cloud Messaging server key
FCM_SERVER_KEY = "YOUR_FCM_SERVER_KEY"

def send_fcm_notification(title, body):
    # This function sends a notification using Firebase Cloud Messaging
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={FCM_SERVER_KEY}"
    }
    
    payload = {
        "to": "/topics/all_devices",  # You can also use "to": "DEVICE_TOKEN" for a specific device
        "notification": {
            "title": title,
            "body": body
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")
        print(f"Response: {response.text}")

try:
    while True:
        if GPIO.input(SENSOR_PIN):
            send_fcm_notification("Alert!", "Motion detected!")
            time.sleep(30)  # Wait for 30 seconds before sending another notification
        time.sleep(0.1)  # Small delay to prevent CPU overload

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleaned up. Exiting...")

