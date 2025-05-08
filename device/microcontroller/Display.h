#include <LiquidCrystal_I2C.h>

// Adress: either 0x3f, or 0x27, 0x26
LiquidCrystal_I2C lcd(0x3F, displayColumns, displayRows);

String lcdStatus = "Initing";
String lcdMessage = "";
int lcdPointer = 0;
bool isLcdMessageUpdated = false;
long unsigned lastLcdScrollTimer;

void displayStatus() {
    lcd.home();
    lcd.print(lcdStatus);
}

void updateLcdMessage(String newValue) {
    lcdMessage = newValue;
    lcdPointer = 0;
    isLcdMessageUpdated = true;
}

void displayMessage() {
    lcd.setCursor(0, 1);
    if (lcdMessage.length() <= displayColumns) {
        lcd.print(lcdMessage);
    } else {
        lcd.print(lcdMessage.substring(lcdPointer, displayColumns+lcdPointer));
        lastLcdScrollTimer = millis();
        if (displayColumns+lcdPointer++ == lcdMessage.length())
            lcdPointer = 0;
    }
}

void lcdUpdateText(bool lcdForceUpdate = false) {
    if (lcdForceUpdate || isLcdMessageUpdated || (lcdMessage.length() > displayColumns && millis() >= lastLcdScrollTimer + scrollDisplayDelay)) {
        lcd.clear();
        displayStatus();
        displayMessage();
        isLcdMessageUpdated = false;
    }
}