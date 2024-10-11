import time
from picamera2 import Picamera2
from libcamera import controls
import numpy as np
from tflite_runtime.interpreter import Interpreter
from PIL import Image
import subprocess

# Load the TFLite model
interpreter = Interpreter(model_path="food_classification_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define class labels
class_labels = ['food_present', 'no_food']

# Initialize camera
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (224, 224)})
picam2.configure(preview_config)
picam2.start()

# Enable auto focus
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Initialize variables
food_detected_time = None
notification_sent = False

def detect_food():
    # Capture image
    frame = picam2.capture_array()
    
    # Preprocess the image
    image = Image.fromarray(frame)
    input_data = np.expand_dims(image, axis=0).astype(np.float32) / 255.0
    
    # Set the tensor to point to the input data to be inferred
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Run the inference
    interpreter.invoke()
    
    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Get the predicted class
    predicted_class = class_labels[np.argmax(output_data)]
    
    return predicted_class

def send_notification():
    subprocess.run(["notify-send", "Food Left Out", "Please put the food back in the fridge."])

while True:
    food_status = detect_food()
    
    if food_status == 'food_present':
        if food_detected_time is None:
            food_detected_time = time.time()
        elif time.time() - food_detected_time > 3600 and not notification_sent:  # 1 hour = 3600 seconds
            send_notification()
            notification_sent = True
    else:
        food_detected_time = None
        notification_sent = False
    
    time.sleep(10)  # Check every 10 seconds

picam2.stop()

