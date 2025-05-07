#include <SoftwareSerial.h>

#include "Config.h"
#include "Memory.h"
#include "Display.h"
#include "Protocol.h"

int previousSwitchValue = -1;

void setup() {
    Serial.begin(9600);
    esp8266.begin(9600);

    lastMessageTimer = millis();
    pinMode(PIN_SWITCH, INPUT);

    lcd.init();
    lcd.backlight();
    lastLcdScrollTimer = millis();
}

void processInput(String input) {
    if (input == "data") {
        Serial.println("Current data:");
        printMemoryData();
    } else if (input == "reset data") {
        resetMemoryData();
        Serial.println("Reset data:");
        printMemoryData();
    }
}

void loop() {
    int switchValue = digitalRead(PIN_SWITCH);

    lcdUpdateText();

    if (esp8266.available()) {
        String message = esp8266.readStringUntil('\n');
        message.trim();
        parseMessage(message);
        expectsAnswer = false;
    } else if (sendNextStatus) {
        sendStatus(statusMessageValue);
        sendNextStatus = false;
    } else if (!expectsAnswer && switchValue != previousSwitchValue) {
        lastMessageTimer = millis();
        updateESPMode(switchValue == modeCLI ? idCLIMode : idAPMode);
        previousSwitchValue = switchValue;
    } else if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        if (!expectsAnswer) {
            input.trim();
            processInput(input);
        } else {
            Serial.print("[ERROR] Can't send messages while expecting answer: ");
            Serial.print(lastMessageDelay - (millis() - lastMessageTimer));
            Serial.println(" ms");
        }
    }

    if (expectsAnswer && millis() > lastMessageTimer + lastMessageDelay) {
        expectsAnswer = false;
        Serial.println("[WARNING] Too long no answer message");
    }
}
