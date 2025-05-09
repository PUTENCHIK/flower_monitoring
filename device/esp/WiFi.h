#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

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

void sendServerRequest() {
    WiFiClient client;
    HTTPClient http;
    String apiURL = String(globalData.domen) + String(apiEndpoint);
    http.begin(client, apiURL);
    http.addHeader("Content-Type", "application/json");
    String body = apiRequestBody;
    body.replace("{{token}}", String(globalData.token));
    body.replace("{{password}}", String(globalData.password));
    body.replace("{{v1}}", String(globalData.v1));
    body.replace("{{v2}}", String(globalData.v2));
    body.replace("{{v3}}", String(globalData.v3));
    int httpResponseCode = http.PATCH(body);
    String payload = "Unknown error";
    if (httpResponseCode > 0) {
        if (httpResponseCode == HTTP_CODE_OK || httpResponseCode == HTTP_CODE_MOVED_PERMANENTLY) {
            payload = http.getString();
        } else {
            payload = "Bad response status: " + String(httpResponseCode);
        }
    } else {
        payload = "No connection: " + String(httpResponseCode);
    }
    http.end();
    sendConsoleMessage(payload);
}