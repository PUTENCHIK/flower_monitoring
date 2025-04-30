#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// --- Конфигурация Wi-Fi ---
const char* ssid     = "Galaxy A16";        // Замените на ваш SSID
const char* password = "qwerty4321";    // Замените на ваш пароль

// --- Конфигурация API ---
const char* apiServer = "http://127.0.0.1:5050"; // Замените на адрес вашего API сервера
const char* apiEndpoint = "/test"; // Замените на ваш API endpoint (например, /data)

// Определяем пины для SoftwareSerial
const int RX_PIN = 4; // ESP8266 RX подключен к Arduino TX (через делитель напряжения!)
const int TX_PIN = 2; // ESP8266 TX подключен к Arduino RX

// Создаем объект SoftwareSerial
SoftwareSerial arduinoSerial(RX_PIN, TX_PIN); // RX, TX

void setup() {
  Serial.begin(9600);
  arduinoSerial.begin(9600);
  arduinoSerial.println("Starting...");

  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  arduinoSerial.println("\nWiFi connected");
  arduinoSerial.print("IP address: ");
  arduinoSerial.println(WiFi.localIP());
}

void loop() {
  // Проверяем, пришли ли данные от Arduino Nano
  if (arduinoSerial.available()) {
    String message = arduinoSerial.readStringUntil('\n'); // Читаем строку до символа новой строки
    message.trim(); // Убираем лишние пробелы и символ новой строки в конце
    arduinoSerial.println("ESP received: " + message);
//    arduinoSerial.println("ESP received: " + message);

    // Отправляем запрос к API
    String apiResponse = sendApiRequest(message);

    // Выводим ответ API в консоль
    arduinoSerial.println("API Response: " + apiResponse);
  }
}

String sendApiRequest(String data) {
  WiFiClient client;
  HTTPClient http;

  String apiURL = String(apiServer) + String(apiEndpoint);

  Serial.println("Connecting to API: " + apiURL);
  arduinoSerial.println("Connecting to API: " + apiURL);

  http.begin(client, apiURL);
  http.addHeader("Content-Type", "application/json"); // Указываем тип содержимого

  String postData = "{\"data\":\"" + data + "\"}";

  Serial.println("Sending data: " + postData);
  arduinoSerial.println("Sending data: " + postData);

  int httpResponseCode = http.POST(postData);

  String payload = "Unknown error"; // Default error message

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    arduinoSerial.print("HTTP Response code: ");
    arduinoSerial.println(httpResponseCode);

    if (httpResponseCode == HTTP_CODE_OK || httpResponseCode == HTTP_CODE_MOVED_PERMANENTLY) {
      payload = http.getString();
      Serial.println("Payload Received: " + payload);
      arduinoSerial.println("Payload Received: " + payload);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      arduinoSerial.print("Error code: ");
      arduinoSerial.println(httpResponseCode);
    }
  } else {
    Serial.print("Error connecting: ");
    Serial.println(httpResponseCode);
    arduinoSerial.print("Error connecting: ");
    arduinoSerial.println(httpResponseCode);
  }

  http.end(); // Закрываем соединение

  return payload;
}
