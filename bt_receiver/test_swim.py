import board
import neopixel

# Configuration
LED_COUNT = 21          # Number of LED pixels
LED_PIN = 32    # GPIO 12 used for the NeoPixels

# Create NeoPixel object
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.5, auto_write=False)

def update_strip():
    # First 10 LEDs one color (e.g., Red)
    for i in range(10):
        strip[i] = (255, 0, 0)  # Red

    # Middle LED another color (e.g., White)
    strip[10] = (255, 255, 255)  # White

    # Last 10 LEDs another color (e.g., Green)
    for i in range(11, 21):
        strip[i] = (0, 255, 0)  # Green

    strip.show()

try:
    while True:
        update_strip()

except KeyboardInterrupt:
    # Turn off all LEDs when Ctrl+C is pressed
    strip.fill((0, 0, 0))
    strip.show()
