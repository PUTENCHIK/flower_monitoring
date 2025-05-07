#include "EEPROM.h"
int currentESPMode = 0;                   // Contains current id of ESP mode: CLI or AP
bool expectsAnswer = false;               // While microcontroller is not getting answer, it doesn't sends anything
bool sendNextStatus = false;              // If true, microcontroller will send status message
bool statusMessageValue;                  // Value of status message which will be send next
unsigned long lastMessageTimer;           // Contains timestamp of last message to block other messages

void sendMessage(int id, String message) {
    String m = String(id) + ":" + message;
    Serial.println("Transmit: " + m);
    esp8266.println(m);
}

void sendStatus(bool status) {
    sendMessage(idStatus, String(status));
}

void setSendStatus(bool newValue) {
    sendNextStatus = true;
    statusMessageValue = newValue;
}

void processMessage(int id, String message) {
    expectsAnswer = false;
    bool result;
    switch (id) {
        case idUpdateEEPROM:
            result = fillGlobalDataByValue(message);
            if (result) {
                putMemoryData();
                Serial.println("Updated data from ESP:");
            } else {
                Serial.println("Data from ESP is invalid. Old data:");
            }
            printMemoryData();
            setSendStatus(result);
            break;
        case idMessage:
            Serial.println("Console message from ESP: " + message);
            break;
        case idStatus:
            Serial.println("Status from ESP: " + message);
            break;
        default:
            Serial.println("\t[ERROR] Unknown message id: " + String(id));
            expectsAnswer = true;
        }
}

void parseMessage(String message) {
    Serial.println("Receive: " + message);
    int colonIndex = message.indexOf(':');
    if (colonIndex != -1) {
        String key = message.substring(0, colonIndex);
        key.trim();
        String value = message.substring(colonIndex + 1);
        value.trim();
        int keyId = key.toInt();
        if (!keyId) {
            Serial.print("\t[ERROR] Key ID is not integer or zero: " + String(key));
            setSendStatus(false);
        } else {
            processMessage(keyId, value);
        }
    } else {
        Serial.println("\t[ERROR] No colon in message");
        setSendStatus(false);
    }
}

void updateESPMode(int newMode) {
    String value = "";
    switch (newMode) {
        case idCLIMode:
        case idAPMode:
            currentESPMode = newMode;
            updateGlobalData();
            Serial.println("Switching ESP mode to " + String(newMode == idCLIMode ? "CLI" : "AP"));
            value += stringifyMemoryValue(fieldDomen);
            value += stringifyMemoryValue(fieldSsidCLI);
            value += stringifyMemoryValue(fieldPasswordCLI);
            if (newMode == idAPMode) {
                value += stringifyMemoryValue(fieldSsidAP);
                value += stringifyMemoryValue(fieldPassword);
                value += stringifyMemoryValue(fieldSendingDelay);
                value += stringifyMemoryValue(fieldPasswordAP);
                value += stringifyMemoryValue(fieldToken);
            }
            break;
        default:
            Serial.println("[ERROR] Unknown mode: " + String(newMode));
    }
    if (value)
        sendMessage(newMode, value);
        expectsAnswer = true;
}
