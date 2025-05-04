#include <SoftwareSerial.h>

#include "Config.h"
#include "Memory.h"
#include "Protocol.h"

void setup() {
    Serial.begin(9600);
    esp8266.begin(9600);

    lastMessageTimer = millis();
}

void processInput(String input) {
    if (input == "data") {
        Serial.println("Current data:");
        printMemoryData();
    } else if (input == "reset data") {
        resetMemoryData();
        Serial.println("Reset data:");
        printMemoryData();
    } else if (input == "cli") {
        lastMessageTimer = millis();
        updateESPMode(idCLIMode);
    } else if (input == "ap") {
        lastMessageTimer = millis();
        updateESPMode(idAPMode);
    }
}

void loop() {
    if (esp8266.available()) {
        String message = esp8266.readStringUntil('\n');
        message.trim();
        parseMessage(message);
        expectsAnswer = false;
    } else if (sendNextStatus) {
        sendStatus(statusMessageValue);
        sendNextStatus = false;
    } else if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        if (!expectsAnswer) {
            input.trim();
            processInput(input);
        } else {
            Serial.println("[ERROR] Can't send messages while expecting answer: " + String(lastMessageDelay - (millis() - lastMessageTimer)) + " ms");
        }
    }

    if (expectsAnswer && millis() > lastMessageTimer + lastMessageDelay) {
        expectsAnswer = false;
        Serial.println("[WARNING] Too long no answer message");
    }
}
