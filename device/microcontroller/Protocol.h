#include "HardwareSerial.h"
#include "EEPROM.h"
int currentESPMode = 0;                   // Contains current id of ESP mode: CLI or AP
int lastMessageId;                        // Id of last message's id
bool expectsAnswer = false;               // While microcontroller is not getting answer, it doesn't sends anything
bool sendNextStatus = false;              // If true, microcontroller will send status message
bool statusMessageValue;                  // Value of status message which will be send next
unsigned long lastMessageTimer;           // Contains timestamp of last message to block other messages

void sendMessage(int id, String text) {
    Serial.print("Transmit: ");
    Serial.print(id);
    Serial.print(':');
    Serial.println(text);
    esp8266.print(id);
    esp8266.print(':');
    esp8266.println(text);
    lastMessageId = id;
}

void sendStatus(bool status) {
    sendMessage(idStatus, String(status));
}

void setSendStatus(bool newValue) {
    sendNextStatus = true;
    statusMessageValue = newValue;
}

void processReceivedStatus(int status) {
    String strStatus = status ? "success" : "fail";
    switch (lastMessageId) {
        case idCLIMode:
            lcdStatus = "CLI mode";
            updateLcdMessage(strStatus);
            break;
        case idAPMode:
            lcdStatus = "AP mode";
            updateLcdMessage(strStatus);
            break;
        case idData:
            break;
        default:
            Serial.print("Unknown last command; status: ");
            Serial.println(strStatus);
    }
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
            Serial.print("Console message from ESP: ");
            Serial.println(message);
            updateLcdMessage(message);
            break;
        case idStatus:
            Serial.print("Status from ESP: ");
            Serial.println(message);
            processReceivedStatus(message.toInt());
            break;
        default:
            Serial.print("\t[ERROR] Unknown message id: ");
            Serial.println(id);
            expectsAnswer = true;
        }
}

void parseMessage(String message) {
    Serial.print("Receive: ");
    Serial.println(message);
    int colonIndex = message.indexOf(':');
    if (colonIndex != -1) {
        String key = message.substring(0, colonIndex);
        key.trim();
        String value = message.substring(colonIndex + 1);
        value.trim();
        int keyId = key.toInt();
        if (!keyId) {
            Serial.print("\t[ERROR] Key ID is not integer or zero: ");
            Serial.println(key);
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
            Serial.println("Switching ESP mode to ");
            Serial.println(newMode == idCLIMode ? "CLI" : "AP");
            updateLcdMessage("Switching to " + String(newMode == idCLIMode ? "CLI" : "AP"));
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
            Serial.print("[ERROR] Unknown mode: ");
            Serial.println(newMode);
    }
    if (value) {
        sendMessage(newMode, value);
        expectsAnswer = true;
    }
}
