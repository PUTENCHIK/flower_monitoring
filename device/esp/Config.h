#include "IPAddress.h"
#include "core_esp8266_features.h"

// --- Program UART Configuration ---
const int RX_PIN = 4;       // ESP8266 GPIO4 / D2
const int TX_PIN = 2;       // ESP8266 GPIO2 / D4
SoftwareSerial arduinoSerial(RX_PIN, TX_PIN);

// --- AP configuration ---
IPAddress apIP(192, 168, 4, 1);
IPAddress dnsIP(192, 168, 4, 1);

// --- API server configuration ---
const char* apiEndpoint = "/devices/data";
const char* apiRequestBody = R"rawliteral(
{
    "deviceToken": "{{token}}",
    "password": "{{password}}",
    "ports": {
        "additionalProp1": {
            "value": {{v1}}
        },
        "additionalProp2": {
            "value": {{v2}}
        },
        "additionalProp3": {
            "value": {{v3}}
        }
    }
}
)rawliteral";

// --- IDs of data fields ---
const int fieldDomen = 1;
const int fieldSsidCLI = 2;
const int fieldPasswordCLI = 3;
const int fieldSsidAP = 4;
const int fieldPassword = 5;
const int fieldSendingDelay = 6;

const int fieldPasswordAP = 11;
const int fieldToken = 12;

const int sensor1 = 101;
const int sensor2 = 102;
const int sensor3 = 103;

// --- IDs of protocol messages ---
const int idCLIMode = 1;
const int idAPMode = 2;
const int idUpdateEEPROM = 3;
const int idMessage = 4;
const int idStatus = 5;
const int idData = 6;

// --- Length of strings ---
const int maxMessageTextLength = 50;
const int maxDomenLength = 40;
const int maxSsidCLILength = 20;
const int maxPasswordCLILength = 20;
const int maxSsidAPLength = 20;
const int maxPasswordAPLength = 20;
const int maxPasswordLength = 20;
const int maxTokenLength = 30;

// --- Consts ---
const int connectionCLIDelay = 500;
const unsigned long maxCLIConnectionTime = 10000;
const int disconnectTimeout = 300;
const int minSendingDelay = 1;
const int maxSendingDelay = 60;
const int defaultSendingDelay = 30;