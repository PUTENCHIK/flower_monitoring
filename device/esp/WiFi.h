#include <ESP8266WiFi.h>

int currentMode = 0;
bool statusChanged = false;
unsigned long connectionStartTimer;

void initCLI() {
    WiFi.disconnect();
    delay(disconnectTimeout);
    WiFi.mode(WIFI_STA);
    WiFi.begin(String(globalData.ssidCLI), String(globalData.passwordCLI));
    connectionStartTimer = millis();
    while (WiFi.status() != WL_CONNECTED) {
        if (millis() >= connectionStartTimer + maxCLIConnectionTime) {
            sendConsoleMessage("Failed to connect to access point");
            updateESPSettings = true;
            WiFi.disconnect();
            delay(disconnectTimeout);
            break;
        }
        delay(connectionCLIDelay);
    }
}

void initAP() {
    WiFi.disconnect();
    delay(disconnectTimeout);
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
    WiFi.softAP(String(globalData.ssidAP), String(globalData.passwordAP));
}

void initESPMode(int mode) {
    switch (mode) {
        case idCLIMode:
            currentMode = mode;
            initCLI();
            break;
        case idAPMode:
            currentMode = mode;
            initAP();
            break;
    }
}