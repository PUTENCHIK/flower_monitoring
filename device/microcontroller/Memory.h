#include <EEPROM.h>

struct Data {
    char domen[maxDomenLength + 1];                   // Domen of remote server (like http://192.168.0.10:5050)
    char ssidCLI[maxSsidCLILength + 1];               // Name of mobile / WiFi
    char passwordCLI[maxPasswordCLILength + 1];       // Password of mobile / WiFi
    char ssidAP[maxSsidAPLength + 1];                 // Name of own access point
    char password[maxPasswordLength + 1];             // Password of device
    int sendingDelay;                                 // Interval between sending data to server
};

Data globalData;

void putMemoryData() {
    EEPROM.put(0, globalData);
}

void updateGlobalData() {
    EEPROM.get(0, globalData);
}

String stringifyMemoryValue(int id) {
    String result = String(id) + ":";
    switch (id) {
        case fieldDomen:
            result += String(globalData.domen);
            break;
        case fieldSsidCLI:
            result += String(globalData.ssidCLI);
            break;
        case fieldPasswordCLI:
            result += String(globalData.passwordCLI);
            break;
        case fieldSsidAP:
            result += String(globalData.ssidAP);
            break;
        case fieldPassword:
            result += String(globalData.password);
            break;
        case fieldSendingDelay:
            result += String(globalData.sendingDelay);
            break;
        case fieldPasswordAP:
            result += String(passwordAP);
            break;
        case fieldToken:
            result += String(token);
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

void updatePassword(String value) {
    char str[maxPasswordLength + 1];
    value.toCharArray(str, sizeof(str));
    strncpy(globalData.password, str, maxPasswordLength);
    globalData.password[maxPasswordLength] = 0;
}

void updateSendingDelay(String value) {
    int v = value.toInt();
    globalData.sendingDelay = !v ? 5 : v;
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
                case fieldPassword:
                    updatePassword(value);
                    break;
                case fieldSendingDelay:
                    updateSendingDelay(value);
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
    updatePassword("password");
    updateSendingDelay("");
    putMemoryData();
}

void printMemoryData() {
    Data data;
    EEPROM.get(0, data);
    Serial.println("\tdomen: " + String(data.domen));
    Serial.println("\tssidCLI: " + String(data.ssidCLI));
    Serial.println("\tpasswordCLI: " + String(data.passwordCLI));
    Serial.println("\tssidAP: " + String(data.ssidAP));
    Serial.println("\tpassword: " + String(data.password));
    Serial.println("\tsendingDelay: " + String(data.sendingDelay));

    Serial.print("\t(const) token: " + String(token));
    Serial.print("\t(const) passwordAP: " + String(passwordAP));
}
