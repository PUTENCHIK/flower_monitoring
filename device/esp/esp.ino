#include <SoftwareSerial.h>
#include <ESP8266HTTPClient.h>

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
    } else if (sendNextStatus) {
        sendStatus();
        sendNextStatus = false;
    }
}

// String sendApiRequest(String data) {
//   WiFiClient client;
//   HTTPClient http;
//   String apiURL = String(apiServer) + String(apiEndpoint);
//   arduinoSerial.println("Connecting to API: " + apiURL);
//   http.begin(client, apiURL);
//   http.addHeader("Content-Type", "application/json");
//   String postData = "{\"data\":\"" + data + "\"}";
//   arduinoSerial.println("Sending data: " + postData);
//   int httpResponseCode = http.POST(postData);
//   String payload = "Unknown error";
//   if (httpResponseCode > 0) {
//     if (httpResponseCode == HTTP_CODE_OK || httpResponseCode == HTTP_CODE_MOVED_PERMANENTLY) {
//       payload = http.getString();
//     } else {
//       arduinoSerial.print("Error code: ");
//       arduinoSerial.println(httpResponseCode);
//     }
//   } else {
//     arduinoSerial.print("Error connecting: ");
//     arduinoSerial.println(httpResponseCode);
//   }
//   http.end();
//   return payload;
// }
