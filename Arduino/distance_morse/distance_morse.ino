const int TRIGpin = 8;
const int ECHOpin = 9;
const int led=12;
const int sound=11;
bool running = false;
bool finish = false;
float duree;
float distance;

bool checkDistance() {
  digitalWrite(TRIGpin,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGpin,LOW);
  duree=pulseIn(ECHOpin,HIGH);
  distance = duree/1000000*343.4/2;
  Serial.println(distance);
  
	if (distance >= 0.35 && distance <=0.65) {
		return true;
		} else {
			return false;
		}
}

void setup() {
  pinMode(TRIGpin, OUTPUT);
  pinMode(ECHOpin, INPUT);
  digitalWrite(TRIGpin,LOW);
  pinMode(led, OUTPUT);
  pinMode(sound, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(TRIGpin,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGpin,LOW);
  duree=pulseIn(ECHOpin,HIGH);
  distance = duree/1000000*343.4/2;
  Serial.println(distance);

  while (distance >= 0.40 && distance <=0.60) {
    running = true;
    finish = false;
    Serial.println("N");
    // -
    digitalWrite(led, HIGH);
    delay(1500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    // changement de lettre
    delay(1500);
    if (not checkDistance()) {return;)

    Serial.println("E");
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // changement de lettre
    delay(1500);
    if (not checkDistance()) {return;)


    Serial.println("U");
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // -
    digitalWrite(led, HIGH);
    delay(1500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    // changement de lettre
    delay(1500);
    if (not checkDistance()) {return;)


    Serial.println("F");
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // -
    digitalWrite(led, HIGH);
    delay(1500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    // *
    digitalWrite(led, HIGH);
    delay(500);
    if (not checkDistance()) {return;)
    digitalWrite(led, LOW);
    delay(500);
    if (not checkDistance()) {return;)
    finish = true;
    running = false;

    /*
     _*   *   **_   **_*
     * 0.5
     - 1.5
    */
  }
if (running == true) {
  Serial.println("Arrêt du code ");
  digitalWrite(led, LOW);
  if (finish == true) {
    Serial.print("avec succès");
    tone(sound, 10000, 400);
	delay(550);
    tone(sound, 10000, 1500);
    while (distance < 0.40 or distance > 0.60) {delay(100}
  } else {
    Serial.print("avec echec");
    tone(sound, 200, 1500);
    }
  running = false;
  }
}
