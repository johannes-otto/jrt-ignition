int interruptor = 2;
int ignition = 3;

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
  unsigned long fromLow,fromHigh,toLow,toHigh;
  if (rt > 60000) {
    fromLow = rt;
    fromHigh = 60000;
    toLow = rt * 14 / 360; //below 1000 rpm
    toHigh = 2285;
  } //1000 rpm
  else if (rt > 30000) {
    fromLow = 60000;
    fromHigh = 30000;
    toLow = 2285;
    toHigh = 1142;
  } //2000rpm
  else if (rt > 20000) {
    fromLow = 30000;
    fromHigh = 20000;
    toLow = 1142;
    toHigh = 762;
  } //3000
  else if (rt > 15000) {
    fromLow = 20000;
    fromHigh = 15000;
    toLow = 762;
    toHigh = 571;
  } //4000
  else if (rt > 12000) {
    fromLow=15000;
    fromHigh=12000;
    toLow=571;
    toHigh=457;
    } //5000
  else if (rt > 10000) {
    fromLow=12000;
    fromHigh=10000;
    toLow=457;
    toHigh=381;
    } //6000
  else if (rt > 8571) {
    fromLow=10000;
    fromHigh=8571;
    toLow=381;
    toHigh=326;
    } //7000
  else {
    fromLow=8571;
    fromHigh=rt;
    toLow=326;
    toHigh=360*14/rt;
    } //

  return map(rt, fromLow, fromHigh, toLow, toHigh);
}

void ignite() {
  end_time = micros();
  round_time = start_time - end_time;
  start_time = end_time;
  delayMicroseconds(get_delay(round_time));
  digitalWrite(ignition, HIGH);
  delay(2);

}
void loop() {
  digitalWrite(ignition, LOW);
}
