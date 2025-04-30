#include <SoftwareSerial.h>

const int RX_PIN = 2; // Пин Arduino для приема данных от ESP8266
const int TX_PIN = 3; // Пин Arduino для отправки данных на ESP8266

SoftwareSerial esp8266(RX_PIN, TX_PIN); // Создаем объект SoftwareSerial

void setup() {
  Serial.begin(9600);   // Инициализация Serial для монитора
  esp8266.begin(9600); // Инициализация SoftwareSerial для ESP8266
}

void loop() {
  if (esp8266.available()) {
    // Читаем данные, отправленные с ESP8266 через SoftwareSerial
    String message = esp8266.readStringUntil('\n');
    Serial.print("Nano received from ESP8266: ");
    Serial.println(message);
  }
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // Убираем лишние пробелы и символ новой строки

    Serial.println("Nano sending: " + input);
    esp8266.println(input);
  }
}
