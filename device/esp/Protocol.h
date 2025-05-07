bool sendNextStatus = false;        // If true, ESP will send status message
bool statusMessageValue;            // Value of status message which will be send next
bool updateESPSettings = false;     // If true, ESP will init corresponding mode and optionally server
int newModeCandidate;

void sendMessage(int id, String message) {
    arduinoSerial.println(String(id) + ":" + message);
}

void sendStatus() {
    sendMessage(idStatus, String(statusMessageValue));
}

void sendConsoleMessage(String message) {
    sendMessage(idMessage, message);
}

void sendNewMemoryData() {
    String value = stringifyMemoryValue(fieldDomen);
    value += stringifyMemoryValue(fieldSsidCLI);
    value += stringifyMemoryValue(fieldPasswordCLI);
    value += stringifyMemoryValue(fieldSsidAP);
    value += stringifyMemoryValue(fieldPassword);
    value += stringifyMemoryValue(fieldSendingDelay);
    sendMessage(idUpdateEEPROM, value);
}

void setSendStatus(bool newValue) {
    sendNextStatus = true;
    statusMessageValue = newValue;
}

void processMessage(int id, String value) {
    bool result;
//    String m;
    switch (id) {
        case idCLIMode:
        case idAPMode:
            statusMessageValue = true;
            result = fillGlobalDataByValue(value);
            updateESPSettings = result;
            newModeCandidate = id;
//            if (!result) {
//                sendConsoleMessage(m);
//            }
            setSendStatus(result);
            break;
        case idStatus:
            sendNextStatus = false;
            break;
        default:
            sendConsoleMessage("[ERROR] Unknown message id: " + String(id));
    }
}

void parseMessage(String message) {
    int colonIndex = message.indexOf(':');
    if (colonIndex != -1) {
        String key = message.substring(0, colonIndex);
        key.trim();
        String value = message.substring(colonIndex + 1);
        value.trim();
        int keyId = key.toInt();
        if (!keyId) {
            setSendStatus(false);
//            sendConsoleMessage("No key id in message");
        } else {
            processMessage(keyId, value);
        }
    } else {
        setSendStatus(false);
//        sendConsoleMessage("No colon in message");
    }
}
