#include <ArduinoBLE.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

BLEService lastTweetService ("19B10010-E8F2-537E-4F6C-D104768A1214"); // create service
BLEStringCharacteristic tweetCharacteristic("19B10011-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite, 30); // create switch characteristic and allow remote device to read and write
void setup() {
  Serial.begin(9600);
  
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy module failed!");
    while (1);
  }
  BLE.setLocalName("lastTweet"); // set the local name peripheral advertises
  BLE.setAdvertisedService(lastTweetService); // set the UUID for the service this peripheral advertises:// 
  lastTweetService.addCharacteristic(tweetCharacteristic); // add the characteristics to the service
  BLE.addService(lastTweetService);
  tweetCharacteristic.setEventHandler(BLEWritten, textReceived);
  tweetCharacteristic.setValue("BLE_peripheral_uart");
  BLE.advertise(); // start advertising
  Serial.println("Bluetooth® device active, waiting for connections...");
  Serial.println(BLE.address());

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.display();
  delay(2000); 
  display.clearDisplay(); // Clear the buffer
  display.setTextSize(1);
  display.setTextColor(WHITE);
}

void loop() {
  BLE.poll(); // poll for Bluetooth® Low Energy events
}

void textReceived(BLEDevice central, BLECharacteristic characteristic){
  Serial.println("Received");
  String valString = tweetCharacteristic.value();
  Serial.println(valString);
  display.clearDisplay();
  display.setCursor(0,0);
  display.println(valString);
  display.display();
}
