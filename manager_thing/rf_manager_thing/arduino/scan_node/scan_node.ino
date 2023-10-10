#include <SPI.h>

#include "RF24.h"
#include "printf.h"

RF24 radio(7, 8);

uint64_t rx_address = 0xFFFFFFFFF0LL;
uint64_t tx_address = 0xFFFFFFFFF1LL;
bool role = false;

char received_message[32];
char send_message[32];
char device_id[4];

struct PayloadStruct {
  char message[16];
  uint64_t addr;
};
PayloadStruct payload;

void SetupSensor();
void SetupRFModule();
char* Send_payload_with_ack(char* sent_message, int timeout = 1000);
bool Register();
void Run();

char* Send_payload_with_ack(char* sent_message, int timeout) {
  radio.stopListening();
  unsigned long start_timer = micros();
  radio.write(sent_message, sizeof(sent_message));
  unsigned long end_timer = micros();

  char* node_ID = NULL;
  uint8_t pipe;

  radio.startListening();
  unsigned long listen_start_timer = millis();
  while (millis() - listen_start_timer < timeout) {
    if (radio.available()) {
      int length = radio.getDynamicPayloadSize();
      if (length > 31) {
        Serial.print(F("too many byte"));
        break;
      }
      // char* received_message = (char*)malloc(sizeof(char) * (length + 1));
      radio.read(&received_message, length);
      received_message[length] = '\0';

      Serial.print(F(" Recieved "));
      Serial.print(length);
      Serial.print(F(" bytes on pipe "));
      Serial.print(pipe);
      Serial.print(F(": "));
      Serial.print(received_message);

      if (strncmp(received_message, "RACK", 4) == 0) {
        Serial.println(F(" ack is come"));
        memcpy(device_id, received_message + 4, 4);
        radio.stopListening();
      } else {
        Serial.println(F(" Not ack"));
        delay(200);
      }
    }
  }

  return 0;
}

void SetupRFModule() {
  Serial.begin(115200);
  while (!Serial) {
  }

  if (!radio.begin()) {
    Serial.println(F("radio hardware is not responding!!"));
    while (1) {
    }
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.enableDynamicPayloads();

  radio.enableAckPayload();

  radio.openWritingPipe(tx_address);
  radio.openReadingPipe(1, rx_address);
  radio.stopListening();

  Serial.println(F("SetupRFModule complete!!!"));
}

void SetupSensor() {
  bool registered = false;

  if (!registered) {
    registered = Register();
  }

  Serial.println(F("SetupSensor complete!!!"));
}

bool Register() {
  while (1) {
    Serial.println(F("send REG ..."));
    char* node_ID = Send_payload_with_ack("REG ", 5000);
    if (node_ID) {
      Serial.println(F("register complete!!!"));
      return true;
    }
  }
}

void Run() {
  Serial.println(F("Run executed"));
  radio.stopListening();
  unsigned long start_timer = micros();
  int sensor_value = analogRead(0);
  sprintf(send_message, "VAL %s%d", device_id, sensor_value);
  radio.write(send_message, sizeof(send_message));
  unsigned long end_timer = micros();
  delay(1000);
}

void setup() {
  SetupRFModule();
  SetupSensor();
}

void loop() { Run(); }