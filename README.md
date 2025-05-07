The Raspberry Pi runs a web server via Apache, which only allows HTTPS and is secured with a username and password. On this HTML page, a button can be clicked, after which news articles related to Bitcoin are fetched using the News API. Sentiment analysis is applied to these headlines via NLP (Natural Language Processing) to determine whether they are positive, neutral, or negative. The retrieved headlines are then sorted by sentiment and displayed on the HTML page. Additionally, the titles are saved to the cloud according to their sentiment.

Furthermore, the Raspberry Pi communicates via BLE (Bluetooth Low Energy) with an Arduino Nano 33 BLE. This Arduino, in turn, drives an OLED display via I2C. The display shows the number of headlines per sentiment. Finally, an MQTT notification is sent to an ESP32, which lights up an LED if new headlines have been retrieved.

![image](https://github.com/user-attachments/assets/93b2ea56-6c1c-49da-aa8c-be6343c4e93b)
![image](https://github.com/user-attachments/assets/757cc40f-4cde-448c-9f10-3dd038384f09)
![image](https://github.com/user-attachments/assets/a4663698-5072-4434-b36a-fea0cac6a93b)
