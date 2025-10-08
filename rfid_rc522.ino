#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  SPI.begin();
  mfrc522.PCD_Init();

  // Инициализация ключа (по умолчанию все FFFF)
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println("Агуагу");
}

void loop() {
  // Проверяем, есть ли команда для записи
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("w")) {
      String textToWrite = command.substring(1);
      writeToBlock8(textToWrite);
    }
  }

  // Постоянное чтение RFID карты
  readBlock8();
  delay(1000); // Читаем каждую секунду
}

void readBlock8() {
  // Сбрасываем предыдущее состояние
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  MFRC522::StatusCode status;
  byte buffer[18];
  byte size = sizeof(buffer);

  // Проверяем наличие карты
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Аутентификация
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 8, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.println("READ_ERROR");
    return;
  }

  // Чтение блока 8
  status = mfrc522.MIFARE_Read(8, buffer, &size);
  if (status != MFRC522::STATUS_OK) {
    Serial.println("READ_ERROR");
    return;
  }

  // Выводим данные как текст
  String text = "";
  for (byte i = 0; i < 16; i++) {
    if (buffer[i] != 0 && buffer[i] != 32) { // Игнорируем нулевые байты и пробелы в конце
      text += (char)buffer[i];
    }
  }

  if (text.length() > 0) {
    Serial.println(text);
  }
}

void writeToBlock8(String text) {
  // Сбрасываем предыдущее состояние
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  MFRC522::StatusCode status;
  byte buffer[16];

  // Подготавливаем буфер для записи (16 байт)
  memset(buffer, 0, sizeof(buffer));

  // Копируем текст в буфер
  text.getBytes(buffer, sizeof(buffer));

  // Проверяем наличие карты
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    Serial.println("WRITE_ERROR");
    return;
  }

  // Аутентификация
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 8, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.println("WRITE_ERROR");
    return;
  }

  // Запись в блок 8
  status = mfrc522.MIFARE_Write(8, buffer, 16);
  if (status == MFRC522::STATUS_OK) {
    Serial.println("WRITE_SUCCESS");
  } else {
    Serial.println("WRITE_ERROR");
  }
}
