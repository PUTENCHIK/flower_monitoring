#include <SoftwareSerial.h>

#include "Config.h"
#include "Memory.h"
#include "Display.h"
#include "Protocol.h"
#include "Data.h"

int previousSwitchValue = -1;

void setup() {
    Serial.begin(9600);
    esp8266.begin(9600);

    lastMessageTimer = millis();
    pinMode(PIN_SWITCH, INPUT);

    lcd.init();
    lcd.backlight();
    lastLcdScrollTimer = millis();

    dataSendingTimer = millis();
    updateGlobalData();
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
        updateESPMode(switchValue == 0 ? idCLIMode : idAPMode);
        previousSwitchValue = switchValue;
    }

    checkSendingData();

    if (expectsAnswer && millis() > lastMessageTimer + lastMessageDelay) {
        expectsAnswer = false;
        Serial.println("[WARNING] Too long no answer message");
    }
}
