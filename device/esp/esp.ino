#include <SoftwareSerial.h>

#include "Config.h"
#include "Html.h"
#include "Data.h"
#include "Protocol.h"
#include "WiFi.h"
#include "Server.h"

void setup() {
    Serial.begin(9600);
    arduinoSerial.begin(9600);
    delay(500);
}

void loop() {
    if (serverRunning) {
        dnsServer.processNextRequest();
        server.handleClient();
    }
    if (arduinoSerial.available()) {
        String message = arduinoSerial.readStringUntil('\n');
        message.trim();
        parseMessage(message);
    } else if (updateESPSettings) {
        updateESPSettings = false;
        initESPMode(newModeCandidate);
        if (currentMode == idAPMode) {
            initServer();
        }
    } else if (sendServerData) {
        sendServerData = false;
        sendServerRequest();
    } else if (sendNextStatus) {
        sendStatus();
        sendNextStatus = false;
    }
}