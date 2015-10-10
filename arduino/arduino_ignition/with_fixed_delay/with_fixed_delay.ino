int interruptor = 2;
int ignition = 3;
int def_ignition=26;
int offset=34;

unsigned long start_time = micros();
unsigned long end_time = micros();
unsigned long round_time = start_time - end_time;

void setup() {
  pinMode(interruptor, INPUT);
  digitalWrite(interruptor, HIGH);

  attachInterrupt(0, ignite, RISING);
  pinMode(ignition, OUTPUT);
  digitalWrite(ignition, LOW);
}

unsigned long get_delay(unsigned long rt) {
  return rt*(offset-def_ignition)/360;
}

void ignite() {
  end_time = micros();
  round_time = start_time - end_time;
  start_time = end_time;
  delayMicroseconds(get_delay(round_time)-(micros()-start_time));
  digitalWrite(ignition, HIGH);
  delay(2);

}
void loop() {
  digitalWrite(ignition, LOW);
}
