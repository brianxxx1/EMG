import time
from rpi_ws281x import PixelStrip, Color
import random
# LED strip configuration:
LED_COUNT = 21          # Number of LED pixels
LED_PIN = 12            # GPIO pin connected to the pixels (must support PWM)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10            # DMA channel to use for generating signal
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def light_specific_leds(lower_half_index, upper_half_index):
    # Ensure indices are within the valid range
    if lower_half_index < 0 or lower_half_index > 9 or upper_half_index < 11 or upper_half_index > 20:
        print("Invalid indices. Lower index should be 0-9, upper index should be 11-20.")
        return

    # Turn off all LEDs first
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))

    # Light up the specified LED in the lower half
    strip.setPixelColor(lower_half_index, Color(255, 0, 0))  # Red

    # Middle LED in white
    strip.setPixelColor(10, Color(255, 255, 255))  # White

    # Light up the specified LED in the upper half
    strip.setPixelColor(upper_half_index, Color(0, 255, 0))  # Green

    strip.show()

try:
    while True:
        # Example indices - replace these with your own logic
        lo = random.randint(0,9)
        up = random.randint(11,20)
        light_specific_leds(lo, up)


except KeyboardInterrupt:
    # Turn off all LEDs when Ctrl+C is pressed
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
