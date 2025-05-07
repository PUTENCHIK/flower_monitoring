#include <ESP8266WebServer.h>
#include <DNSServer.h>

ESP8266WebServer server(80);
DNSServer dnsServer;

bool serverRunning = false;

void handleRoot() {
    String page = htmlPage;
    page.replace("{{domen}}", String(globalData.domen));
    page.replace("{{ssidCLI}}", String(globalData.ssidCLI));
    page.replace("{{passwordCLI}}", String(globalData.passwordCLI));
    page.replace("{{ssidAP}}", String(globalData.ssidAP));
    page.replace("{{passwordAP}}", String(globalData.passwordAP));
    page.replace("{{token}}", String(globalData.token));
    page.replace("{{password}}", String(globalData.password));
    page.replace("{{sendingDelay}}", String(globalData.sendingDelay));
    server.send(200, "text/html", page);
}

void handleConfig() {
    String domen, ssidCLI, passwordCLI, ssidAP, password, sendingDelay;
    bool flag = true;
    if (server.hasArg("domen")) {                                 // domen
        domen = server.arg("domen");
        domen.trim();
    } else {
        sendConsoleMessage("No 'domen' in POST request");
        flag = false;
    }
    if (server.hasArg("ssidCLI")) {                               // ssidCLI
        ssidCLI = server.arg("ssidCLI");
        ssidCLI.trim();
    } else {
        sendConsoleMessage("No 'ssidCLI' in POST request");
        flag = false;
    }
    if (server.hasArg("passwordCLI")) {                           // passwordCLI
        passwordCLI = server.arg("passwordCLI");
        passwordCLI.trim();
    } else {
        sendConsoleMessage("No 'passwordCLI' in POST request");
        flag = false;
    }
    if (server.hasArg("ssidAP")) {                                // ssidAP
        ssidAP = server.arg("ssidAP");
        ssidAP.trim();
    } else {
        sendConsoleMessage("No 'ssidAP' in POST request");
        flag = false;
    }
    if (server.hasArg("password")) {                              // password
        password = server.arg("password");
        password.trim();
    } else {
        sendConsoleMessage("No 'password' in POST request");
        flag = false;
    }
    if (server.hasArg("sendingDelay")) {                          // sendingDelay
        sendingDelay = server.arg("sendingDelay");
        sendingDelay.trim();
    } else {
        sendConsoleMessage("No 'sendingDelay' in POST request");
        flag = false;
    }
    if (flag) {
        if (domen.length())
            updateDomen(domen);
        if (ssidCLI.length())
            updateSsidCLI(ssidCLI);
        if (passwordCLI.length())
            updatePasswordCLI(passwordCLI);
        if (ssidAP.length() && ssidAP != String(globalData.ssidAP)) {
            updateSsidAP(ssidAP);
            updateESPSettings = true;
        }
        if (password.length())
            updatePassword(password);
        if (sendingDelay.length())
            updateSendingDelay(sendingDelay);
        sendNewMemoryData();
        server.sendHeader("Location", "/");
        server.send(303);
    }
}

void handleNotFound(){
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET) ? "GET" : "POST";
    message += "\nArguments: ";
    message += server.args();
    message += "\n";
    for (int i = 0; i < server.args(); i++) {
        message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
    }
    server.send(404, "text/plain", message);
}

void initServer() {
    dnsServer.stop();
    server.stop();

    dnsServer.setErrorReplyCode(DNSReplyCode::NoError);
    dnsServer.start(53, "*", apIP);

    server.on("/", HTTP_GET, handleRoot);
    server.on("/config", HTTP_POST, handleConfig);  
    server.onNotFound(handleNotFound);

    server.begin();
    serverRunning = true;
}
