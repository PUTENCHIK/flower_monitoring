// --- Toggle switch ---
#define PIN_SWITCH 4
const int modeCLI = 0;
const int modeAP = 1;

// --- Program UART Configuration ---
#define PIN_RX 2     // D2 Arduino for receiving data
#define PIN_TX 3     // D3 Arduino for transmiting data
SoftwareSerial esp8266(PIN_RX, PIN_TX);

// --- IDs of data ---
const int fieldDomen = 1;
const int fieldSsidCLI = 2;
const int fieldPasswordCLI = 3;
const int fieldSsidAP = 4;
const int fieldPasswordAP = 5;

// --- IDs of protocol messages ---
const int idCLIMode = 1;
const int idAPMode = 2;
const int idUpdateEEPROM = 3;
const int idMessage = 4;
const int idStatus = 5;

// --- Length of strings ---
const int maxMessageTextLength = 50;
const int maxDomenLength = 40;
const int maxSsidCLILength = 20;
const int maxPasswordCLILength = 20;
const int maxSsidAPLength = 20;
const int maxPasswordAPLength = 20;

// --- Consts ---
const char passwordAP[maxPasswordAPLength] = "admin123";
const unsigned long lastMessageDelay = 15000;