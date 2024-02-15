#include <Servo.h>
Servo brain;
const int motor = 10;
const int magnet=12;
const int magnetLED = 6;
const int photoResistanceLED = 5;

int ULUM=0;
int magnetState=0;

bool open = false;
bool magnetActivated = false;
bool enoughLight = false;


void setup() {
  brain.write(90);
  Serial.begin(9600);
  brain.attach(motor);
  pinMode(magnet, INPUT);
  pinMode(A0, INPUT);
  pinMode(magnetLED, OUTPUT);
  pinMode(photoResistanceLED, OUTPUT);
}

void loop() {
  if (not open) {
    ULUM=analogRead(A0);
    magnetState=digitalRead(magnet);
    if (magnetState==LOW) {
      Serial.println("Aimant activé");
      magnetActivated = true;
      digitalWrite(magnetLED, HIGH);
    } else {
      Serial.println("Aimant desactivé");
      magnetActivated = false;
      digitalWrite(magnetLED, LOW);
    }

    Serial.println(ULUM);
    if (ULUM > 200) {
      Serial.println("Lumière OK");
      enoughLight = true;
      digitalWrite(photoResistanceLED, HIGH);
    } else {
      Serial.println("Lumière éteinte");
      enoughLight = false;
      digitalWrite(photoResistanceLED, LOW);
    }
  }
  if (magnetActivated && enoughLight) {
  Serial.println("Coffre ouvert !");
  brain.write(0);
  open = true;
  delay(15000)
  Serial.println("Coffre fermé.");
  brain.write(90);
  open = false;
  }
  }
