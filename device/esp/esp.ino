#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// --- Конфигурация Wi-Fi ---
const char* ssid     = "Galaxy A16";        // Замените на ваш SSID
const char* password = "qwerty4321";    // Замените на ваш пароль

// --- Конфигурация API ---
const char* apiServer = "http://localhost:5050"; // Замените на адрес вашего API сервера
const char* apiEndpoint = "/test"; // Замените на ваш API endpoint (например, /data)

// --- Пин для Serial Communication с Arduino Nano ---
const int rxPin = 2; // GPIO2 (D4 на некоторых платах) - RX ESP8266 (прием данных от Arduino)

void setup() {
  Serial.begin(9600);
  Serial.println("Starting...");

  // Инициализация Serial для общения с Arduino Nano
  Serial1.begin(9600, SERIAL_8N1, SERIAL_RX_ONLY, rxPin); // Serial1 использует HardwareSerial

  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Проверяем, пришли ли данные от Arduino Nano
  if (Serial1.available() > 0) {
    String arduinoInput = Serial1.readStringUntil('\n'); // Читаем строку до символа новой строки
    arduinoInput.trim(); // Убираем лишние пробелы и символ новой строки в конце
    Serial.print("Received from Arduino: ");
    Serial.println(arduinoInput);

    // Отправляем запрос к API
    String apiResponse = sendApiRequest(arduinoInput);

    // Выводим ответ API в консоль
    Serial.print("API Response: ");
    Serial.println(apiResponse);
  }
}

String sendApiRequest(String data) {
  WiFiClient client;
  HTTPClient http;

  String apiURL = String(apiServer) + String(apiEndpoint);

  Serial.print("Connecting to API: ");
  Serial.println(apiURL);

  http.begin(client, apiURL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded"); // Указываем тип содержимого

  String postData = "data=" + data; // Формируем данные для отправки в теле POST запроса

  Serial.print("Sending data: ");
  Serial.println(postData);

  int httpResponseCode = http.POST(postData);

  String payload = "Error"; // Default error message

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode == HTTP_CODE_OK || httpResponseCode == HTTP_CODE_MOVED_PERMANENTLY) {
      payload = http.getString();
      Serial.print("Payload Received: ");
      Serial.println(payload);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
  } else {
    Serial.print("Error connecting: ");
    Serial.println(httpResponseCode);
  }

  http.end(); // Закрываем соединение

  return payload;
}
