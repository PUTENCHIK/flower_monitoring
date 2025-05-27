// --- Toggle switch ---
#define PIN_SWITCH 4

// --- Liquid Crystal Config ---
// SDA - A4
// SCL - A5

// --- Program UART Configuration ---
#define PIN_RX 2     // D2 Arduino for receiving data
#define PIN_TX 3     // D3 Arduino for transmiting data
SoftwareSerial esp8266(PIN_RX, PIN_TX);

// --- Liquid crystal display ---
const int scrollDisplayDelay = 800;     // Delay for scroll too long messages (ms)

// --- Flowers data ---
#define PIN_POT1 A1
#define PIN_POT2 A2
#define PIN_POT3 A3

// --- Protocol variables
String lastMessage;

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
const int maxDomenLength = 40;
const int maxSsidCLILength = 20;
const int maxPasswordCLILength = 20;
const int maxSsidAPLength = 20;
const int maxPasswordLength = 20;

// --- Consts ---
const char* token = "newtoken";
const char* passwordAP = "admin123";
const unsigned long lastMessageDelay = 15000;