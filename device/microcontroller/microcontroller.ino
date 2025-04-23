void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // Убираем лишние пробелы и символ новой строки

    Serial.print("Received: ");
    Serial.println(input);

    // Отправляем данные в ESP8266
    Serial.println(input); // Отправляем данные через Serial
    delay(100);
  }
}
