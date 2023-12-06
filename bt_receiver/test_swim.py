import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 21         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (18 uses PWM).
# Other configuration variables as needed...

strip = PixelStrip(LED_COUNT, LED_PIN, 800000, 5, True, 255)
strip.begin()

def light_up_led(index, color):
    if index < 0 or index >= LED_COUNT:
        return

    # Turn off all LEDs
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    
    # Set the middle LED to white
    strip.setPixelColor(10, Color(255, 255, 255))

    # Light up the specified LED
    strip.setPixelColor(index, color)
    strip.show()

# Example usage
try:
    while True:
        # Example data received (replace with your data logic)
        data = 5  # Replace with actual data index

        # Decide the color based on the LED index
        color = Color(255, 0, 0) if data < 10 else Color(0, 255, 0)

        # Call the function to light up the LED
        light_up_led(data, color)
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all LEDs
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
