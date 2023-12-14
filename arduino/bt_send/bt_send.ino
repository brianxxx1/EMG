
#include <ArduinoBLE.h>
#include <Adafruit_NeoPixel.h>

#define SERVICE_UUID  "19B10000-E8F2-537E-4F6C-D104768A1214"
#define LEFT_CHARACTERISTIC_UUID "19B10000-E8F2-537E-4F6C-D104768A1214"
#define RIGHT_CHARACTERISTIC_UUID "19B10000-E8F2-537E-4F6C-D104768A1215"

#define LED_PIN    11
#define LED_COUNT  21

BLEService BLEservice(SERVICE_UUID);

// Bluetooth® Low Energy LED Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEUnsignedCharCharacteristic left_characteristic(LEFT_CHARACTERISTIC_UUID, BLERead | BLEWrite);
BLEUnsignedCharCharacteristic right_characteristic(RIGHT_CHARACTERISTIC_UUID, BLERead | BLEWrite);

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int initLeftValue = 0;
int initRightValue = 0;

const int ledPin = LED_BUILTIN;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  // set LED pin to output mode
  pinMode(ledPin, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy module failed!");

    while (1);
  }

  BLE.setLocalName("EMG");
  BLE.setAdvertisedService(BLEservice);

  // add the characteristic to the service
  BLEservice.addCharacteristic(left_characteristic);
  BLEservice.addCharacteristic(right_characteristic);


  // add service
  BLE.addService(BLEservice);

  left_characteristic.writeValue(initLeftValue);
  right_characteristic.writeValue(initRightValue);

  // start advertising
  BLE.advertise();
  Serial.println("BLE LED Peripheral");
}

void loop() {
  // listen for Bluetooth® Low Energy peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      digitalWrite(ledPin, HIGH);   
      updateValue();
      delay(1); // 40ms => 25 readings/sec => voting can have a odd number to break the tie
    }

    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
    digitalWrite(ledPin, LOW);   
  }
}

void updateValue() {
  int left_emg_pin = A0;
  int right_emg_pin = A1;
  int left_emg_val = 0;
  int right_emg_val = 0;

  left_emg_val = analogRead(left_emg_pin);
  right_emg_val = analogRead(right_emg_pin);

  left_characteristic.writeValue(left_emg_val);
  right_characteristic.writeValue(right_emg_val);

  int lowerHalfIndex = mapSignalToLedIndex(left_emg_val, 0, 1023, true);
  int upperHalfIndex = mapSignalToLedIndex(right_emg_val, 0, 1023, false);
  lightSpecificLeds(lowerHalfIndex, upperHalfIndex);
  
  Serial.print(F("Left EMG value sent: "));
  Serial.println(left_emg_val);

  Serial.print(F("Right EMG value sent: "));
  Serial.println(right_emg_val);

}


void lightSpecificLeds(int lowerHalfIndex, int upperHalfIndex) {
  for (int i = 0; i < LED_COUNT; i++) {
    if (i == lowerHalfIndex)
      strip.setPixelColor(i, strip.Color(255, 0, 0)); // Red
    else if (i == 10)
      strip.setPixelColor(i, strip.Color(255, 255, 255)); // White
    else if (i == upperHalfIndex)
      strip.setPixelColor(i, strip.Color(0, 255, 0)); // Green
    else
      strip.setPixelColor(i, strip.Color(0, 0, 0)); // Off
  }
  strip.show();
}

int mapSignalToLedIndex(int signal, int min_value, int max_value, bool is_left) {
  return mapValue(signal, min_value, max_value, is_left ? 0 : 11, is_left ? 9 : 20);
}

long mapValue(long value, long in_min, long in_max, long out_min, long out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}