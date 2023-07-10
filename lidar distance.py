import time
import board
import busio
import adafruit_vl53l0x
import pyttsx3

# Initialize the I2C bus.
i2c = busio.I2C(board.D23, board.D13)

# Create a VL53L0X object.
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Initialize the text-to-speech engine.
engine = pyttsx3.init()

def convert_to_cm(mm):
    # Convert millimeters to inches.
    return mm / 10

def say_distance(distance):
    # Convert distance to inches.
    inches = convert_to_cm(distance)
    # Convert inches to a string with two decimal places.
    distance_str = "{:.2f}".format(inches) + " inches"
    # Speak the distance using the text-to-speech engine.
    engine.say(distance_str)
    engine.runAndWait()

def main():
    try:
        while True:
            # Get the distance in millimeters.
            distance = vl53.range

            if distance < 500:
                # Output the distance in millimeters and inches.
                print("Distance: {} cm)".format(convert_to_cm(distance)))
                # Speak the distance.
                say_distance(distance)
                # Wait for a moment before taking the next measurement.
                time.sleep(0.20)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

