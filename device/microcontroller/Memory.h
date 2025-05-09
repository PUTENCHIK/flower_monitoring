#include <EEPROM.h>

struct Data {
    char domen[maxDomenLength + 1];                   // Domen of remote server (like http://192.168.0.10:5050)
    char ssidCLI[maxSsidCLILength + 1];               // Name of mobile / WiFi
    char passwordCLI[maxPasswordCLILength + 1];       // Password of mobile / WiFi
    char ssidAP[maxSsidAPLength + 1];                 // Name of own access point
    char password[maxPasswordLength + 1];             // Password of device
    int sendingDelay;                                 // Interval between sending data to server (min)
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

bool fillGlobalDataByValue() {
    String keyvalue, value;
    int scIndex = lastMessage.indexOf(';');
    int colonIndex, id;
    while (scIndex != -1) {
        keyvalue = lastMessage.substring(0, scIndex);
        colonIndex = keyvalue.indexOf(':');
        if (colonIndex != -1) {
            value = keyvalue.substring(colonIndex + 1);
            id = keyvalue.substring(0, colonIndex).toInt();
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
        lastMessage = lastMessage.substring(scIndex + 1);
        scIndex = lastMessage.indexOf(';');
    }
    return true;
}

// void resetMemoryData() {
//     updateDomen("-");
//     updateSsidCLI("-");
//     updatePasswordCLI("-");
//     updateSsidAP("MyESP8266");
//     updatePassword("password");
//     updateSendingDelay("");
//     putMemoryData();
// }

// void printMemoryData() {
//     Serial.print("\tdomen: ");
//     Serial.println(globalData.domen);
//     Serial.print("\tssidCLI: ");
//     Serial.println(globalData.ssidCLI);
//     Serial.print("\tpasswordCLI: ");
//     Serial.println(globalData.passwordCLI);
//     Serial.print("\tssidAP: ");
//     Serial.println(globalData.ssidAP);
//     Serial.print("\tpassword: ");
//     Serial.println(globalData.password);
//     Serial.print("\tsendingDelay: ");
//     Serial.println(globalData.sendingDelay);

//     Serial.print("\t(const) token: ");
//     Serial.println(token);
//     Serial.print("\t(const) passwordAP: ");
//     Serial.println(passwordAP);
// }
