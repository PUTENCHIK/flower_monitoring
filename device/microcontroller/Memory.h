#include <EEPROM.h>

struct Data {
    char domen[maxDomenLength + 1];                   // Domen of remote server (like http://192.168.0.10:5050)
    char ssidCLI[maxSsidCLILength + 1];               // Name of mobile / WiFi
    char passwordCLI[maxPasswordCLILength + 1];       // Password of mobile / WiFi
    char ssidAP[maxSsidAPLength + 1];                 // Name of own access point
};

Data globalData;

void updateMemoryData() {
    EEPROM.put(0, globalData);
}

String stringifyMemoryValue(int id) {
    Data data;
    EEPROM.get(0, data);
    String result = String(id) + ":";
    switch (id) {
        case fieldDomen:
            result += String(data.domen);
            break;
        case fieldSsidCLI:
            result += String(data.ssidCLI);
            break;
        case fieldPasswordCLI:
            result += String(data.passwordCLI);
            break;
        case fieldSsidAP:
            result += String(data.ssidAP);
            break;
    }
    result += ";";
    return result;
}

void updateDomen(String value) {
    char str[maxDomenLength + 1];
    value.toCharArray(str, sizeof(str));
    strncpy(globalData.domen, str, maxDomenLength);
    globalData.domen[maxDomenLength] = 0;
}

void updateSsidCLI(String value) {
    char str[maxSsidCLILength + 1];
    value.toCharArray(str, sizeof(str));
    strncpy(globalData.ssidCLI, str, maxSsidCLILength);
    globalData.ssidCLI[maxSsidCLILength] = 0;
}

void updatePasswordCLI(String value) {
    char str[maxPasswordCLILength + 1];
    value.toCharArray(str, sizeof(str));
    strncpy(globalData.passwordCLI, str, maxPasswordCLILength);
    globalData.passwordCLI[maxPasswordCLILength] = 0;
}

void updateSsidAP(String value) {
    char str[maxSsidAPLength + 1];
    value.toCharArray(str, sizeof(str));
    strncpy(globalData.ssidAP, str, maxSsidAPLength);
    globalData.ssidAP[maxSsidAPLength] = 0;
}

bool fillGlobalDataByValue(String string) {
    String keyvalue, key, value;
    int scIndex = string.indexOf(';');
    int colonIndex, id;
    while (scIndex != -1) {
        keyvalue = string.substring(0, scIndex);
        colonIndex = keyvalue.indexOf(':');
        if (colonIndex != -1) {
            key = keyvalue.substring(0, colonIndex);
            value = keyvalue.substring(colonIndex + 1);
            id = key.toInt();
            switch (id) {
                case fieldDomen:
                    updateDomen(value);
                    break;
                case fieldSsidCLI:
                    updateSsidCLI(value);
                    break;
                case fieldPasswordCLI:
                    updatePasswordCLI(value);
                    break;
                case fieldSsidAP:
                    updateSsidAP(value);
                    break;
                default:
                    return false;
            }
        } else {
            return false;
        }
        string = string.substring(scIndex + 1);
        scIndex = string.indexOf(';');
    }
    return true;
}

void resetMemoryData() {
    updateDomen("-");
    updateSsidCLI("-");
    updatePasswordCLI("-");
    updateSsidAP("MyESP8266");
    updateMemoryData();
}

void printMemoryData() {
    Data data;
    EEPROM.get(0, data);
    Serial.print("\tdomen: ");
    Serial.println(data.domen);
    Serial.print("\tssidCLI: ");
    Serial.println(data.ssidCLI);
    Serial.print("\tpasswordCLI: ");
    Serial.println(data.passwordCLI);
    Serial.print("\tssidAP: ");
    Serial.println(data.ssidAP);
    Serial.print("\tpasswordAP: ");
    Serial.println(passwordAP);
}