long unsigned dataSendingTimer;

String stringifySensorValue(int id, int value) {
    return String(id) + ":" + String(value) + ";";
}

void sendSensorsData() {
    int v1, v2, v3;
    v1 = analogRead(PIN_POT1);
    v2 = analogRead(PIN_POT2);
    v3 = analogRead(PIN_POT3);
    String value = stringifyMemoryValue(fieldToken);
    value += stringifyMemoryValue(fieldPassword);
    value += stringifySensorValue(sensor1, v1);
    value += stringifySensorValue(sensor2, v2);
    value += stringifySensorValue(sensor3, v3);
    sendMessage(idData, value);
    expectsAnswer = true;
}

void checkSendingData() {
    if (currentESPMode == idCLIMode && millis() >= dataSendingTimer + (globalData.sendingDelay * 60000)) {
        dataSendingTimer = millis();
        sendSensorsData();
    }
}